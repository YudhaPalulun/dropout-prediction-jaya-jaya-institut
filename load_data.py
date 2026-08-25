import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data.csv", sep=";")

engine = create_engine("postgresql://hr_user:hr_pass@localhost:5432/hr_attrition")
df.to_sql("students", engine, if_exists="replace", index=False)
print("Selesai, jumlah baris:", len(df))