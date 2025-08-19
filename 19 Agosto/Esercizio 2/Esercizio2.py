import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("19 Agosto\Esercizio 2\AirQualityUCI.csv", sep=";")
df = df.rename(columns=lambda x: x.strip())

df = df.replace(-200, np.nan)
df["NO2(GT)"] = pd.to_numeric(df["NO2(GT)"], errors = "coerce")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


df = df.dropna(subset=["NO2(GT)"])

daily_mean = df.groupby(df["Date"].dt.date)["NO2(GT)"].transform("mean")
df["AirQuality"] = np.where(df["NO2(GT)"] <= daily_mean, "buona", "scarsa")

df["dayofweek"] = df["Date"].dt.dayofweek
df["month"] = df["Date"].dt.month
df["day"] = df["Date"].dt.day

X = df[["NO2(GT)", "dayofweek", "month", "day"]]
y = df["AirQuality"]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42, stratify=y)

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)

print("Classification Report:")
print(classification_report(y_test,y_pred))

