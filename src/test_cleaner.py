from agents.data_cleaner import DataCleaner

cleaner = DataCleaner()
df, diagnostics = cleaner.clean("demo_data/sales_sample.csv")

print("Diagnostics:")
print(diagnostics)
print("\nCleaned Data:")
print(df.head())
