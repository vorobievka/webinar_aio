from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

PG_DSN = 'sqlite+aiosqlite:///data.db'

engine = create_async_engine(PG_DSN)


class Base(DeclarativeBase, AsyncAttrs):
    pass


Session = async_sessionmaker(engine, expire_on_commit=False)


class People(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    # json: Mapped[dict] = mapped_column(JSON, nullable=True)
    birth_year: Mapped[str] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(nullable=True)
    films: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    hair_color: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[str] = mapped_column(nullable=True)
    homeworld: Mapped[str] = mapped_column(nullable=True)
    mass: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    skin_color: Mapped[str] = mapped_column(nullable=True)
    species: Mapped[str] = mapped_column(nullable=True)
    starships: Mapped[str] = mapped_column(nullable=True)
    vehicles: Mapped[str] = mapped_column(nullable=True)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
