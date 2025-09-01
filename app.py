import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your processed sales data
df = pd.read_csv("data/processed_sales.csv", parse_dates=["date"])

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Region:", style={"fontWeight": "bold"}),
        dcc.RadioItems(
            id="region-selector",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"}
            ],
            value="all",
            labelStyle={"display": "inline-block", "margin": "0 10px"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    dcc.Graph(id="sales-line-chart")
])

# Callback for interactivity
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Use color parameter to differentiate regions
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        color="region" if selected_region == "all" else None,  # color by region only if "all" is selected
        title=f"Sales Over Time ({selected_region.capitalize()})"
    )

    # Add vertical line for price increase (15 Jan 2021)
    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white"
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
