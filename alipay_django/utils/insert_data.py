import sqlite3

conn = sqlite3.connect('db')

c = conn.cursor()

c.execute(
    "INSERT INTO demo_goods (goods_name, goods_price) VALUES ('华为手表', 1288);"
    "INSERT INTO demo_goods (goods_name, goods_price) VALUES ('天王手表', 369);"
    "INSERT INTO demo_goods (goods_name, goods_price) VALUES ('迪士尼手表', 151);"
    "INSERT INTO demo_goods (goods_name, goods_price) VALUES ('天梭瑞士手表', 1080);"
)

conn.commit()
conn.close()
