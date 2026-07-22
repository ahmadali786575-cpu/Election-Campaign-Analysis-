import os
import pandas as pd

from flask import Flask, render_template, request, redirect, url_for, session
import joblib
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "election_dataset_fixed_10states.csv")

df = pd.read_csv(DATA_PATH, comment="#")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR,"data","election_dataset.csv")
voting_df = pd.read_csv(DATA_PATH, comment="#")
# Load trained ML model
model = joblib.load("model.pkl")
model_accuracy = joblib.load("accuracy.pkl")

@app.route("/")
def dashboard():

    year = request.args.get("year", "All")

    if year == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Year"] == int(year)]

    total_constituencies = filtered_df["Constituency"].nunique()

    total_candidates = filtered_df["Candidate"].nunique()

    total_parties = filtered_df["Party"].nunique()

    total_votes = filtered_df["Votes_Polled"].sum()

    # Convert total spending from Rupees to Crores
    total_expenditure = round(
        filtered_df["Campaign_Spending"].sum() / 10000000,
        2
    )

    # Votes Over Years

    votes_year = df.groupby("Year")["Votes_Polled"].sum().reset_index()

    years = votes_year["Year"].tolist()

    votes = (votes_year["Votes_Polled"] / 1000000).round(1).tolist()


    # Party Vote Share

    party_share = (
        filtered_df.groupby("Party")["Votes_Received"]
        .sum()
    )

    party_share = (party_share / party_share.sum()) * 100
    party_share = party_share.sort_values(ascending=False)

    top_parties = party_share.head(6)

    parties = top_parties.index.tolist()
    vote_share = top_parties.round(2).tolist()

    # ==============================
    # Top States by Votes Polled
    # ==============================

    state_data = (
        filtered_df
        .groupby("State")["Votes_Polled"]
        .sum()
        .sort_values(ascending=False)
        .head(5)

    )

    states = state_data.index.tolist()

    state_votes = (state_data / 1_000_000).round(1).tolist()


    # ==============================
    # Votes Trend
    # ==============================

    trend = (
        df.groupby("Year")["Campaign_Spending"]
        .sum()
        .reset_index()
    )

    trend_years = trend["Year"].tolist()
    # Convert Rupees to Crores
    trend_votes = (trend["Campaign_Spending"] / 10000000).round(1).tolist()
    # ==============================
    # Top Winning Parties
    # ==============================

    winner_data = (
        filtered_df[filtered_df["Winner"] == "Yes"]
        .groupby("Party")
        .size()
        .sort_values(ascending=False)
        .head(6)
    )

    winner_parties = winner_data.index.tolist()
    winner_counts = winner_data.values.tolist()


    # ==============================
    # Top Candidates
    # ==============================

    top_candidates_df = (
        filtered_df[filtered_df["Winner"] == "Yes"]
        .sort_values("Votes_Received", ascending=False)
        .head(5)
    )

    top_candidates = (
        top_candidates_df["Candidate"] + " (" + top_candidates_df["Party"] + ")"
    ).tolist()

    candidate_votes = (
        top_candidates_df["Votes_Received"] / 100000
    ).round(2).tolist()


 # ==============================
# Recent Election Highlights
# ==============================

# Highest Votes Polled (Millions)
 # ==============================
# Recent Election Highlights
# ==============================

    highest_votes = (
        df.groupby("Year")["Votes_Polled"]
        .sum()
        .max() / 1_000_000
    )

    most_seats = (
        df[df["Winner"] == "Yes"]
        .groupby("Party")
        .size()
    )

    highest_vote_share = round(df["Vote_Share_%"].max(), 1)
    top_party = most_seats.idxmax()
    top_seats = most_seats.max()

    highest_spending = (
    df.groupby("Year")["Campaign_Spending"]
    .sum()
    .max() / 10000000
    )

    registered_parties = df["Party"].nunique()

    return render_template(
        "index.html",
        total_constituencies=total_constituencies,
        total_candidates=total_candidates,
        total_parties=total_parties,
        total_votes=total_votes,
        total_expenditure=total_expenditure,
  
        years=years,
        votes=votes,
        parties=parties,
        vote_share=vote_share,
        states=states,
        state_votes=state_votes,

        trend_years=trend_years,
        trend_votes=trend_votes,

        winner_parties=winner_parties,
        winner_counts=winner_counts,

        top_candidates=top_candidates,
        candidate_votes=candidate_votes,
        highest_votes=round(highest_votes,1),
        highest_vote_share=highest_vote_share,
        top_party=top_party,
        top_seats=top_seats,
        highest_spending=round(highest_spending,2),
        registered_parties=registered_parties,
        )

