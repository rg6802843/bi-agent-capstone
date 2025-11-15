import logging
import os
import time

from agents.data_cleaner import DataCleaner
from agents.eda_agent import EDAAgent
from agents.insight_agent import InsightAgent
from agents.report_builder import ReportBuilder
from session_manager import SessionManager
from utils import write_json_log


logging.basicConfig(level=logging.INFO)


class Coordinator:
    def __init__(self):
        self.cleaner = DataCleaner()
        self.eda = EDAAgent()
        self.insight = InsightAgent()
        self.report = ReportBuilder()
        self.session = SessionManager()

    def run(self, file_path: str):
        """
        Main pipeline runner for data → EDA → insights → report
        """

        # 1. Start session
        session_id = self.session.create_session(file_path)
        session_folder = os.path.join(self.session.sessions_dir, session_id)

        start_time = time.time()
        meta = self.session.load_meta(session_id)

        write_json_log(session_id, "Session started")

        # 2. Data Cleaning
        df, diag = self.cleaner.clean(file_path, session_folder)
        meta["metrics"]["rows_after_cleaning"] = df.shape[0]
        meta["metrics"]["columns"] = df.shape[1]
        meta["metrics"]["missing_before"] = diag["missing_values_before"]
        meta["metrics"]["missing_after"] = diag["missing_values_after"]
        self.session.save_meta(session_id, meta)

        # 3. EDA
        stats, plots = self.eda.analyze(df, session_folder)
        meta["metrics"]["plots_generated"] = len(plots)
        self.session.save_meta(session_id, meta)

        # 4. Insights
        insights, md_path = self.insight.summarize(stats, plots, session_folder)
        meta["metrics"]["insight_file"] = md_path
        self.session.save_meta(session_id, meta)

        # 5. Final Report
        report_path = self.report.build_report(
            session_id, df, stats, plots, insights, session_folder
        )

        meta["metrics"]["report_path"] = report_path
        meta["metrics"]["total_runtime_seconds"] = round(time.time() - start_time, 2)
        self.session.save_meta(session_id, meta)

        return report_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    c = Coordinator()
    final_report = c.run(args.file)
    print("Final Report:", final_report)
