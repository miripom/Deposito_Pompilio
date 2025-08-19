import pandas as pd

df = pd.read_csv("19 Agosto\Esercizio 1\PJME_hourly.csv", parse_dates=["Datetime"])

print(df.head())

df["Date"] = df["Datetime"].dt.date

df["Daily_Mean"] = df.groupby("Date")["PJME_MW"].transform("mean")

df["Class"] = (df["PJME_MW"] > df["Daily_Mean"]).map({True:"Alto", False:"Basso"})

print(df.head())