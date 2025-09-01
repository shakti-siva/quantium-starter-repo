import dash
from dash import html

# Create app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Hello Quantium!", style={"textAlign": "center"}),
    html.P("If you can see this, Dash works 🎉")
])

# Run server
if __name__ == "__main__":
    print("🚀 Dash app is starting... open http://127.0.0.1:8050/")
    app.run(debug=True)

