SERVER = "DESKTOP-6783BGC\MSSQLSERVER007"
DATABASE = "Lab7"
DRIVER = "SQL Server Native Client 11.0"
USERNAME = "Roman"
PASSWORD = "12345678"


DATABASE_CONNECTION = f"mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}"