import pandas as pd
import datawrappergraphics
import numpy as np
import logging

WORLD_CHART_ID = "bGaOM"
CANADA_CHART_ID = "qeH8o"
FIB_CHART_ID = "Em8sO"

raw_cases = pd.read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv", encoding="utf-8")

data = raw_cases[raw_cases["Status"].isin(["confirmed", "suspected"])].sample(frac=1)

for col, values in data.iteritems():
    data[col] = data[col].astype(str).str.replace("ʻ", "")
    
canada_percent = str(round((len(data[data["Country"] == "Canada"]) / len(data) *100), 1))


fib_chart = (datawrappergraphics.FibonacciChart(chart_id=FIB_CHART_ID)
             .data(data)
             .head(f"Confirmed and suspected monkeypox cases around the world")
             .deck(f"<b>{canada_percent}%</b> of worldwide cases have been in Canada.")
             .publish()
             )

raw = pd.read_csv("https://raw.githubusercontent.com/owid/notebooks/main/EdouardMathieu/monkeypox/owid-monkeypox-data.csv")

all_countries = raw.pivot(index="location", columns="date", values="total_confirmed_by_confirmation").dropna(axis=0)

latest_date = all_countries.columns[-1]

all_countries = all_countries.drop("World").sort_values(latest_date, ascending=False)

all_countries["current_rank"] = range(1, len(all_countries)+1)

canada_cases = all_countries.at["Canada", str(latest_date)]
us_cases = all_countries.at["United States", str(latest_date)]

# def get_rank_suffix(rank):
#     match rank:
#         case 1:
#             suffix = "st"
#         case 2:
#             suffix = "nd"
#         case 3:
#             suffix = "rd"
#         case _:
#             suffix = "th"
        
#     return rank
        
world_chart = (datawrappergraphics.Chart(chart_id=WORLD_CHART_ID)
    .data(all_countries)
    .head(f"Monkeypox around the world")
    .deck(f"<span style='color:#C42127;font-weight:500'>Canada</span> has had at least <b>{int(canada_cases)}</b> cases so far, and the <span style='color:#1F78B4;font-weight:500'>United States</span> has had at least <b>{int(us_cases)}</b> cases.")
    .footer(timestamp=True, byline="Dexter McMillan", source="Our World in Data")
    .publish()
    )

canada = raw.loc[raw["location"] == "Canada", ["date", "total_all_by_entry"]]

canada_chart = (datawrappergraphics.Chart(chart_id=CANADA_CHART_ID)
    .data(canada)
    .head(f"Confirmed and suspected monkeypox cases in <span style='color:#C42127'>Canada</span>")
    .deck(f"Canada has had <b>{int(canada_cases)}</b> total cases so far.")
    .footer(timestamp=True, byline="Dexter McMillan", source="Our World in Data")
    .publish()
    )