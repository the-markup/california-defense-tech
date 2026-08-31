# How we examined defense industry contracts in California
This repo contains data for our story "Defense tech is booming in California. Trump may push it even further."

## Methodology
The Markup and CalMatters downloaded the following data on defense industry contracts from [usaspending.gov](https://www.usaspending.gov/).

The data includes any federal obligations from fiscal years 2002 to 2026 where the awarding agency was the Department of Defense and the recipient's location was in California. Our analysis looks at changes over time by California congressional district.
In the /data folder, a .csv for each year includes:

- **"recipient_name"**: name of contract winner
- **"action_date_fiscal_year"**: the fiscal year when agency issued the action
- **"prime_award_transaction_recipient_cd_current"**: current congressional district listed for the winner
- **"federal_action_obligation"**: dollars committed as part of agreement
- **"recipient_county_name"**: county where award recipient is based

## License

Code in this repository is licensed under the Apache License, Version 2.0; see [LICENSE](LICENSE).
