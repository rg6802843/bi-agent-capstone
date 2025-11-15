from agents.data_cleaner import DataCleaner
from agents.eda_agent import EDAAgent
from agents.insight_agent import InsightAgent
from agents.report_builder import ReportBuilder

cleaner = DataCleaner()
df, diag = cleaner.clean("demo_data/sales_sample.csv")

eda = EDAAgent()
stats, plots = eda.analyze(df)

insight = InsightAgent()
insights, insights_path = insight.summarize(stats, plots)

report = ReportBuilder()
report_path = report.build_report("test_session", df, stats, plots, insights)

print("Report generated at:", report_path)
