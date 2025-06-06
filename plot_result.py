import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results.csv", header=None, names=["Artist", "Year", "Count", "AvgPeak"], quotechar='"', skipinitialspace=True)

df["Year"] = df["Year"].astype(int)
df["AvgPeak"] = df["AvgPeak"].astype(float)

plt.figure(figsize=(12, 6))

for artist, group in df.groupby("Artist"):
    plt.plot(group["Year"], group["AvgPeak"], marker='o', label=artist)

plt.title("Average Peak Position per Year by Artist")
plt.xlabel("Year")
plt.ylabel("Average Peak Position (lower is better)")
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("average_peak_per_year.png")
