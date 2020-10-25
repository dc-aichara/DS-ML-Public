from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://results.eci.gov.in/pc/en/partywise/index.htm"
content = requests.get(url).content
soup = BeautifulSoup(content, "html.parser")
table = soup.find_all("tr")

A = []
for a in table:
    A.append(a)

last_update = A[-1].text

A = A[13 : len(A) - 6]

list1 = []
for i in range(len(A)):
    a = [td.text for td in A[i].find_all("td")]
    list1.append(a)

df = pd.DataFrame(list1)
df.columns = ["party", "won", "leading", "total"]

col_int = df.columns.values.tolist()[1:]

for col in col_int:
    df[col] = df[col].astype(int)

df = df.sort_values(by="total", ascending=False).reset_index(drop=True)
print(df[:10])

winner_party = df[df["total"] == df["total"].max()]["party"].values[0]
if df["total"].max() >= 272:
    print(
        "Winning party : ",
        winner_party,
        "with {} seats".format(df["total"].max()),
        last_update,
    )
