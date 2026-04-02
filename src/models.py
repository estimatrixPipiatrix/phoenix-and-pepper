from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer


class Base(DeclarativeBase):
    pass


class Port(Base):
    __tablename__ = "ports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    size: Mapped[int] = mapped_column(Integer)
    base_fee: Mapped[int] = mapped_column(Integer)
