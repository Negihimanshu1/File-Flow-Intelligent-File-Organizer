import matplotlib.pyplot as plt


def create_bar_chart(df):
    """Create a bar chart of file categories."""

    plt.figure(figsize=(10, 6))

    plt.bar(df["Category"], df["File Count"])

    plt.title("FileFlow - Files by Category")
    plt.xlabel("File Category")
    plt.ylabel("Number of Files")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.show()