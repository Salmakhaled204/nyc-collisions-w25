import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

csv_file = "merged_final.csv"
parquet_file = "merged_final.parquet"

chunksize = 100_000  # you can lower this if memory is still a problem

print("Starting chunked conversion...")
writer = None

for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize, low_memory=False)):
    print(f"  Processing chunk {i}...")
    table = pa.Table.from_pandas(chunk)

    if writer is None:
        writer = pq.ParquetWriter(parquet_file, table.schema)

    writer.write_table(table)

if writer is not None:
    writer.close()

print("Done! File saved as merged_final.parquet")
