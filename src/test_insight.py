from agents.data_cleaner import DataCleaner
from agents.eda_agent import EDAAgent
from agents.insight_agent import InsightAgent

cleaner = DataCleaner()
df, diag = cleaner.clean("demo_data/sales_sample.csv")

eda = EDAAgent()
stats, plots = eda.analyze(df)

insight = InsightAgent()
insights, path = insight.summarize(stats, plots)

print("Generated Insight File:", path)
print("\nInsights:")
for line in insights:
    print(line)
