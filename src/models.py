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


class ShipType(Base):
    __tablename__ = "ship_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    cargo_capacity_tons: Mapped[int] = mapped_column(Integer)
    base_speed_knots: Mapped[float] = mapped_column(Float)
    operating_speed_knots: Mapped[float] = mapped_column(Float)
    operating_cost_daily: Mapped[int] = mapped_column(Integer)
    can_carry_phoenix: Mapped[bool] = mapped_column(default=False)


class Ship(Base):
    __tablename__ = "ships"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    ship_type_id: Mapped[int] = mapped_column(ForeignKey("ship_types.id"))
    home_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))
    condition: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50))


class CargoType(Base):
    __tablename__ = "cargo_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    cargo_class: Mapped[str] = mapped_column(String(20))
    unit_price_denarii: Mapped[int] = mapped_column(Integer)
    unit_weight_kg: Mapped[float] = mapped_column(Float)
    special_handling: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )
