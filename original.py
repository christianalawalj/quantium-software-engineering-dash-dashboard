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
total_sales = daily["sales"].sum()
avg_daily_sales = daily["sales"].mean()

max_sales_row = daily.loc[daily["sales"].idxmax()]
max_sales_value = max_sales_row["sales"]
max_sales_date = max_sales_row["date"].strftime("%b %d, %Y")


# 6) Create a line chart: date on x-axis, sales on y-axis
fig = px.line(
    daily,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"}
)
fig.update_layout(
    template="plotly_white",
    title_font_size=18,
    margin=dict(l=40, r=40, t=60, b=40),
)

# 7) Create the Dash app
app = Dash(__name__)

# 8) Build the page layout (title + description + chart)
#
app.layout = html.Div(  # create an invisible box that holds everything
    style={
        "fontFamily": "Arial, sans-serif",  # use a clean readable font
        "backgroundColor": "#f5f6f8",       # light gray background not completely white
        "padding": "30px",                  # space between the edge of the screen and content
    },
    children=[  # everything inside the page goes here

        # Header
        html.H1(
            "Pink Morsel Sales Dashboard",
            style={"marginBottom": "5px"},  # keep the large heading close to the subtitle title > subtitle > content
        ),

        html.P(
            "Interactive dashboard showing daily sales trends for Pink Morsel Products",
            style={"color": "#555", "marginBottom": "30px"}  # gray text softer than the title Big bottom margin space before KPIs
        ),

        html.Div(
            style={
                "display": "flex",          # arrange the children side by side
                "gap": "20px",              # space between the cards
                "marginBottom": "30px",     # space before the chart
            },
            children=[

                # Total Sales
                html.Div(
                    style={
                        "backgroundColor": "white", #white card
                        "padding": "20px", #space inside the card
                        "borderRadius": "8px", #rounded corners
                        "flex": "1", #all cards are the same width
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.1)", #subtle depth to look more professional
                    },
                    children=[
                        html.P("Total Sales", style={"color": "#777"}),
                        html.H3(f"${total_sales:,.0f}")   # FIXED formatting
                    ]
                ),

                # Average Daily Sales
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "flex": "1",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
                    },
                    children=[
                        html.P("Average Daily Sales", style={"color": "#777"}),
                        html.H3(f"${avg_daily_sales:,.0f}")  # FIXED formatting
                    ]
                ),

                # Highest Sales Day
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "flex": "1",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
                    },
                    children=[
                        html.P("Highest Sales Day", style={"color": "#777"}), #show the biggest sales number
                        html.H3(f"${max_sales_value:,.0f}"),
                        html.P(max_sales_date, style={"color": "#777"}),# show the date underneath in smaller text
                    ]
                ),
            ]
        ),

        html.Div( #this is a card that holds the chart
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
            },
            children=[
                dcc.Graph(figure=fig) #dash graph component, with the plotly chart built previously
            ]
        ),

        # Shows Business Thinking and connects the chart to a decision.
        html.P(
            "Daily Pink Morsel sales show a clear structural increase beginning in early 2021, "
            "indicating that the price increase implemented in January 2021 led to higher sustained revenue.",
            style={"marginTop": "20px", "color": "#444"}
        )
    ]
)

# 9) Start the app server
if __name__ == "__main__":
    app.run(debug=True)
