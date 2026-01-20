# 1) Bring in the tools we need
import pandas as pd                 # for reading CSV and working with tables
from dash import Dash, html, dcc    # for making a Dash web app
import plotly.express as px         # for making charts

# 2) Read the CSV file into a table (DataFrame)
df = pd.read_csv("outputfile.csv")

# 3) Make sure the "date" column is treated like real dates
df["date"] = pd.to_datetime(df["date"])

# 4) Sort the table so dates go in correct order
df = df.sort_values("date")

# 5) Add up sales per day (so we get one number per date)
daily = df.groupby("date", as_index=False)["sales"].sum()

# 6) Create a line chart: date on x-axis, sales on y-axis
fig = px.line(
    daily,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"}
)

# 7) Create the Dash app
app = Dash(__name__)

# 8) Build the page layout (title + description + chart)
app.layout = html.Div(
    children=[
        html.H1("Pink Morsel Sales Visualiser"),
        html.P("Line chart of total Pink Morsel sales by day."),
        dcc.Graph(figure=fig),
    ]
)

# 9) Start the app server
if __name__ == "__main__":
    app.run(debug=True)


