import plotly.express as px


def create_plotly_chart(df):
    """Create an interactive Plotly chart."""

    fig = px.bar(
        df,
        x="Category",
        y="File Count",
        title="FileFlow - Interactive File Category Analysis",
        labels={
            "Category": "File Category",
            "File Count": "Number of Files"
        },
        hover_data=["File Count"]
    )

    fig.update_layout(
        xaxis_title="File Category",
        yaxis_title="Number of Files",
        template="plotly_white"
    )

    fig.show()