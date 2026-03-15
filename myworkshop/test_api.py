from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import DateTime, Integer, String, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite+aiosqlite:///./users.db"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
	pass


class UserTable(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
	email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
	)


class UserCreate(BaseModel):
	email: EmailStr
	username: str = Field(min_length=3, max_length=30, pattern=r"^[a-z0-9_]+$")


class UserUpdate(BaseModel):
	email: EmailStr | None = None
	username: str | None = Field(default=None, min_length=3, max_length=30, pattern=r"^[a-z0-9_]+$")


class UserResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	email: str
	username: str
	created_at: datetime


async def get_session() -> AsyncGenerator[AsyncSession, None]:
	async with SessionLocal() as session:
		yield session


async def seed_users(session: AsyncSession) -> None:
	count_stmt = select(func.count(UserTable.id))
	count = await session.scalar(count_stmt)
	if count and count > 0:
		return

	session.add_all(
		[
			UserTable(id=1, username="alice", email="alice@example.com"),
			UserTable(id=2, username="bob", email="bob@example.com"),
			UserTable(id=3, username="charlie", email="charlie@example.com"),
		]
	)
	await session.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	async with SessionLocal() as session:
		await seed_users(session)

	yield


app = FastAPI(title="Async User API", lifespan=lifespan)


def map_integrity_error_to_conflict(exc: IntegrityError) -> str:
	error_text = str(exc.orig).lower()
	if "users.email" in error_text or "email" in error_text:
		return "Email already exists"
	if "users.username" in error_text or "username" in error_text:
		return "Username already exists"
	return "Unique constraint violation"


async def fetch_user_by_id(user_id: int, session: AsyncSession) -> UserTable | None:
	stmt = select(UserTable).where(UserTable.id == user_id)
	result = await session.execute(stmt)
	return result.scalar_one_or_none()


async def fetch_users(session: AsyncSession) -> list[UserTable]:
	stmt = select(UserTable).order_by(UserTable.id)
	result = await session.execute(stmt)
	return list(result.scalars().all())


async def create_user(data: UserCreate, session: AsyncSession) -> UserTable:
	new_user = UserTable(email=data.email, username=data.username)
	session.add(new_user)
	try:
		await session.commit()
	except IntegrityError as exc:
		await session.rollback()
		raise HTTPException(status_code=409, detail=map_integrity_error_to_conflict(exc)) from exc

	await session.refresh(new_user)
	return new_user


async def patch_user(user_id: int, data: UserUpdate, session: AsyncSession) -> UserTable | None:
	user = await fetch_user_by_id(user_id, session)
	if user is None:
		return None

	update_data = data.model_dump(exclude_unset=True)
	for field_name, field_value in update_data.items():
		setattr(user, field_name, field_value)

	if not update_data:
		return user

	try:
		await session.commit()
	except IntegrityError as exc:
		await session.rollback()
		raise HTTPException(status_code=409, detail=map_integrity_error_to_conflict(exc)) from exc

	await session.refresh(user)
	return user


async def remove_user(user_id: int, session: AsyncSession) -> bool:
	user = await fetch_user_by_id(user_id, session)
	if user is None:
		return False

	await session.delete(user)
	await session.commit()
	return True


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
	return await create_user(data, session)


@app.get("/users", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
	return await fetch_users(session)


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
	user = await fetch_user_by_id(user_id, session)
	if user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return user


@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_session)):
	user = await patch_user(user_id, data, session)
	if user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
	deleted = await remove_user(user_id, session)
	if not deleted:
		raise HTTPException(status_code=404, detail="User not found")