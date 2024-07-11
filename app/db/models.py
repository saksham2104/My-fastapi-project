from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

names = Table(
    "names",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100))
)
