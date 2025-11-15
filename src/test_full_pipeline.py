from coordinator import Coordinator

c = Coordinator()
report_path = c.run("demo_data/sales_sample.csv")

print("PIPELINE COMPLETED!")
print("Final Report Path:", report_path)
