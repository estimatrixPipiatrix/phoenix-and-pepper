from sqlalchemy import create_engine
from src.models import Base

engine = create_engine(
    "postgresql://phoenix:pepper@localhost:5432/phoenix_and_pepper"
)
Base.metadata.create_all(engine)
print("Tabulae creatae!")