@app.route("/voting-analysis")
def voting_analysis():

    # ==========================
    # Get Filters
    # ==========================

    year = request.args.get("year", "All")
    state = request.args.get("state", "All")
    party = request.args.get("party", "All")
    constituency = request.args.get("constituency", "All")

    # ==========================
    # Apply Filters
    # ==========================

    filtered_df = voting_df.copy()

    if year != "All":
        filtered_df = filtered_df[
            filtered_df["Year"] == int(year)
        ]

    if state != "All":
        filtered_df = filtered_df[
            filtered_df["State"] == state
        ]

    if party != "All":
        filtered_df = filtered_df[
            filtered_df["Party"] == party
        ]

    if constituency != "All":
        filtered_df = filtered_df[
            filtered_df["Constituency"] == constituency
        ]

    # ==============================
    # Votes Polled Over Years
    # ==============================

    trend_df = voting_df.copy()

    # Apply State filter only
    if state != "All":
        trend_df = trend_df[
            trend_df["State"] == state
        ]

    # Apply Party filter only
    if party != "All":
        trend_df = trend_df[
            trend_df["Party"] == party
        ]

    # Apply Constituency filter only
    if constituency != "All":
        trend_df = trend_df[
            trend_df["Constituency"] == constituency
        ]

    trend_constituency = (
        trend_df
        .groupby(
            ["Year", "State", "Constituency"],
            as_index=False
        )
        .agg({
            "Votes_Polled": "max"
        })
    )

    votes_year = (
        trend_df
        .groupby("Year", as_index=False)
        .agg({
            "Votes_Polled": "sum"
        })
    )

    vote_years = votes_year["Year"].tolist()

    votes_million = (
        votes_year["Votes_Polled"] / 1000000
    ).round(1).tolist()

    # ==============================
    # Average Turnout Over Years
    # ==============================
    # ==============================
# Average Turnout Over Years
# ==============================

    # ==========================================
