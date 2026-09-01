# /// script
# dependencies = [
#     "cpi==2.0.10",
#     "marimo",
#     "mcp==2.1.1",
#     "pandas==3.0.5",
#     "ruff==0.16.5",
#     "ty==0.0.77",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import cpi
    import marimo as mo
    import pandas as pd

    return cpi, mo, pd


@app.cell
def _(cpi):
    cpi.update()
    return


@app.cell
def _():
    READ_COLS = [
        "recipient_name",
        "recipient_county_name",
        "action_date_fiscal_year",
        "prime_award_transaction_recipient_cd_current",
        "federal_action_obligation",
    ]
    READ_DTYPE = {"action_date_fiscal_year": str}
    return READ_COLS, READ_DTYPE


@app.cell
def _(READ_COLS, READ_DTYPE, cpi, pd):
    INFLATION_ADJUSTMENT_YEAR = "2025"

    def adjust_to_2025_dollars(value, source_year):
        return cpi.inflate(
            value, int(source_year), to=int(INFLATION_ADJUSTMENT_YEAR)
        )

    def read_defense_spend_data(year: str):
        df = pd.read_csv(
            f"./data/defense-contracts-{year}.csv",
            usecols=READ_COLS,
            dtype=READ_DTYPE,
        )
        return df

    return adjust_to_2025_dollars, read_defense_spend_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Fact-check
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # LA County

    > The total value of defense contracts won by companies in Los Angeles County more than doubled in the last 10 years after adjusting for inflation, according to an analysis by CalMatters and The Markup.
    """)
    return


@app.cell
def _(YEARS_OF_INTEREST, adjust_to_2025_dollars, mo, read_defense_spend_data):
    def read_la_county_data(year):
        df = read_defense_spend_data(year)
        return df[df["recipient_county_name"] == "LOS ANGELES"]

    _dfs = {year: read_la_county_data(year) for year in YEARS_OF_INTEREST}
    la_obligation_totals = {
        year: adjust_to_2025_dollars(
            _dfs[year]["federal_action_obligation"].sum(), int(year)
        )
        for year in YEARS_OF_INTEREST
    }

    la_2025_div_2015 = round(
        la_obligation_totals["2025"] / la_obligation_totals["2015"], 1
    )

    mo.md(
        f"The total value of defense contracts won by companies in Los Angeles County {la_2025_div_2015}x'd in the last 10 years after adjusting for inflation, according to an analysis by CalMatters and The Markup."
    )
    return (read_la_county_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > The $15 billion in contracts won in LA County last year went largely to old-school defense contractors with headquarters elsewhere, like Boeing.
    """)
    return


@app.cell
def _(mo, read_la_county_data):
    LAST_YEAR = "2025"
    df_la_spending_2025 = read_la_county_data(LAST_YEAR)

    sum_federal_obligation_in_la_county_2025 = df_la_spending_2025[
        "federal_action_obligation"
    ].sum()

    top10_la_cnty_recipients = (
        df_la_spending_2025.groupby("recipient_name")[
            "federal_action_obligation"
        ]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    mo.vstack(
        [
            f"The ${sum_federal_obligation_in_la_county_2025:,.0f} in contracts won in LA County {LAST_YEAR} went largely to old-school defense contractors with headquarters elsewhere, like Boeing.",
            mo.md("**Top 10 recepients in LA County**"),
            top10_la_cnty_recipients,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CA-36

    > The increase in defense contracts between 2015 and 2025 in that district [CA-36] alone was more than $3.3 billion.
    """)
    return


@app.cell
def _(adjust_to_2025_dollars, read_defense_spend_data):
    def calc_district_total_obligation(
        congressional_district: str,
        year: str,
        read_data_func=read_defense_spend_data,
    ):
        df = read_data_func(year)
        df_cd = df[
            df["prime_award_transaction_recipient_cd_current"]
            == congressional_district
        ]
        total_obligation = adjust_to_2025_dollars(
            df_cd["federal_action_obligation"].sum(), int(year)
        )
        return round(total_obligation)

    return (calc_district_total_obligation,)


@app.cell
def _(calc_district_total_obligation, mo):
    CA_CD_36 = "CA-36"
    YEARS_OF_INTEREST = ["2015", "2025"]

    ca_cd_36_total_obligation = {
        year: calc_district_total_obligation(CA_CD_36, year)
        for year in YEARS_OF_INTEREST
    }

    ca_cd_36_total_obligation_10y_difference = (
        ca_cd_36_total_obligation["2025"] - ca_cd_36_total_obligation["2015"]
    )

    mo.vstack(
        [
            f"The increase in defense contracts between 2015 and 2025 in that district alone [{CA_CD_36}] was {ca_cd_36_total_obligation_10y_difference:+,}.",
        ]
    )
    return (YEARS_OF_INTEREST,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CA-43

    > [Maxine] Waters’ district [CA-43] has seen its share of obligated defense department spending grow over the last decade by more than $1.6 billion, or more than 500%, adjusted for inflation.
    """)
    return


@app.cell
def _(YEARS_OF_INTEREST, calc_district_total_obligation, mo):
    CA_CD_43 = "CA-43"

    ca_cd_43_total_obligation = {
        year: calc_district_total_obligation(CA_CD_43, year)
        for year in YEARS_OF_INTEREST
    }

    ca_cd_43_total_obligation_10y_difference = (
        ca_cd_43_total_obligation["2025"] - ca_cd_43_total_obligation["2015"]
    )

    ca_cd_43_total_obligation_10y_growth_pct = (
        100
        * (
            ca_cd_43_total_obligation["2025"]
            - ca_cd_43_total_obligation["2015"]
        )
        / ca_cd_43_total_obligation["2015"]
    )

    mo.vstack(
        [
            f"Waters’ district [{CA_CD_43}] has seen its share of obligated defense department spending grow over the last decade by {ca_cd_43_total_obligation_10y_difference:+,}, or {ca_cd_43_total_obligation_10y_growth_pct:+.0f}%. adjusted for inflation.",
        ]
    )
    return


if __name__ == "__main__":
    app.run()
