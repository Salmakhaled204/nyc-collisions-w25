import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

# ---------------------------
# pastel palette
# ---------------------------
PASTEL_PINK = "#f7b2d9"
PASTEL_BLUE = "#a5c8ff"
PASTEL_MINT = "#c5f2d5"
PASTEL_YELLOW = "#ffe6a7"
DEEP_INDIGO = "#4b3f72"
PAGE_BG = "#fdf7ff"

# Bootstrap for basic layout
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
]

# ===========================
# 1) LOAD FULL MERGED DATA
# ===========================
print("Reading merged_final.csv (full file)...")
df = pd.read_csv("merged_final.csv")
print("Dashboard df shape:", df.shape)


# ===========================
# 2) HELPER: GUESS COLUMN NAMES
# ===========================
def guess_col(df, candidates):
    # exact match
    for c in candidates:
        if c in df.columns:
            return c
    # substring match (case-insensitive)
    for col in df.columns:
        for c in candidates:
            if c.lower() in col.lower():
                return col
    return None


collision_col = guess_col(df, ["collision_id"])
borough_col = guess_col(df, ["borough"])
year_col = guess_col(df, ["crash_year", "year"])
date_crash_col = guess_col(df, ["crash_date_crash", "crash_date"])
factor_col = guess_col(df, ["contributing_factor_vehicle_1", "contributing_factor"])
vehicle_col = guess_col(df, ["vehicle_type_code_1", "vehicle_type"])
age_col = guess_col(df, ["person_age_imputed", "person_age"])
injury_col = guess_col(df, ["person_injury_clean", "person_injury"])
lat_col = guess_col(df, ["latitude", "lat"])
lon_col = guess_col(df, ["longitude", "lon", "long"])
hour_col = guess_col(df, ["crash_hour", "hour"])
weekday_col = guess_col(df, ["crash_weekday"])

print("Detected columns:")
for name, val in [
    ("collision_col", collision_col),
    ("borough_col", borough_col),
    ("year_col", year_col),
    ("date_crash_col", date_crash_col),
    ("factor_col", factor_col),
    ("vehicle_col", vehicle_col),
    ("age_col", age_col),
    ("injury_col", injury_col),
    ("lat_col", lat_col),
    ("lon_col", lon_col),
    ("hour_col", hour_col),
    ("weekday_col", weekday_col),
]:
    print(f" {name}: {val}")


# ===========================
# 3) FEATURE ENGINEERING
# ===========================
# date → year + weekday
if date_crash_col is not None:
    df[date_crash_col] = pd.to_datetime(df[date_crash_col], errors="coerce")

    if year_col is None:
        df["crash_year_tmp"] = df[date_crash_col].dt.year
        year_col = "crash_year_tmp"

    if weekday_col is None:
        df["crash_weekday_tmp"] = df[date_crash_col].dt.day_name()
        weekday_col = "crash_weekday_tmp"

# age groups
if age_col is not None:
    df["age_group"] = pd.cut(
        df[age_col],
        bins=[0, 17, 30, 45, 60, 120],
        labels=["<18", "18–30", "31–45", "46–60", "60+"],
    )
else:
    df["age_group"] = "Unknown"

# injury column clean
if injury_col is not None:
    df[injury_col] = df[injury_col].fillna("UNKNOWN")
else:
    injury_col = None

# columns used for search
search_cols = [
    c
    for c in [borough_col, factor_col, vehicle_col, injury_col, "age_group", year_col]
    if c is not None
]


def unique_sorted(col):
    if col is None:
        return []
    return sorted(df[col].dropna().unique())


borough_options = unique_sorted(borough_col)
year_options = unique_sorted(year_col)
vehicle_options = unique_sorted(vehicle_col)
factor_options = unique_sorted(factor_col)
age_group_options = unique_sorted("age_group")

print(
    "Unique counts:",
    "borough",
    len(borough_options),
    "year",
    len(year_options),
    "vehicle",
    len(vehicle_options),
    "factor",
    len(factor_options),
    "age_group",
    len(age_group_options),
)


# ===========================
# small helper: pastel styling for all figs
# ===========================
def style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Segoe UI', system-ui", color=DEEP_INDIGO),
        title_font=dict(family="'Segoe UI', system-ui", size=16, color=DEEP_INDIGO),
        margin=dict(l=40, r=20, t=45, b=40),
    )
    return fig