# Average Turnout Chart (Ignore Year Filter)
# ==========================================

    turnout_chart_df = voting_df.copy()

    # Apply only State filter
    if state != "All":
        turnout_chart_df = turnout_chart_df[
            turnout_chart_df["State"] == state
        ]

    # Apply only Party filter
    if party != "All":
        turnout_chart_df = turnout_chart_df[
            turnout_chart_df["Party"] == party
        ]

    # Apply only Constituency filter
    if constituency != "All":
        turnout_chart_df = turnout_chart_df[
            turnout_chart_df["Constituency"] == constituency
        ]

    # One record per constituency
    turnout_chart_df = (
        turnout_chart_df
        .groupby(
            ["Year", "State", "Constituency"],
            as_index=False
        )
        .first()
    )

    turnout_year = (
        turnout_chart_df
        .groupby("Year", as_index=False)
        .agg({
            "Votes_Polled": "sum",
            "Registered_Electors": "sum"
        })
    )

    turnout_year["Turnout"] = (
        turnout_year["Votes_Polled"]
        /
        turnout_year["Registered_Electors"]
    ) * 100

    turnout_years = turnout_year["Year"].tolist()

    turnout_values = turnout_year["Turnout"].round(2).tolist()
    
    # ======================================
    # One Record Per Constituency
    # ======================================

    constituency_df = (
        filtered_df
        .groupby(
            ["Year", "State", "Constituency"],
            as_index=False
        )
        .agg({
            "Votes_Polled": "max",
            "Registered_Electors": "max"
        })
    )

    total_votes = int(
        filtered_df["Votes_Polled"].sum()
    )
    average_turnout = round(
        (
            constituency_df["Votes_Polled"].sum()
            /
            constituency_df["Registered_Electors"].sum()
        ) * 100,
        2
    )


    # State with Highest & Lowest Turnout
    # ===========================
    # ===========================
    # Highest / Lowest Turnout
    # ===========================

    state_df = filtered_df.copy()

    # One row per constituency
    state_df = (
        state_df
        .groupby(
            ["Year", "State", "Constituency"],
            as_index=False
        )
        .agg({
            "Votes_Polled": "max",
            "Registered_Electors": "max"
        })
    )

    state_turnout = (
        state_df
        .groupby("State", as_index=False)
        .agg({
            "Votes_Polled": "sum",
            "Registered_Electors": "sum"
        })
    )

    state_turnout["Turnout"] = (
        state_turnout["Votes_Polled"]
        /
        state_turnout["Registered_Electors"]
    ) * 100

    state_turnout = state_turnout.sort_values(
        by="Turnout",
        ascending=False
    )

    # ===========================
    # Highest / Lowest Turnout
    # ===========================

    if constituency != "All":

        highest_state = constituency
        highest_turnout = average_turnout

        lowest_state = constituency
        lowest_turnout = average_turnout

    else:

        state_df = filtered_df.copy()

        state_df = (
            state_df
            .groupby(
                ["Year", "State", "Constituency"],
                as_index=False
            )
            .agg({
                "Votes_Polled": "max",
                "Registered_Electors": "max"
            })
        )

        state_turnout = (
            state_df
            .groupby("State", as_index=False)
            .agg({
                "Votes_Polled": "sum",
                "Registered_Electors": "sum"
            })
        )

        state_turnout["Turnout"] = (
            state_turnout["Votes_Polled"]
            /
            state_turnout["Registered_Electors"]
        ) * 100

        state_turnout = state_turnout.sort_values(
            by="Turnout",
            ascending=False
        )

        if state_turnout.empty:

            highest_state = "-"
            highest_turnout = 0

            lowest_state = "-"
            lowest_turnout = 0

        elif len(state_turnout) == 1:

            highest_state = state_turnout.iloc[0]["State"]
            highest_turnout = round(state_turnout.iloc[0]["Turnout"], 2)

            lowest_state = state_turnout.iloc[0]["State"]
            lowest_turnout = round(state_turnout.iloc[0]["Turnout"], 2)

        else:

            highest_state = state_turnout.iloc[0]["State"]
            highest_turnout = round(state_turnout.iloc[0]["Turnout"], 2)

            lowest_state = state_turnout.iloc[-1]["State"]
            lowest_turnout = round(state_turnout.iloc[-1]["Turnout"], 2)

    # Filter according to selected year
    constituency_df = filtered_df

    
    # ======================================
    # Top 10 Constituencies (Raw Sum)
    # ======================================

    # Raw votes for display
    top_constituencies = (
        filtered_df
        .groupby(
            ["Constituency", "State"],
            as_index=False
        )
        .agg({
            "Votes_Polled": "sum"
        })
    )

    # Correct turnout calculation
    turnout_df = (
        filtered_df
        .groupby(
            ["Constituency", "State"],
            as_index=False
        )
        .agg({
            "Votes_Polled": "max",
            "Registered_Electors": "max"
        })
    )

    turnout_df["Turnout"] = (
        turnout_df["Votes_Polled"]
        /
        turnout_df["Registered_Electors"]
    ) * 100

    # Merge turnout into the raw-votes table
    top_constituencies = top_constituencies.merge(
        turnout_df[
            ["Constituency", "State", "Turnout"]
        ],
        on=["Constituency", "State"],
        how="left"
    )

    top_constituencies = (
        top_constituencies
        .sort_values(
            by="Votes_Polled",
            ascending=False
        )
        .head(10)
    )
    

    # ==========================================
    # Top 10 States Chart (Raw Sum)
    # ==========================================

    state_chart_df = voting_df.copy()

    if year != "All":
        state_chart_df = state_chart_df[
            state_chart_df["Year"] == int(year)
        ]

    if party != "All":
        state_chart_df = state_chart_df[
            state_chart_df["Party"] == party
        ]

    # Do NOT group by constituency

    state_votes = (
        state_chart_df
        .groupby("State")["Votes_Polled"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    state_names = state_votes.index.tolist()

    state_votes_million = (
        state_votes / 1000000
    ).round(2).tolist()
    state_names = state_votes.index.tolist()

    state_votes_million = (
        state_votes / 1000000
    ).round(2).tolist()

    # ==========================================
    # Voting Insights Cards
    # ==========================================

    # Highest Votes Polled (Raw Sum)
    highest_votes = (
        filtered_df["Votes_Polled"].sum()
    )

    # Average Turnout
    average_turnout_card = round(average_turnout, 2)

    # Highest Turnout State / Constituency
    highest_turnout_name = highest_state
    highest_turnout_value = highest_turnout

    # Lowest Turnout State / Constituency
    lowest_turnout_name = lowest_state
    lowest_turnout_value = lowest_turnout

    # Most Active State (Highest Raw Votes)
    active_df = (
        filtered_df
        .groupby("State", as_index=False)
        .agg({
            "Votes_Polled": "sum"
        })
    )

    active_df = active_df.sort_values(
        by="Votes_Polled",
        ascending=False
    )

    if active_df.empty:
        most_active_state = "-"
        most_active_votes = 0
    else:
        most_active_state = active_df.iloc[0]["State"]
        most_active_votes = int(active_df.iloc[0]["Votes_Polled"])

    return render_template(
    "voting_analysis.html",

    selected_year=year,
    selected_state=state,
    selected_party=party,
    selected_constituency=constituency,
    highest_votes=highest_votes,

    average_turnout_card=average_turnout_card,

    highest_turnout_name=highest_turnout_name,
    highest_turnout_value=highest_turnout_value,

    lowest_turnout_name=lowest_turnout_name,
    lowest_turnout_value=lowest_turnout_value,

    most_active_state=most_active_state,
    most_active_votes=most_active_votes,

    years=sorted(voting_df["Year"].unique()),

    states=sorted(voting_df["State"].unique()),

    parties=sorted(voting_df["Party"].unique()),

    constituencies=sorted(voting_df["Constituency"].unique()),

    total_votes=total_votes,

    average_turnout=average_turnout,

    highest_state=highest_state,

    highest_turnout=highest_turnout,

    lowest_state=lowest_state,

    lowest_turnout=lowest_turnout,

    vote_years=vote_years,

    votes_million=votes_million,

    turnout_years=turnout_years,

    turnout_values=turnout_values,

    top_constituencies=top_constituencies.to_dict("records"),
    state_names=state_names,
    state_votes_million=state_votes_million,

)


@app.route("/about")
def about():

    # ===============================
    # Project Statistics
    # ===============================

    years_covered = df["Year"].nunique()

    states_covered = df["State"].nunique()

    constituencies_covered = (
        df
        .groupby(["State", "Constituency"])
        .ngroups
    )

    parties_covered = df["Party"].nunique()

    records = len(df)

    total_votes = int(df["Votes_Polled"].sum())

    total_spending = round(df["Campaign_Spending"].sum() / 10000000, 2)
    return render_template(
        "about.html",
        years_covered=years_covered,
        states_covered=states_covered,
        constituencies_covered=constituencies_covered,
        parties_covered=parties_covered,
        records=records,
        total_votes=total_votes,
        total_spending=total_spending,
        accuracy=model_accuracy
    
  
    )

@app.route("/prediction")
def prediction():

    year = request.args.get("year", "All")

    if year == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Year"] == int(year)]

    return render_template(
        "prediction.html",

        selected_year=year,
        accuracy=model_accuracy,

        years=sorted(df["Year"].unique()),

        states=sorted(filtered_df["State"].unique()),

        constituencies=sorted(filtered_df["Constituency"].unique()),

        candidates=sorted(filtered_df["Candidate"].unique()),

        educations=sorted(filtered_df["Education"].unique()),

        urban_rural=sorted(filtered_df["Urban_Rural"].unique()),

        incumbents=sorted(filtered_df["Incumbent"].unique()),

        criminal_cases=sorted(filtered_df["Criminal_Cases"].unique()),

        total_constituencies=filtered_df["Constituency"].nunique(),

        total_parties=filtered_df["Party"].nunique(),

        total_records=len(filtered_df)
    )

@app.route("/predict", methods=["POST"])
def predict():

    state = request.form["state"]
    constituency = request.form["constituency"]
    age = int(request.form["age"])
    education = request.form["education"]
    criminal = int(request.form["criminal"])
    assets = float(request.form["assets"])
    liabilities = float(request.form["liabilities"])
    spending = float(request.form["spending"])
    electors = int(request.form["electors"])
    urban = request.form["urban"]
    incumbent = request.form["incumbent"]

    sample = pd.DataFrame([{
        "State": state,
        "Constituency": constituency,
        "Age": age,
        "Education": education,
        "Criminal_Cases": criminal,
        "Assets": assets,
        "Liabilities": liabilities,
        "Campaign_Spending": spending,
        "Registered_Electors": electors,
        "Urban_Rural": urban,
        "Incumbent": incumbent
    }])

    prediction = model.predict(sample)[0]

    probability = round(
    max(model.predict_proba(sample)[0]) * 100,
    2
)



    return render_template(
    "prediction.html",

    active_page="dashboard",
    predicted_party=prediction,
    probability=round(probability,2),

    accuracy=model_accuracy,

    spending=spending,
    incumbent=incumbent,

    selected_year="All",


    states=sorted(df["State"].unique()),

    constituencies=sorted(df["Constituency"].unique()),

    candidates=sorted(df["Candidate"].unique()),

    educations=sorted(df["Education"].unique()),

    urban_rural=sorted(df["Urban_Rural"].unique()),

    incumbents=sorted(df["Incumbent"].unique()),

    criminal_cases=sorted(df["Criminal_Cases"].unique()),

    total_constituencies=df["Constituency"].nunique(),

    total_parties=df["Party"].nunique(),

    total_records=len(df)
)
if __name__ == "__main__":
    app.run(debug=True)



