# /// script
# dependencies = [
#     "cpi==2.0.10",
#     "marimo",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from glob import glob

    import cpi
    import marimo as mo
    import pandas as pd

    return cpi, glob, mo, pd


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
def _(glob):
    data_fps = sorted(glob("./data/*.csv"))
    return


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

        # Commented out for the timebeing b/c cpi is too slow
        # df["federal_action_obligation_original"] = df[
        #     "federal_action_obligation"
        # ]
        # df["federal_action_obligation"] = df[
        #     "federal_action_obligation"
        # ].apply(
        #     lambda obligation: adjust_to_2025_dollars(obligation, int(year))
        # )

        return df

    return (read_defense_spend_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Fact-check
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > The total value of defense contracts won by companies in Los Angeles County nearly tripled in the last 10 years after adjusting for inflation, according to an analysis by CalMatters and The Markup.
    """)
    return


@app.cell
def _(YEARS_OF_INTEREST, read_defense_spend_data):
    def read_la_county_data(year):
        df = read_defense_spend_data(year)
        return df[df["recipient_county_name"] == "LOS ANGELES"]

    _dfs = {year: read_la_county_data(year) for year in YEARS_OF_INTEREST}

    la_2025_obligation_total = _dfs["2025"]["federal_action_obligation"].sum()
    la_2015_obligation_total = _dfs["2015"]["federal_action_obligation"].sum()

    round(la_2025_obligation_total / la_2015_obligation_total, 1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > The $15 billion in contracts won in LA County last year went largely to old-school defense contractors with headquarters elsewhere, like Boeing.
    """)
    return


@app.cell
def _(read_defense_spend_data):
    DF_2025_SPENDING = read_defense_spend_data("2025")
    df_la_spending_2025 = DF_2025_SPENDING[
        DF_2025_SPENDING["recipient_county_name"] == "LOS ANGELES"
    ]

    sum_federal_obligation_in_la_county_2025 = df_la_spending_2025[
        "federal_action_obligation"
    ].sum()

    print(
        f"The {sum_federal_obligation_in_la_county_2025:,.0f} in contracts won in LA County last year..."
    )
    return (df_la_spending_2025,)


@app.cell
def _(df_la_spending_2025):
    df_la_spending_2025.groupby("recipient_name")[
        "federal_action_obligation"
    ].sum().sort_values(ascending=False).head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > In 2015, 14 of the top 100 defense contracts won in California went to businesses focused on drones or space, according to the CalMatters and Markup analysis. By 2025, that share was up to 21. The shift is similar if measured by dollars, from 13%to 18%.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > California’s 36th Congressional District includes El Segundo, a high-tech defense hub outside Los Angeles. In the district’s 2024 House race, incumbent Democrat Ted Lieu took nearly 70 percent of the vote over a Republican challenger. The increase in defense contracts between 2015 and 2025 in that district alone was more than $3.6 billion.
    """)
    return


@app.cell
def _(read_defense_spend_data):
    CA_CD_36 = "CA-36"
    YEARS_OF_INTEREST = ["2015", "2025"]

    def calc_district_total_obligation(congressional_district: str, year: str):
        df = read_defense_spend_data(year)
        df_cd = df[
            df["prime_award_transaction_recipient_cd_current"]
            == congressional_district
        ]
        total_obligation = df_cd["federal_action_obligation"].sum()
        return round(total_obligation)

    ca_cd_36_total_obligation = {
        year: calc_district_total_obligation(CA_CD_36, year)
        for year in YEARS_OF_INTEREST
    }

    ca_cd_36_total_obligation_10y_difference = (
        ca_cd_36_total_obligation["2025"] - ca_cd_36_total_obligation["2015"]
    )

    print(
        f"The increase in defense contracts between 2015 and 2025 in that district alone was {ca_cd_36_total_obligation_10y_difference:+,}."
    )
    return YEARS_OF_INTEREST, calc_district_total_obligation


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Another district, California’s 43rd, is represented by Maxine Waters, who in 2021 signed on to the proposed No Militarization of Space Act, which described the Space Force as an unnecessary waste of resources and sought to abolish it.

    > Trump recently proposed to double the budget of the Space Force, another potential boon to the area. Meanwhile, Waters’ district has seen its share of obligated defense department spending grow over the last decade by more than $1.6 billion, or more than 500%, adjusted for inflation. Waters’ office didn’t respond to a request for comment.
    """)
    return


@app.cell
def _(YEARS_OF_INTEREST, calc_district_total_obligation):
    CA_CD_43 = "CA-43"

    ca_cd_43_total_obligation = {
        year: calc_district_total_obligation(CA_CD_43, year)
        for year in YEARS_OF_INTEREST
    }

    ca_cd_43_total_obligation_10y_difference = (
        ca_cd_43_total_obligation["2025"] - ca_cd_43_total_obligation["2015"]
    )

    print(
        f"Waters’ district has seen its share of obligated defense department spending grow over the last decade by {ca_cd_43_total_obligation_10y_difference:+,}."
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
