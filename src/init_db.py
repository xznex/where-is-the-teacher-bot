from database import engine, Base
from models.audience import *


Base.metadata.create_all(bind=engine)