# ===========================
# 4) DASH APP LAYOUT
# ===========================
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    style={
        "backgroundColor": PAGE_BG,
        "minHeight": "100vh",
        "padding": "22px 0",
        "fontFamily": "'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    },
    children=[
        html.Div(
            className="container",
            children=[
                # HEADER
                html.Div(
                    className="d-flex flex-column flex-md-row align-items-md-center justify-content-between mb-3",
                    children=[
                        html.Div(
                            children=[
                                html.H1(
                                    "NYC Motor Vehicle Collisions — Interactive Dashboard",
                                    style={
                                        "fontWeight": "700",
                                        "fontSize": "28px",
                                        "marginBottom": "0.25rem",
                                        "color": DEEP_INDIGO,
                                    },
                                ),
                                html.P(
                                    "Soft pastel view of crashes by borough, time, vehicles, and factors.",
                                    style={
                                        "color": "#7b6f9e",
                                        "marginBottom": "0",
                                        "fontSize": "14px",
                                    },
                                ),
                            ]
                        ),
                    ],
                ),

                # FILTER CARD
                html.Div(
                    className="card shadow-sm mb-3",
                    style={
                        "borderRadius": "16px",
                        "border": f"1px solid {PASTEL_PINK}33",
                    },
                    children=[
                        html.Div(
                            className="card-body",
                            children=[
                                html.H5(
                                    "Filters",
                                    className="card-title",
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "600",
                                        "color": DEEP_INDIGO,
                                    },
                                ),
                                html.Div(
                                    className="row g-2",
                                    children=[
                                        html.Div(
                                            className="col-md-3 col-sm-6",
                                            children=[
                                                html.Label(
                                                    "Borough",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="filter-borough",
                                                    options=[
                                                        {"label": b, "value": b}
                                                        for b in borough_options
                                                    ],
                                                    value=[],
                                                    multi=True,
                                                    placeholder="All boroughs",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="col-md-3 col-sm-6",
                                            children=[
                                                html.Label(
                                                    "Year",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="filter-year",
                                                    options=[
                                                        {"label": str(int(y)), "value": y}
                                                        for y in year_options
                                                    ],
                                                    value=[],
                                                    multi=True,
                                                    placeholder="All years",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="col-md-3 col-sm-6",
                                            children=[
                                                html.Label(
                                                    "Vehicle Type",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="filter-vehicle",
                                                    options=[
                                                        {"label": v, "value": v}
                                                        for v in vehicle_options
                                                    ],
                                                    value=[],
                                                    multi=True,
                                                    placeholder="All vehicle types",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="col-md-3 col-sm-6",
                                            children=[
                                                html.Label(
                                                    "Contributing Factor",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="filter-factor",
                                                    options=[
                                                        {"label": f, "value": f}
                                                        for f in factor_options
                                                    ],
                                                    value=[],
                                                    multi=True,
                                                    placeholder="All factors",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="col-md-3 col-sm-6 mt-2",
                                            children=[
                                                html.Label(
                                                    "Age Group",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="filter-age-group",
                                                    options=[
                                                        {"label": str(a), "value": str(a)}
                                                        for a in age_group_options
                                                    ],
                                                    value=[],
                                                    multi=True,
                                                    placeholder="All ages",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),

                # SEARCH + BUTTON CARD
                html.Div(
                    className="card shadow-sm mb-3",
                    style={
                        "borderRadius": "16px",
                        "border": f"1px solid {PASTEL_BLUE}33",
                    },
                    children=[
                        html.Div(
                            className="card-body",
                            children=[
                                html.Div(
                                    className="row g-2 align-items-center",
                                    children=[
                                        html.Div(
                                            className="col-md-10",
                                            children=[
                                                html.Label(
                                                    "Search mode (e.g. 'Brooklyn 2022 pedestrian')",
                                                    className="form-label mb-1",
                                                ),
                                                dcc.Input(
                                                    id="search-box",
                                                    type="text",
                                                    placeholder="Type keyword(s) and click Generate Report…",
                                                    style={
                                                        "width": "100%",
                                                        "padding": "8px 10px",
                                                        "borderRadius": "999px",
                                                        "border": "1px solid #d0cde8",
                                                        "backgroundColor": "#fdfbff",
                                                    },
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="col-md-2 d-grid",
                                            style={"marginTop": "26px"},
                                            children=[
                                                html.Button(
                                                    "Generate Report",
                                                    id="btn-generate",
                                                    n_clicks=0,
                                                    className="btn",
                                                    style={
                                                        "fontWeight": "600",
                                                        "height": "40px",
                                                        "borderRadius": "999px",
                                                        "border": "none",
                                                        "backgroundImage": f"linear-gradient(90deg,{PASTEL_PINK},{PASTEL_BLUE})",
                                                        "color": "white",
                                                        "boxShadow": "0 4px 10px rgba(0,0,0,0.12)",
                                                    },
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),

                # KPI CARD
                html.Div(
                    id="kpi-card",
                    className="shadow-sm mb-3",
                    style={
                        "borderRadius": "16px",
                        "border": f"1px solid {PASTEL_MINT}66",
                        "background": "#ffffff",
                        "padding": "10px 16px",
                        "fontWeight": "500",
                        "fontSize": "14px",
                        "color": DEEP_INDIGO,
                    },
                ),

                # TOP ROW GRAPHS
                html.Div(
                    className="row g-3 mb-3",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="card shadow-sm h-100",
                                    style={"borderRadius": "18px"},
                                    children=[
                                        html.Div(
                                            className="card-body",
                                            children=[
                                                dcc.Graph(
                                                    id="bar-borough",
                                                    config={"displayModeBar": False},
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="card shadow-sm h-100",
                                    style={"borderRadius": "18px"},
                                    children=[
                                        html.Div(
                                            className="card-body",
                                            children=[
                                                dcc.Graph(
                                                    id="line-year",
                                                    config={"displayModeBar": False},
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                    ],
                ),

                # MIDDLE ROW (heatmap + map)
                html.Div(
                    className="row g-3 mb-3",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="card shadow-sm h-100",
                                    style={"borderRadius": "18px"},
                                    children=[
                                        html.Div(
                                            className="card-body",
                                            children=[
                                                dcc.Graph(
                                                    id="heatmap-hour-weekday",
                                                    config={"displayModeBar": False},
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="card shadow-sm h-100",
                                    style={"borderRadius": "18px"},
                                    children=[
                                        html.Div(
                                            className="card-body",
                                            children=[
                                                dcc.Graph(
                                                    id="map-crashes",
                                                    config={"displayModeBar": True},
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                    ],
                ),

                # BOTTOM ROW (pie)
                html.Div(
                    className="row g-3 mb-4",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="card shadow-sm h-100",
                                    style={"borderRadius": "18px"},
                                    children=[
                                        html.Div(
                                            className="card-body",
                                            children=[
                                                dcc.Graph(
                                                    id="pie-injury",
                                                    config={"displayModeBar": False},
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)


# ===========================
# 5) CALLBACK: GENERATE REPORT
# ===========================
@app.callback(
    [
        Output("bar-borough", "figure"),
        Output("line-year", "figure"),
        Output("heatmap-hour-weekday", "figure"),
        Output("map-crashes", "figure"),
        Output("pie-injury", "figure"),
        Output("kpi-card", "children"),
    ],
    Input("btn-generate", "n_clicks"),
    State("filter-borough", "value"),
    State("filter-year", "value"),
    State("filter-vehicle", "value"),
    State("filter-factor", "value"),
    State("filter-age-group", "value"),
    State("search-box", "value"),
)
def update_dashboard(
    n_clicks,
    borough_sel,
    year_sel,
    vehicle_sel,
    factor_sel,
    age_group_sel,
    search_text,
):

    # start with all rows
    mask = pd.Series(True, index=df.index)

    borough_sel = borough_sel or []
    year_sel = year_sel or []
    vehicle_sel = vehicle_sel or []
    factor_sel = factor_sel or []
    age_group_sel = age_group_sel or []
    search_text = (search_text or "").strip()

    # dropdown filters
    if borough_col and borough_sel:
        mask &= df[borough_col].isin(borough_sel)
    if year_col and year_sel:
        mask &= df[year_col].isin(year_sel)
    if vehicle_col and vehicle_sel:
        mask &= df[vehicle_col].isin(vehicle_sel)
    if factor_col and factor_sel:
        mask &= df[factor_col].isin(factor_sel)
    if age_group_sel:
        mask &= df["age_group"].astype(str).isin(age_group_sel)

    # keyword search
    if search_text:
        tokens = search_text.split()
        search_mask = pd.Series(False, index=df.index)
        for token in tokens:
            token_mask = pd.Series(False, index=df.index)
            for col in search_cols:
                token_mask |= df[col].astype(str).str.contains(
                    token, case=False, na=False
                )
            search_mask |= token_mask
        mask &= search_mask

    print(
        f"[DEBUG] n_clicks={n_clicks}, search='{search_text}', rows_after_mask={mask.sum()}"
    )

    dff = df[mask]

    if dff.empty:
        empty_fig = style_fig(px.bar(title="No data for selected filters / search"))
        return (
            empty_fig,
            empty_fig,
            style_fig(px.imshow([[0]], title="No data")),
            style_fig(px.scatter_mapbox(lat=[], lon=[])),
            style_fig(px.pie(values=[1], names=["No data"])),
            "No data for the selected filters and search query.",
        )

    # 1) Bar – crashes per borough
    if borough_col:
        borough_counts = (
            dff.groupby(borough_col)[collision_col]
            .nunique()
            .reset_index(name="crash_count")
            .sort_values("crash_count", ascending=False)
        )
        bar_fig = px.bar(
            borough_counts,
            x=borough_col,
            y="crash_count",
            title="Number of Crashes per Borough",
            color_discrete_sequence=[PASTEL_PINK],
        )
        bar_fig = style_fig(bar_fig)
    else:
        bar_fig = style_fig(px.bar(title="Borough column not found"))

    # 2) Line – crashes over time
    if year_col:
        yearly_counts = (
            dff.groupby(year_col)[collision_col]
            .nunique()
            .reset_index(name="crash_count")
            .sort_values(year_col)
        )
        line_fig = px.line(
            yearly_counts,
            x=year_col,
            y="crash_count",
            markers=True,
            title="Crashes Over Time",
        )
        line_fig.update_traces(
            line=dict(color=PASTEL_BLUE, width=3),
            marker=dict(color=PASTEL_BLUE, size=6),
        )
        line_fig = style_fig(line_fig)
    else:
        line_fig = style_fig(px.line(title="Year column not found"))

    # 3) Heatmap – hour vs weekday
    if hour_col and weekday_col:
        tmp = dff.dropna(subset=[hour_col, weekday_col])
        if not tmp.empty:
            pivot = tmp.pivot_table(
                index=weekday_col,
                columns=hour_col,
                values=collision_col,
                aggfunc="nunique",
                fill_value=0,
            )
            heatmap_fig = px.imshow(
                pivot.values,
                x=pivot.columns,
                y=pivot.index,
                labels=dict(x="Hour of Day", y="Weekday", color="Crashes"),
                title="Crashes by Hour and Weekday",
                color_continuous_scale=[ "#fff7fb", PASTEL_PINK, PASTEL_BLUE ],
            )
            heatmap_fig = style_fig(heatmap_fig)
        else:
            heatmap_fig = style_fig(
                px.imshow([[0]], title="No data for hour/weekday")
            )
    else:
        heatmap_fig = style_fig(
            px.imshow([[0]], title="Hour / weekday columns not found")
        )

    # 4) Map – crash locations
    if lat_col and lon_col:
        dmap = dff.dropna(subset=[lat_col, lon_col])
        if len(dmap) > 5000:
            dmap = dmap.sample(5000, random_state=42)

        hover_name = borough_col if borough_col else collision_col
        hover_data = {}
        if collision_col:
            hover_data[collision_col] = True
        if factor_col:
            hover_data[factor_col] = True

        map_fig = px.scatter_mapbox(
            dmap,
            lat=lat_col,
            lon=lon_col,
            hover_name=hover_name,
            hover_data=hover_data,
            zoom=9,
            title="Crash Locations (sample of all rows for plotting)",
            height=450,
        )
        map_fig.update_traces(
            marker=dict(size=5, color=PASTEL_PINK, opacity=0.75)
        )
        map_fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
        )
        map_fig = style_fig(map_fig)
    else:
        map_fig = style_fig(
            px.scatter_mapbox(lat=[], lon=[], title="No location columns found")
        )

    # 5) Pie – injury severity
    if injury_col:
        pie_fig = px.pie(
            dff,
            names=injury_col,
            title="Injury Severity Distribution",
            color_discrete_sequence=[
                PASTEL_PINK,
                PASTEL_BLUE,
                PASTEL_YELLOW,
                PASTEL_MINT,
            ],
        )
        pie_fig = style_fig(pie_fig)
    else:
        pie_fig = style_fig(
            px.pie(
                values=[1],
                names=["Missing injury column"],
                title="Injury column not found",
            )
        )

    # KPI text
    if collision_col:
        total_crashes = dff[collision_col].nunique()
    else:
        total_crashes = len(dff)

    total_persons = len(dff)
    if age_col:
        avg_age = round(dff[age_col].mean(), 1)
    else:
        avg_age = "N/A"

    kpi_text = (
        f"Report generated from {total_crashes} distinct collisions "
        f"and {total_persons} person records. "
        f"Average age of involved persons: {avg_age}."
    )

    return bar_fig, line_fig, heatmap_fig, map_fig, pie_fig, kpi_text


# ===========================
# 6) RUN APP LOCALLY
# ===========================
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
