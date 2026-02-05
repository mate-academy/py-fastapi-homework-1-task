from sqlalchemy.ext.asyncio import create_async_engine
from src.settings import get_settings

settings = get_settings()

# Build URL from PATH_TO_DB
db_url = f"sqlite+aiosqlite:///{settings.PATH_TO_DB}"
engine = create_async_engine(db_url, echo=False)
