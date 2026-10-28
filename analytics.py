import pandas as pd


def create_dataframe(categories):
    """Create a Pandas DataFrame from file categories."""

    data = {
        "Category": list(categories.keys()),
        "File Count": list(categories.values())
    }

    df = pd.DataFrame(data)

    return df


def check_missing_values(df):
    """Check missing/null values in the DataFrame."""

    missing_values = df.isnull().sum()

    return missing_values


def show_analysis(df):
    """Display basic analysis of the DataFrame."""

    print("\n📊 PANDAS DATA ANALYSIS")
    print("==============================")

    print("\nFile Category Data:")
    print(df)

    print("\nTotal Files:", df["File Count"].sum())

    print(
        "Maximum Files in a Category:",
        df["File Count"].max()
    )

    print(
        "Minimum Files in a Category:",
        df["File Count"].min()
    )

    print("\nMissing Values:")
    print(check_missing_values(df))