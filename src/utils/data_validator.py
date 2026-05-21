import pandas as pd


REQUIRED_CASE_COLUMNS = [
    "case_id",
    "received_date",
    "district",
    "issue_category_lv1",
]


REQUIRED_QUESTION_COLUMNS = [
    "question_id",
    "meeting_date",
    "councilor_name",
    "topic_category_lv1",
]


class DataValidator:
    @staticmethod
    def validate_columns(df: pd.DataFrame, required_columns: list):
        missing = [c for c in required_columns if c not in df.columns]
        return missing


if __name__ == "__main__":
    cases = pd.read_csv("data/samples/sample_1999_cases.csv")
    missing = DataValidator.validate_columns(
        cases,
        REQUIRED_CASE_COLUMNS
    )

    if missing:
        print("Missing columns:", missing)
    else:
        print("Validation passed")
