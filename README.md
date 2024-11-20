# Macroeconomic Monitor

This project aims at providing the most accurate and up-to-date data about the Vietnamese economy.

With the data, you can make fancy figures.

## Procedure

- I scrape the data from GSO (stored in `.xml` format). In total, there are 13 databases.
- I then extract the information from these databases and store them in one single `.json` file.

**Notes**: We used archived links for now since some of the links are not accessible in real-time.

The archived links contain data until the end of 2023.


## Data sources

- Vietnam consolidated macroeconomic data: [DSBB Standard](http://nsdp.gso.gov.vn/index.htm)

- General Statistics Office of Vietnam: [GSO](https://pxweb.gso.gov.vn/pxweb/en/)

- My dataset collection: [thanhqtran/dataset](https://github.com/thanhqtran/dataset)

## Code Reference:

- Real-time routines: [Scheduling Notebook and Script Runs with GitHub Actions](https://towardsdatascience.com/scheduling-notebook-and-script-runs-with-github-actions-cc60f3ac17f2), with [Git Repo](https://github.com/venkatesannaveen/medium-articles).

- [Git-hub Stats real-time visualization](https://github.com/jstrieb/github-stats)

- [Making gif animation plots](https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30)
  
## To visualize data structure

- [json viewer](http://jsonviewer.stack.hu/)

- [Code Beautify](https://codebeautify.org)

### Deployed at [Macro Monitor](https://thanhqtran.github.io/macroeconomicmonitor/)
