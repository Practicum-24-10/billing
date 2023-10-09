from database.core.config import pg_config
from database.db import AsyncPostgres


engine: AsyncPostgres = AsyncPostgres(pg_config.db_user,
                                      pg_config.db_password,
                                      pg_config.db_host,
                                      pg_config.db_port,
                                      pg_config.db_name)
