import matplotlib.pyplot as plt
import seaborn as sns


def create_seaborn_chart(df):
    """Create a Seaborn bar chart for file categories."""

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="Category",
        y="File Count",
        hue="Category",
        legend=False
    )

    plt.title("FileFlow - Seaborn File Category Analysis")
    plt.xlabel("File Category")
    plt.ylabel("Number of Files")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.show()