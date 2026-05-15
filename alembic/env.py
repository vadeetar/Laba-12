import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. ДОБАВЛЯЕМ ЭТИ СТРОКИ:
# Прописываем путь к корню проекта, чтобы Alembic нашел папку app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем Base и все наши модели
from app.core.database import Base
from app.models import *

# this is the Alembic Config object...
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. МЕНЯЕМ target_metadata = None НА:
target_metadata = Base.metadata

# ... дальше идет остальной стандартный код файла ...