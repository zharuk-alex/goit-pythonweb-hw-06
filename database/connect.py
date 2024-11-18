from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from database.models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    # logger.info(f"Schema '{engine.url.database}' created.")
else:
    # logger.info(f"Schema '{engine.url.database}' allready exist.")
    pass

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
