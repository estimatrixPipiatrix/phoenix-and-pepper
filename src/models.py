from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer, ForeignKey


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


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    origin_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))
    destination_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))
    distance_km: Mapped[float] = mapped_column(Float)
    base_sailing_days: Mapped[int] = mapped_column(Integer)
    danger_level: Mapped[int] = mapped_column(Integer)
    danger_type: Mapped[int] = mapped_column(String(50))
