# import oracledb
# class OracleLoginRepository:
#     def __init__(self, conn):
#         self.conn = conn

#     def get_list_users(self):
#         with self.conn.cursor() as cursor:

#             # OUT parameters
#             out_total_pages = cursor.var(oracledb.NUMBER)
#             out_data = cursor.var(oracledb.CLOB)
#             out_error = cursor.var(oracledb.STRING, 4000)

#             cursor.callproc(
#                 "pkg_api_handler.p_get_list_users",
#                 [
#                     0,
#                     10,
#                     None,
#                     "01-04-2025",
#                     "30-04-2025",
#                     None,
#                     out_total_pages,
#                     out_data,
#                     out_error,
#                 ],
#             )

#             # Read OUT values
#             total_pages = int(out_total_pages.getvalue() or 0)

#             data_clob = out_data.getvalue()
#             data = data_clob.read() if data_clob else None

#             error = out_error.getvalue()

#             return {
#                 "total_pages": total_pages,
#                 "data": data,       # JSON string (CLOB)
#                 "error": error,
#             }