import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Load private key from file
with open(os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"], "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Convert to DER format that Snowflake connector expects
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

conn = snowflake.connector.connect(
    user=os.environ["SNOWFLAKE_USER"],
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    private_key=private_key_bytes,
    warehouse="TRANSFORMING",
    database="RAW",
    schema="TFRRS",
)


# Read master CSV
master_path = "../data/processed/master_results.csv"
df = pd.read_csv(master_path)

# Write to Snowflake, replacing existing data each run
success, nchunks, nrows, _ = write_pandas(
    conn=conn,
    df=df,
    table_name="PERFORMANCES",
    overwrite=True,
    auto_create_table=True,
)

print(f"Loaded {nrows} rows to RAW.TFRRS.PERFORMANCES")
conn.close()