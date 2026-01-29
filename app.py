"""
pandas is used for data manipulation, i group, filter, roll averages, and it is used in what would be SQL / Spark
stands for this layer
"""
import pandas as pd
""" Plotly is a high level plotting API, it helps to create charts from dataframes
we use it for:
simple chart lines
multi-line charts (by region)
"""
import plotly.express as px
"""
This is lower level API and allows charts to be modified in detail. i use this for vertical markers and annotations 
"""""
import plotly.graph_objects as go
"""
Dash is a python webframework specifically for data apps. and allows UI to be built without javascript. 
It connect the Ui to data to charts using callback methods
"""

""" 
HTML is for html elements like buttons and divs 
"""
from dash import Dash, html, dcc, Input, Output, State
"""
creates the dropdown and date pickers and input / output / state 
"""
import dash_bootstrap_components as dbc
""" allows for professional UI structure and matched real entreprise dashboards used only for styling no logic."""


"""
Data Gold layer
this is the data from the output csv file produced in task 2 data processing python file. 
we alread have just sales, date, region for PINK MORSELF only sales = quantity * price
we merged the raw csvs given by the three files in the data folder
"""
df = pd.read_csv("outputfile.csv") #reads the csv file
df["date"] = pd.to_datetime(df["date"]) #turns dates to real datetime objects
df = df.sort_values("date") #sort the time series charts and order them because rolling averages depend on order and sadly dash and plotly do not fix this for us
"""
does the sales in pink morsels increase or decrease after the price increase of the product what occurs? 
"""
EVENT_DATE = pd.to_datetime("2021-01-15")  # this is the specific event time reference point of jan 15 2021 we are asked to evaluate “price increase” reference point

"""
groups all transactions by date
sums sales across regions
produces one row per day
"""
def build_daily(filtered_df: pd.DataFrame) -> pd.DataFrame:
    """
    Daily totals (all regions combined).
    """
    return filtered_df.groupby("date", as_index=False)["sales"].sum()

"""
allows regional breakdown
same gold dataset, different aggregation grain
"""
def build_daily_by_region(filtered_df: pd.DataFrame) -> pd.DataFrame:
    """
    ("Daily totals split by region."
     """
    return filtered_df.groupby(["date", "region"], as_index=False)["sales"].sum()

