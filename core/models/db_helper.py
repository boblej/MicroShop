from sqlalchemy.ext.asyncio import create_async_engine, engine, async_sessionmaker, AsyncSession

from core.config import DATABASE_URL

class DataBaseHelper:

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

db_helper = DataBaseHelper(
    url=DATABASE_URL,
    echo=True,
)
