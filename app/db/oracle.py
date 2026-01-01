# import oracledb
# from app.core.config import settings

# # Global connection pools (VERY IMPORTANT)
# oracle_pool = oracledb.create_pool(
#     dsn=settings.ORACLE_DSN,
#     user=settings.ORACLE_USER,
#     password=settings.ORACLE_PASSWORD,
#     min=5, # minimum open connections
#     max=20, # maximum connections
#     increment=5, # grow pool by this amount
#     getmode=oracledb.POOL_GETMODE_WAIT,  # wait if pool is busy
# )

# # oracle2_pool = oracledb.create_pool(
# #     dsn=settings.ORACLE2_DSN,
# #     user=settings.ORACLE2_USER,
# #     password=settings.ORACLE2_PASSWORD,
# #     min=5,
# #     max=20,
# #     increment=5,
# #     threaded=True,
# # )
