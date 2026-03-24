"""
NSO (Vietnam General Statistics Office) Excel Data Scraper
Downloads and parses Excel files from nsdp.nso.gov.vn
"""

import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Links from excel_files.txt ────────────────────────────────────────────────
NSO_LINKS = {
    "GDP": "http://nsdp.nso.gov.vn/GSO-chung/Tu%E1%BA%A5n%20Anh/excel%20chung/GDP_VNM.xlsx",
    "CPI": "http://nsdp.nso.gov.vn/GSO-chung/Tu%E1%BA%A5n%20Anh/excel%20chung/CPI_VNM.xlsx",
    "IIP": "http://nsdp.nso.gov.vn/GSO-chung/Tu%E1%BA%A5n%20Anh/excel%20chung/IIP_VNM.xlsx",
    "LMI": "http://nsdp.nso.gov.vn/GSO-chung/Tu%E1%BA%A5n%20Anh/excel%20chung/LMI_VNM.xlsx",
    "PPI": "http://nsdp.nso.gov.vn/GSO-chung/Tu%E1%BA%A5n%20Anh/excel%20chung/PPI_VNM.xlsx",
}


# ── Download ──────────────────────────────────────────────────────────────────
def download_excel(url: str, save_dir: str = "data") -> bytes:
    """Download an Excel file from a URL, cache it locally."""
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, url.split("/")[-1])

    if os.path.exists(filename):
        print(f"[cache] {filename}")
        with open(filename, "rb") as f:
            return f.read()

    print(f"[download] {url}")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(filename, "wb") as f:
        f.write(r.content)
    print(f"[saved]  {filename}  ({len(r.content):,} bytes)")
    return r.content


# ── Parse ─────────────────────────────────────────────────────────────────────
def parse_nso_sheet(content: bytes, sheet_name: str) -> pd.DataFrame:
    """
    Parse one sheet of an NSO Excel file into a tidy DataFrame.

    The NSO format:
      Rows 0-8  : metadata / blank
      Row 9     : header – col0='Country code', col1='Descriptor',
                  col2='INDICATOR', col3='Descriptor Vietnamese',
                  col4='FREQ', col5='BASE_PER', col6+: period labels
      Row 10    : section title (no data)
      Row 11+   : data rows

    Returns a DataFrame with columns:
        indicator, descriptor, descriptor_vn, freq, base_per, <period cols>
    """
    xl = pd.ExcelFile(io.BytesIO(content))
    raw = xl.parse(sheet_name, header=None)

    # locate the header row (contains 'INDICATOR' or 'Country code')
    header_row = None
    for i, row in raw.iterrows():
        if row.astype(str).str.contains("INDICATOR|Country code", na=False).any():
            header_row = i
            break
    if header_row is None:
        raise ValueError(f"Could not find header row in sheet '{sheet_name}'")

    header = raw.iloc[header_row]

    # period columns: everything after BASE_PER that looks like '2004-Q1' or '2004'
    period_cols = []
    for col_idx, val in enumerate(header):
        s = str(val)
        if "-" in s and s[:4].isdigit():
            period_cols.append((col_idx, s))

    # data rows start at header_row + 2 (skip the section-title row)
    data_start = header_row + 2
    data_rows = []

    for _, row in raw.iloc[data_start:].iterrows():
        indicator = str(row.iloc[0]).strip()
        if indicator in ("nan", "", "NaN"):
            continue
        descriptor    = str(row.iloc[1]).strip()
        descriptor_vn = str(row.iloc[3]).strip()
        freq          = str(row.iloc[4]).strip()
        base_per      = str(row.iloc[5]).strip()

        values = {}
        for col_idx, period in period_cols:
            val = row.iloc[col_idx]
            try:
                values[period] = float(val)
            except (TypeError, ValueError):
                values[period] = float("nan")

        data_rows.append({
            "indicator":     indicator,
            "descriptor":    descriptor,
            "descriptor_vn": descriptor_vn,
            "freq":          freq,
            "base_per":      base_per,
            **values,
        })

    return pd.DataFrame(data_rows)


def get_series(df: pd.DataFrame, indicator: str) -> pd.Series:
    """Return a time-indexed pd.Series for a given indicator code."""
    row = df[df["indicator"] == indicator]
    if row.empty:
        raise KeyError(f"Indicator '{indicator}' not found.")
    meta_cols = ["indicator", "descriptor", "descriptor_vn", "freq", "base_per"]
    period_data = row.drop(columns=meta_cols).iloc[0]
    period_data.index = pd.PeriodIndex(period_data.index, freq="Q")
    return period_data.astype(float)


# ── Plot ──────────────────────────────────────────────────────────────────────
def plot_gdp(df: pd.DataFrame, output_path: str = "data/gdp_plot.png"):
    """Plot Vietnam quarterly real GDP and nominal GDP by major sector."""

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle("Vietnam – Quarterly GDP (NSO)", fontsize=16, fontweight="bold")

    # Panel 1: Real GDP total
    ax1 = axes[0]
    try:
        series = get_series(df, "NGDP_R_PA_XDC").dropna()
        ax1.plot(series.index.to_timestamp(), series.values,
                 color="#1f77b4", linewidth=2, marker="o", markersize=3)
        ax1.set_title("Real GDP – Total (chained prices, VND billions)", fontsize=13)
        ax1.set_ylabel("VND Billions")
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis="x", rotation=45)
    except KeyError as e:
        ax1.text(0.5, 0.5, str(e), ha="center", va="center", transform=ax1.transAxes)

    # Panel 2: Nominal GDP by sector
    ax2 = axes[1]
    sector_indicators = {
        "NGDPVA_R_ISIC4_A_XDC":       "Agriculture",
        "VNM_NGDPVA_R_ISIC4_BTE_XDC": "Industry",
        "NGDPVA_R_ISIC4_F_XDC":       "Construction",
        "VNM_NGDPVA_R_ISIC4_GTT_XDC": "Services",
    }
    for code, label in sector_indicators.items():
        try:
            s = get_series(df, code).dropna()
            ax2.plot(s.index.to_timestamp(), s.values, linewidth=1.8,
                     marker="o", markersize=2, label=label)
        except KeyError:
            pass

    ax2.set_title("Real GDP by Sector (chained prices, VND billions)", fontsize=13)
    ax2.set_ylabel("VND Billions")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax2.legend(loc="upper left", fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[saved] {output_path}")
    plt.show()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    content = download_excel(NSO_LINKS["GDP"])

    xl = pd.ExcelFile(io.BytesIO(content))
    print("Sheets:", xl.sheet_names)

    # Parse quarterly sheet
    df_q = parse_nso_sheet(content, "Dataset_Q")
    print(f"\nParsed {len(df_q)} indicators from Dataset_Q")
    print("Sample indicators:")
    print(df_q[["indicator", "descriptor"]].head(15).to_string(index=False))

    # Save to CSV
    df_q.to_csv("data/GDP_quarterly.csv", index=False)
    print("\n[saved] data/GDP_quarterly.csv")

    # Plot
    plot_gdp(df_q)
