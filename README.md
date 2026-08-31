# How we examined defense industry contracts in California
This repo contains data for our story "Defense tech is booming in California. Trump may push it even further."
<h2>Methodology</h2>
The Markup and CalMatters downloaded the following data on defense industry contracts from <a href=
                                                                                             https://www.usaspending.gov/>usaspending.gov</a>.
The data includes any federal obligations from fiscal years 2002 to 2026 where the awarding agency was the Department of Defense and the recipient's location was in California. Our analysis looks at changes over time by California congressional district.
In the /data folder, a .csv for each year includes:
<ul>
  <li><b>"recipient_name"</b>: name of contract winner</li>
  <li><b>"action_date_fiscal_year"</b>: the fiscal year when agency issued the action</li>
  <li><b>"prime_award_transaction_recipient_cd_current"</b>: current congressional district listed for the winner</li>
  <li><b>"federal_action_obligation"</b>: dollars committed as part of agreement</li>
</ul>
## License

Code in this repository is licensed under the Apache License, Version 2.0; see [LICENSE](LICENSE).
