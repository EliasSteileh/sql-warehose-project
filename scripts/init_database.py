
import os
import duckdb

db_path = "datawarehouse.duckdb"

# Delete database file if exists
if os.path.exists(db_path):
    os.remove(db_path)

# Create new database and schemas
con = duckdb.connect(db_path)

con.execute("CREATE SCHEMA bronze;")
con.execute("CREATE SCHEMA silver;")
con.execute("CREATE SCHEMA gold;")

con.close()
print("Database initialized successfully.")