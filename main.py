from scraper import GloBirdScraper
from send_email import send_email
import polars as pl
from datetime import date, timedelta
import glob
import os
from time import sleep
from matplotlib import pyplot as plt
import html_css_formatter as html_format

def format_data(usage,charge):
    data = html_format.HEADER(
        f"{date.today() - timedelta(days = 1)}"
        )
    for i in range(len(usage)):
        if "*" in usage[i]: u = f"<strong>{usage[i]}</strong>"
        else: u = usage[i]

        if "*" in charge[i]: c = f"<strong>{charge[i]}</strong>"
        else: c = charge[i]

        data += f"""
        <tr>
            <td>{i}</td>
            <td>{u}</td>
            <td>{c}</td>
        </tr>"""
    data += html_format.FOOTER()
    return data

def min_to_hourly(data):
    hourly_data = []
    for i in range(0, len(data), 12):
        hourly_data.append(sum(data[i:i+12]))
    return hourly_data

def std_dev(data):
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance ** (1/2)

def scrapeSite():
    for csv_file in glob.glob("*.csv"):
        os.remove(csv_file)
    scraper = GloBirdScraper()
    scraper.getCSV()
    
def main(scrape=True):
    if scrape: scrapeSite()
    try:
        df = pl.read_csv(f"summary-{date.today()}.csv")
    except:
        print("Error! File not found!")
        return

    target_date = (date.today() - timedelta(days=2)).strftime("%d-%b-%Y")
    df = df.filter(pl.col("Date") != target_date)

    usages = min_to_hourly(df.select(pl.col("Usage (kWh)")).to_series().to_list())
    usage_std = std_dev(usages)
    usage_mean = sum(usages) / len(usages)

    charge = min_to_hourly(df.select(pl.col("Wholesale Price (Cents/kWh, Gst incl)")).to_series().to_list())
    charge_std = std_dev(charge)
    charge_mean = sum(charge) / len(charge)

    #print(f"U: {usage_mean:.2f} ± {usage_std:.2f}")
    #print(f"C: {charge_mean:.2f} ± {charge_std:.2f}")

    for i,u in enumerate(usages):
        if u > usage_mean + usage_std:
            usages[i] = f"{u:.2f}*"
        else: 
            usages[i] = f"{u:.2f}"

    for i,c in enumerate(charge):
        if c > charge_mean + charge_std:
            charge[i] = f"{c:.2f}*"
        else: 
            charge[i] = f"{c:.2f}"


    #print(usages)
    #print(charge)

    formatted = format_data(usages, charge)

    send_email(
        f"GloBird Data Summary - {date.today()}",
        formatted,
        os.getenv("EMAIL_TO"),
    )

main(scrape=True)