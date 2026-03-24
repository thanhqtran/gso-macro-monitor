# Vietnam Macroeconomic Monitor

- (2025/06/06): Data archived until 20250601 was released.
- (2024/11/20): Data archived until 2023q2 was released.
- (2024/11/22): New data until 2024q3 are available now.

## Purposes

This project aims to provide the most accurate and up-to-date data on the Vietnamese economy.

Data retrieving procedure:

- Data is sourced from NSO's e-DSBB Excel files (stored at `nsdp.nso.gov.vn`). There are 5 datasets: GDP, CPI, IIP, LMI, PPI.
- `nso_scraper.py` downloads, parses, and plots the data directly from NSO's Excel files.
- Legacy XML scraping from GSO is also available via `scrape_all.py` (15 databases → single `.json` file).
- To download pre-built data, see `Release` on the right panel.

The comprehensive data can be found in e-DSBB at the [Excel sheets provided by NSO](http://nsdp.nso.gov.vn/).

## Usage

To install all dependencies, run

```sh
pip install -r requirements.txt
```

### NSO Excel scraper (new)

```sh
python nso_scraper.py
```

Downloads and caches Excel files to `data/`, parses all indicators into tidy CSVs, and saves plots. Available datasets:

| Key | Description | File |
| --- | --- | --- |
| `GDP` | National Accounts (quarterly & annual) | `GDP_VNM.xlsx` |
| `CPI` | Consumer Price Index | `CPI_VNM.xlsx` |
| `IIP` | Industrial Production Index | `IIP_VNM.xlsx` |
| `LMI` | Labor Market Indicators | `LMI_VNM.xlsx` |
| `PPI` | Producer Price Index | `PPI_VNM.xlsx` |

To scrape a specific dataset in your own script:

```python
from nso_scraper import download_excel, parse_nso_sheet, get_series, NSO_LINKS

content = download_excel(NSO_LINKS["GDP"])
df = parse_nso_sheet(content, "Dataset_Q")       # quarterly sheet
gdp = get_series(df, "NGDP_R_PA_XDC")           # real GDP series
```

### GSO XML scraper (legacy)

- To scrape all data at once, run `scrape_all.py`
- After scraping, filter variables of interest with `make_df.py`
- Data description: `dsbb_indicator_desc.csv`
- All databases listed in: `dsbb_database.csv`

## Tiếng Việt

Để tiện cho mục tiêu nghiên cứu, mình viết một số script trên Python để cho máy đọc dữ liệu chính thức từ Tổng cục thống kê GSO.

Với CSDL này, chúng ta có thể vẽ các biểu đồ cơ bản hoặc ước lượng các mô hình vĩ mô.

Hiện nay GSO có 15 CSDL kinh tế, chủ yếu quan tâm đến các dữ liệu vĩ mô theo quý.

Những ai cần dùng có thể tải về toàn bộ data ở mục `Release`.

Do link `SDMX` của GSO không ổn định, nhiều khi không truy cập được nên mình chỉ sử dụng các đường link sao lưu trên Internet Archive ở thời điểm gần nhất (2023/12/31). Riêng dữ liệu về Tài khoản quốc gia có từ 2010q1 đến 2023q2. Dữ liệu từ 2023q2 trở đi có thể truy cập thủ công ở các bảng tính [Excel cung cấp bởi GSO](http://nsdp.gso.gov.vn/index.htm).

Trong tương lai, khi đường link chính ổn định hơn, mình sẽ update `Release` mới.

Phần link gốc không có mô tả ý nghĩa `@INDICATOR`. Ai quan tâm có thể tham khảo ở file `dsbb_indicator_desc.csv`.


---


## Data sources

- Vietnam consolidated macroeconomic data: [DSBB Standard](http://nsdp.gso.gov.vn/index.htm)

- General Statistics Office of Vietnam: [GSO](https://pxweb.gso.gov.vn/pxweb/en/)

- My dataset collection: [thanhqtran/dataset](https://github.com/thanhqtran/dataset)

**ASEAN**:

- Thailand National Account Statistics [From 1993Q1](https://www.nesdc.go.th/en/)
- Singapore National Account (Singstat) [From 1975Q1](https://www.singstat.gov.sg/find-data/search-by-theme/economy/national-accounts/latest-data)
- Malaysia National Account [From 2000Q1](https://ekonomi.gov.my/en/socio-economic-statistics/socio-economic/national-accounts)
- Indonesian National Account [From 1990Q1](https://fred.stlouisfed.org/tags/series?t=gdp%3Bindonesia%3Bquarterly)
- Phillippines [From 1981Q1](https://openstat.psa.gov.ph/Metadata/Economic-Accounts/National-Accounts-of-the-Philippines/Quarterly-Gross-Domestic-Product-Series-Q1-1981-to-Q4-2023)
- Brunei [From 2014Q1](https://deps.mofe.gov.bn/SitePages/National%20Accounts.aspx)
- Cambodia [Annual_only](https://www.nbc.gov.kh/english/economic_research/NSDP.html)
- Lao PDR [Annual only](https://laosis.lsb.gov.la/)


## Code Reference:

- Real-time routines: [Scheduling Notebook and Script Runs with GitHub Actions](https://towardsdatascience.com/scheduling-notebook-and-script-runs-with-github-actions-cc60f3ac17f2), with [Git Repo](https://github.com/venkatesannaveen/medium-articles).

- [Git-hub Stats real-time visualization](https://github.com/jstrieb/github-stats)

- [Making gif animation plots](https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30)
  
## To visualize data structure

- [json viewer](http://jsonviewer.stack.hu/)

- [Code Beautify](https://codebeautify.org)

### Deployed at [Macro Monitor](https://thanhqtran.github.io/macroeconomicmonitor/)
