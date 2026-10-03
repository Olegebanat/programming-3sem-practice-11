import pandas as pd

N = 20

pages = pd.Series({
    "Dune": 412,
    "Neuromancer": 271,
    "Hyperion": 482,
    "Solaris": 204,
    "Foundation": 255
})

print(pages)
print(pages.loc["Hyperion"])
print(pages.iloc[0])
print(pages.loc["Neuromancer":"Solaris"])
print(pages.loc[["Dune", "Foundation"]])

print(pages.mean())
print(pages.max())
print(pages.idxmax())

mask = pages > 50 * N
print(mask)
print(pages[mask])
march = pd.Series({
    "Dune": 12.0,
    "Hyperion": 5.0,
    "Solaris": 8.0
})

april = pd.Series({
    "Hyperion": 7.0,
    "Dune": 10.0,
    "Ubik": 4.0
})

sales_sum = march + april

print(sales_sum)
print(sales_sum.isna().sum())
print(sales_sum.dropna())
print(march.add(april, fill_value=0))
books = pd.DataFrame({
    "title": ["Dune", "Neuromancer", "Hyperion", "Solaris", "Foundation", "Ubik"],
    "genre": ["sci-fi", "cyberpunk", "sci-fi", "classic", "classic", "cyberpunk"],
    "year": [1965, 1984, 1989, 1961, 1951, 1969],
    "pages": [412, 271, 482, 204, 255, 224],
    "price": [320.0, 275.5, 410.0, 189.9, 240.0, 295.0]
})

print(books)
print(books.shape)
print(books.columns)
print(books.dtypes)
books.info()
print(books.describe())
print(books.head(2))
print(books.tail(2))
print(type(books["price"]))
print(type(books[["price"]]))

print(books[["title", "price"]])

print(books.loc[2])
print(books.iloc[0])

print(books.loc[1:3, ["title", "pages"]])
print(books.iloc[:3, :2])

print(books.loc[4, "price"])
print(books.iloc[4, 4])
orders = pd.read_csv(
    "orders.csv",
    comment="#",
    sep=";",
    decimal=",",
    na_values="-",
    dtype={"code": "str"},
    parse_dates=["date"]
)

print(orders)
print(orders.dtypes)
print(orders.shape)
print(orders.isna().sum())
orders["copies"] = orders["copies"].fillna(0).astype(int)
orders["revenue"] = orders["copies"] * orders["price"]

print(orders)
print(orders["revenue"].sum())

print(
    orders.nlargest(3, "revenue")[["date", "title", "revenue"]]
)
mask = (orders["genre"] == "sci-fi") & (orders["revenue"] > 100 * N)

print(mask.sum())
print(orders.loc[mask, ["date", "title", "revenue"]])
print(orders["genre"].value_counts())