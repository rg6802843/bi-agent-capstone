import os
import pandas as pd
from datetime import datetime

# Absolute project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class DataCleaner:
    def __init__(self):
        # Force outputs folder to root directory
        self.output_dir = os.path.join(PROJECT_ROOT, "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load CSV file into a Pandas DataFrame."""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")

    def clean(self, file_path: str, session_folder: str):
        """Loads, cleans, returns cleaned df + diagnostics."""

        df = self.load_csv(file_path)
        diagnostics = {}
        diagnostics["initial_shape"] = df.shape

        # Remove duplicates
        df = df.drop_duplicates()
        diagnostics["after_duplicates"] = df.shape

        # Missing values diagnostics BEFORE
        diagnostics["missing_values_before"] = df.isnull().sum().to_dict()

        # Fill missing values
        for col in df.columns:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(
                    df[col].mode()[0] if not df[col].mode().empty else ""
                )

        # Missing values diagnostics AFTER
        diagnostics["missing_values_after"] = df.isnull().sum().to_dict()

        # Save cleaned file INSIDE session folder
        out_path = os.path.join(session_folder, "cleaned.csv")
        df.to_csv(out_path, index=False)

        diagnostics["cleaned_file"] = out_path

        return df, diagnostics
