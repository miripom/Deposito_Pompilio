import pandas as pd

df = pd.read_csv("19 Agosto\Esercizio 1\PJME_hourly.csv", parse_dates=["Datetime"])

print(df.head())

df["Date"] = df["Datetime"].dt.date
df["Week"] = df["Datetime"].dt.isocalendar().week

df["Daily_Mean"] = df.groupby("Date")["PJME_MW"].transform("mean")

df["Weekly_Mean"] = df.groupby("Week")["PJME_MW"].transform("mean")

df["Daily_Class"] = (df["PJME_MW"] > df["Daily_Mean"]).map({True:"Alto", False:"Basso"})
df["Weekly_Class"] = (df["PJME_MW"] > df["Weekly_Mean"]).map({True: "Alto", False:"Basso"})

print(df.head())