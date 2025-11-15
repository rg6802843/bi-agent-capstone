from agents.data_cleaner import DataCleaner
from agents.eda_agent import EDAAgent

cleaner = DataCleaner()
df, diag = cleaner.clean("demo_data/sales_sample.csv")

eda = EDAAgent()
stats, plots = eda.analyze(df)

print("Stats keys:", stats.keys())
print("Generated plots:")
for p in plots:
    print(" -", p)