"""
smooths noisy daily data
reveals underlying trends

"""
def add_rolling_avg(daily: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    Adds a rolling average column to daily totals.
    """
    daily = daily.sort_values("date").copy()
    daily["sales_roll"] = daily["sales"].rolling(window=window, min_periods=1).mean()
    return daily

"""
Split data into pre-event and post-event Janurary 15
Compute mean sales in each period
Calculate percentage change
"""
def compute_uplift(daily: pd.DataFrame) -> tuple[float | None, float | None, float | None]:
    """
    Returns (pre_avg, post_avg, uplift_pct).
    If not enough data on either side, returns (None, None, None).
    """
    if daily.empty:
        return None, None, None

    pre = daily[daily["date"] < EVENT_DATE]
    post = daily[daily["date"] >= EVENT_DATE]

    if len(pre) < 5 or len(post) < 5:
        return None, None, None

    pre_avg = float(pre["sales"].mean())
    post_avg = float(post["sales"].mean())
    uplift_pct = ((post_avg - pre_avg) / pre_avg) * 100.0 if pre_avg != 0 else None
    return pre_avg, post_avg, uplift_pct

"""
prevents mixing of strings and numbers in calculations
"""
def money(n: float | None) -> str:
    if n is None:
        return "—"
    return f"${n:,.0f}"
"""
this is the event marker itself for Jan 15, 2021 to add it so that stakeholders can see on the chart itself
"""
def _add_event_marker(fig: go.Figure, date_min, date_max) -> None:
    """Adds the Jan 15, 2021 marker if it falls in range."""
    if date_min is None or date_max is None:
        return
    if date_min <= EVENT_DATE <= date_max:
        fig.add_vline(
            x=EVENT_DATE,
            line_width=2,
            line_dash="dot",
            line_color="rgba(255,159,28,0.95)",
        )
        fig.add_annotation(
            x=EVENT_DATE,
            y=1.02,
            yref="paper",
            text="Jan 15, 2021 event",
            showarrow=False,
            font=dict(size=12, color="rgba(255,159,28,0.95)"),
            xanchor="left",
        )
"""
make_fig(...)
This function:
receives already-aggregated data
applies a view lens
returns a fully styled Plotly figure
"""

def make_fig(
    daily: pd.DataFrame,
    view: str = "all",
    daily_by_region: pd.DataFrame | None = None,
) -> go.Figure:
    """
    view:
      - all     : daily totals line
      - pre     : pre-event daily totals for Jan 15
      - post    : post-event daily totals for Jan 15
      - region  : multi-line by region
      - rolling : 7-day rolling average line
    """
    if view == "region":
        if daily_by_region is None or daily_by_region.empty:
            fig = px.line(title=None)
            date_min, date_max = None, None
        else:
            fig = px.line(
                daily_by_region,
                x="date",
                y="sales",
                color="region",
                title=None,
                labels={"date": "Date", "sales": "Sales ($)", "region": "Region"},
            )
            fig.update_traces(line=dict(width=2.2))
            date_min, date_max = daily_by_region["date"].min(), daily_by_region["date"].max()
    else:
        plot_df = daily.copy()

        if view == "pre":
            plot_df = plot_df[plot_df["date"] < EVENT_DATE]
        elif view == "post":
            plot_df = plot_df[plot_df["date"] >= EVENT_DATE]
        elif view == "rolling":
            plot_df = add_rolling_avg(plot_df, window=7)

        y_col = "sales_roll" if view == "rolling" else "sales"

        fig = px.line(
            plot_df,
            x="date",
            y=y_col,
            title=None,
            labels={"date": "Date", y_col: "Sales ($)" if y_col == "sales" else "Sales (7-day avg)"},
        )

        fig.update_traces(
            line=dict(width=2.5),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>",
        )

        date_min, date_max = (plot_df["date"].min(), plot_df["date"].max()) if not plot_df.empty else (None, None)

    # Shared formatting
    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        xaxis=dict(showgrid=True, gridcolor="rgba(17,24,39,0.08)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(17,24,39,0.08)", tickprefix="$", separatethousands=True),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    # Event marker for views where it makes sense
    if view in {"all", "rolling", "region"}:
        _add_event_marker(fig, date_min, date_max)

    # Hide legend unless it's region view
    if view != "region":
        fig.update_layout(showlegend=False)

    return fig

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets) #cretes the web app, loads boostrap styleing and registers callbacks
server = app.server

app.title = "Pink Morsel Sales Dashboard"

"""
Layout which is static contains no data logic  for goos practice, it defines the navigation bar
the title and description'filters
KPI's
chart
footer
"""

app.layout = html.Div(
    [
        # Top nav
        html.Div(
            [
                html.Div(
                    [
                        html.Span(className="brand-badge"),
                        html.Span("QUANTIUM • FORAGE", className="brand-text"),
                    ],
                    className="topbar-brand",
                ),
                html.Div(
                    [
                        html.Div("OVERVIEW", className="topbar-navlink"),
                        html.Div("COMPANY", className="topbar-navlink active"),
                        html.Div("SCREENER", className="topbar-navlink"),
                        html.Div("INSIGHTS", className="topbar-navlink"),
                        html.Div("DASHBOARD", className="topbar-navlink"),
                    ],
                    className="topbar-links",
                ),
            ],
            className="topbar",
        ),

        html.Div(
            [
                # Title
                html.Div("Pink Morsel Sales Dashboard", className="page-title"),
                html.Div(
                    "Interactive dashboard for analyzing daily sales trends for Pink Morsel products. "
                    "Use the filters to explore patterns over time.",
                    className="page-subtitle",
                ),

                # Filters card
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("View", className="label"),
                                        dcc.Dropdown(
                                            id="view",
                                            options=[
                                                {"label": "All (Gold Dataset)", "value": "all"},
                                                {"label": "Pre Price Increase (Before Jan 15, 2021)", "value": "pre"},
                                                {"label": "Post Price Increase (On/After Jan 15, 2021)", "value": "post"},
                                                {"label": "By Region", "value": "region"},
                                                {"label": "7-day Rolling Average", "value": "rolling"},
                                            ],
                                            value="all",
                                            clearable=False,
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Div("Date Range", className="label"),
                                        dcc.DatePickerRange(
                                            id="date-range",
                                            min_date_allowed=df["date"].min().date(),
                                            max_date_allowed=df["date"].max().date(),
                                            start_date=df["date"].min().date(),
                                            end_date=df["date"].max().date(),
                                            display_format="MM/DD/YYYY",
                                        ),
                                    ]
                                ),
                                html.Button("Apply Filters", id="apply", n_clicks=0, className="btn-primary"),
                            ],
                            className="filters-grid",
                        ),
                    ],
                    className="card card-pad",
                ),

                html.Div(style={"height": "14px"}),

                # KPI cards
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Total Sales", className="kpi-title"),
                                html.Div(id="kpi-total", className="kpi-value"),
                                html.Div("Sum of daily totals in selected range", className="kpi-sub"),
                            ],
                            className="card card-pad",
                        ),
                        html.Div(
                            [
                                html.Div("Average Daily Sales", className="kpi-title"),
                                html.Div(id="kpi-avg", className="kpi-value"),
                                html.Div("Mean sales per day in selected range", className="kpi-sub"),
                            ],
                            className="card card-pad",
                        ),
                        html.Div(
                            [
                                html.Div("Highest Sales Day", className="kpi-title"),
                                html.Div(id="kpi-high", className="kpi-value"),
                                html.Div(id="kpi-high-date", className="kpi-sub"),
                            ],
                            className="card card-pad",
                        ),
                        html.Div(
                            [
                                html.Div("Post-Event Uplift", className="kpi-title"),
                                html.Div(id="kpi-uplift", className="kpi-value"),
                                html.Div(id="kpi-uplift-sub", className="kpi-sub"),
                            ],
                            className="card card-pad",
                        ),
                    ],
                    className="kpi-row",
                ),

                html.Div(style={"height": "14px"}),

                # Chart card
                html.Div(
                    [
                        html.Div("Daily Sales Over Time", className="section-title"),
                        dcc.Loading(
                            type="default",
                            children=dcc.Graph(id="sales-graph", config={"displayModeBar": True}),
                        ),
                    ],
                    className="card card-pad",
                ),

                # Footer
                html.Div(
                    [
                        html.Div("Privacy Statement  |  Terms of Use  |  Manage Cookies"),
                        html.Div("© 2026 Quantium Forage Simulation  |  Dash / Plotly"),
                    ],
                    className="footer",
                ),
            ],
            className="shell",
        ),
    ]
)

# -----------------------------
# Callbacks
# -----------------------------
@app.callback(
    Output("sales-graph", "figure"),
    Output("kpi-total", "children"),
    Output("kpi-avg", "children"),
    Output("kpi-high", "children"),
    Output("kpi-high-date", "children"),
    Output("kpi-uplift", "children"),
    Output("kpi-uplift-sub", "children"),
    Input("apply", "n_clicks"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("view", "value"),
)
def update_dashboard(n_clicks, start_date, end_date, view):
    filtered = df.copy()

    if start_date:
        filtered = filtered[filtered["date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["date"] <= pd.to_datetime(end_date)]

    daily = build_daily(filtered)
    daily_by_region = build_daily_by_region(filtered)

    fig = make_fig(daily, view=view, daily_by_region=daily_by_region)

    total_sales = float(daily["sales"].sum()) if not daily.empty else None
    avg_daily = float(daily["sales"].mean()) if not daily.empty else None

    if not daily.empty:
        high_row = daily.loc[daily["sales"].idxmax()]
        high_value = float(high_row["sales"])
        high_date = pd.to_datetime(high_row["date"]).strftime("%b %d, %Y")
    else:
        high_value, high_date = None, "—"

    pre_avg, post_avg, uplift_pct = compute_uplift(daily)

    uplift_text = "—" if uplift_pct is None else f"{uplift_pct:+.1f}%"
    uplift_sub = (
        "Not enough data on both sides of Jan 15, 2021"
        if uplift_pct is None
        else f"Pre: {money(pre_avg)} / Post: {money(post_avg)}"
    )

    return (
        fig,
        money(total_sales),
        money(avg_daily),
        money(high_value),
        high_date,
        uplift_text,
        uplift_sub,
    )

#execute app and run on a local server, enables live reloading and
if __name__ == "__main__":
    app.run(debug=True)