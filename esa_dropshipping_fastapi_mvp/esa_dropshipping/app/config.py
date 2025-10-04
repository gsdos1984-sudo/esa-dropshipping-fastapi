from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./esa.db")
    DF_STREET: str = os.getenv("DF_STREET", "W Military Hwy")
    DF_CITY: str = os.getenv("DF_CITY", "McAllen")
    DF_STATE: str = os.getenv("DF_STATE", "TX")
    DF_ZIP: str = os.getenv("DF_ZIP", "78503")

settings = Settings()
