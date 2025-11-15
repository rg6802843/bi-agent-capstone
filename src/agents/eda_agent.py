import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EDAAgent:
    def __init__(self):
        pass   # No plot_dir here

    def analyze(self, df: pd.DataFrame, session_folder: str):
        """Generate summary statistics + plots inside the session folder."""

        # Create plots folder (absolute path)
        plot_dir = os.path.join(session_folder, "plots")
        os.makedirs(plot_dir, exist_ok=True)

        stats = {}
        plot_paths = []

        # Summary statistics
        stats["describe"] = df.describe(include='all').to_dict()

        numeric_df = df.select_dtypes(include=['float64', 'int64'])

        # Correlation matrix
        if numeric_df.shape[1] > 1:
            corr = numeric_df.corr()
            stats["correlation"] = corr.to_dict()

            plt.figure(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="Blues")
            heatmap_path = os.path.join(plot_dir, "correlation_heatmap.png")
            plt.savefig(heatmap_path)
            plt.close()
            plot_paths.append(heatmap_path)
        else:
            stats["correlation"] = {}  # ensure key exists

        # Distributions
        for col in numeric_df.columns:
            plt.figure(figsize=(7, 5))
            sns.histplot(df[col], kde=False)
            dist_path = os.path.join(plot_dir, f"{col}_distribution.png")
            plt.savefig(dist_path)
            plt.close()
            plot_paths.append(dist_path)

        # Time-series trend
        if "date" in df.columns and "units_sold" in df.columns:
            try:
                df["date"] = pd.to_datetime(df["date"])
                df_sorted = df.sort_values("date")

                plt.figure(figsize=(8, 5))
                df_sorted.groupby("date")["units_sold"].sum().plot()
                ts_path = os.path.join(plot_dir, "units_sold_trend.png")
                plt.savefig(ts_path)
                plt.close()
                plot_paths.append(ts_path)
            except Exception:
                pass

        return stats, plot_paths
