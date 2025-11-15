import os
import json
from datetime import datetime

# Absolute project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class InsightAgent:
    def __init__(self):
        # Outputs folder should always be in project root
        self.output_dir = os.path.join(PROJECT_ROOT, "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def summarize(self, stats: dict, plot_paths: list, session_folder: str):
        """
        Generate human-readable business insights from stats & plots.
        (Rule-based version, no LLM yet)
        """
        describe = stats.get("describe", {})
        correlation = stats.get("correlation", {})

        insights = []

        # 1. Basic numeric insights
        if "units_sold" in describe:
            mean_units = describe["units_sold"]["mean"]
            max_units = describe["units_sold"]["max"]
            insights.append(f"- Average units sold: **{mean_units:.2f}**")
            insights.append(f"- Highest units sold in a single day: **{max_units}**")

        if "price" in describe:
            mean_price = describe["price"]["mean"]
            insights.append(f"- Average price across products: **{mean_price:.2f}**")

        # 2. Correlation insights
        if correlation:
            if "units_sold" in correlation and "price" in correlation["units_sold"]:
                corr = correlation["units_sold"]["price"]
                if corr < -0.3:
                    insights.append("- **Negative correlation** between price and units sold → Lower price tends to increase sales.")
                elif corr > 0.3:
                    insights.append("- **Positive correlation** between price and units sold → Higher-priced items sell more.")
                else:
                    insights.append("- Little correlation between price and units sold.")

        # 3. Plot Insights
        insights.append("\n### Plot Insights")
        insights.append("Generated plots show potential sales trends and distribution patterns.")

        # 4. Save insights into session folder
        out_path = os.path.join(session_folder, "insights.md")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# Business Insights Report\n\n")
            f.write("\n".join(insights))
            f.write("\n\n### Included Plots:\n")
            for p in plot_paths:
                f.write(f"- {p}\n")

        return insights, out_path
