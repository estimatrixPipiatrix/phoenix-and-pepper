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
    crew_cost_daily: Mapped[int] = mapped_column(Integer)


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
    handling_cost_per_unit: Mapped[int] = mapped_column(Integer, default=0)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    customer_type: Mapped[str] = mapped_column(String(50))
    home_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    destination_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))
    order_date: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(20))


class OrderLine(Base):
    __tablename__ = "order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    cargo_type_id: Mapped[int] = mapped_column(ForeignKey("cargo_types.id"))
    quantity: Mapped[int] = mapped_column(Integer)


class Voyage(Base):
    __tablename__ = "voyages"

    id: Mapped[int] = mapped_column(primary_key=True)
    ship_id: Mapped[int] = mapped_column(ForeignKey("ships.id"))
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    departure_date: Mapped[str] = mapped_column(String(10))
    arrival_date: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20))


class VoyageManifest(Base):
    __tablename__ = "voyage_manifest"

    id: Mapped[int] = mapped_column(primary_key=True)
    voyage_id: Mapped[int] = mapped_column(ForeignKey("voyages.id"))
    order_line_id: Mapped[int] = mapped_column(ForeignKey("order_lines.id"))


class VoyageCost(Base):
    __tablename__ = "voyage_costs"

    id: Mapped[int] = mapped_column(primary_key=True)
    voyage_id: Mapped[int] = mapped_column(ForeignKey("voyages.id"))
    ship_operations_cost: Mapped[int] = mapped_column(Integer)
    port_fees: Mapped[int] = mapped_column(Integer)
    crew_wages: Mapped[int] = mapped_column(Integer)
    phoenix_handling_cost: Mapped[int] = mapped_column(Integer)
    hazard_surcharge: Mapped[int] = mapped_column(Integer)
    total_cost: Mapped[int] = mapped_column(Integer)
