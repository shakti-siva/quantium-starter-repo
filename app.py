import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load & clean data
# -----------------------------
df = pd.read_csv("sales.csv")

# Clean sales column
df["sales"] = df["sales"].astype(str).str.replace("$", "", regex=False)
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["sales", "date", "region"])

# Aggregate sales by date + region
df = df.groupby(["date", "region"], as_index=False)["sales"].sum()
df = df.sort_values("date")

# -----------------------------
# Cutoff date
# -----------------------------
cutoff_date = pd.to_datetime("2021-01-15")

# -----------------------------
# Dash app
# -----------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    
    html.Label("Select Region(s):", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        options=[{'label': r.title(), 'value': r} for r in df["region"].unique()],
        value=list(df["region"].unique()),  # default = all regions
        multi=True,
        id="region-filter"
    ),
    
    dcc.Graph(id="sales-graph"),
    html.Div(id="summary", style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '18px'})
])

# -----------------------------
# Callbacks
# -----------------------------
@app.callback(
    [Output("sales-graph", "figure"),
     Output("summary", "children")],
    [Input("region-filter", "value")]
)
def update_graph(selected_regions):
    filtered = df[df["region"].isin(selected_regions)]
    
    # Pre/post averages
    pre_avg = filtered[filtered["date"] < cutoff_date]["sales"].mean()
    post_avg = filtered[filtered["date"] >= cutoff_date]["sales"].mean()
    change = ((post_avg - pre_avg) / pre_avg * 100) if pre_avg else 0
    
    # Line chart
    fig = px.line(
        filtered,
        x="date",
        y="sales",
        color="region",
        title="Pink Morsel Sales Over Time",
        labels={"sales": "Total Sales ($)", "date": "Date"}
    )

    # Vertical line (price increase)
    fig.add_shape(
        type="line",
        x0=cutoff_date,
        x1=cutoff_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", dash="dash")
    )
    fig.add_annotation(
        x=cutoff_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price Increase",
        showarrow=False,
        yanchor="bottom",
        font=dict(color="red")
    )
    
    # Avg lines
    if not pd.isna(pre_avg):
        fig.add_hline(
            y=pre_avg,
            line_dash="dot",
            line_color="blue",
            annotation_text="Avg Before",
            annotation_position="bottom right"
        )
    if not pd.isna(post_avg):
        fig.add_hline(
            y=post_avg,
            line_dash="dot",
            line_color="green",
            annotation_text="Avg After",
            annotation_position="top right"
        )
    
    fig.update_layout(template="plotly_white", title_x=0.5, margin=dict(l=50, r=50, t=80, b=50))
    
    # Summary text
    summary_text = f"Average sales {'increased' if change>=0 else 'decreased'} by {abs(change):.1f}% after the price rise"
    
    return fig, summary_text

if __name__ == "__main__":
    app.run(debug=True)
