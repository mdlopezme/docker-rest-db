import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(user=db_user,password=db_pass,host=db_host)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE Triton_Gallery;")
except:
    print('Database already exists, resetting table Gallery_Details')

cursor.execute("USE Triton_Gallery;")
cursor.execute("DROP TABLE IF EXISTS Gallery_Details;")

try:
    cursor.execute("""
        CREATE TABLE Gallery_Details (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(50) NOT NULL,
            owner       VARCHAR(50) NOT NULL,
            height      INT NOT NULL,
            age         INT NOT NULL
        );
    """)
except RuntimeError as err:
    print('RuntimeError: {err}')

query = "INSERT INTO Gallery_Details (name,owner,height,age) VALUES (%s,%s,%s,%s)"
values = [
    ('Geisel-1.jpg','Terrel Gilmore', 163, 45),
    ('Geisel-2.jpg','Sila Mann', 189, 51),
    ('Geisel-3.jpg','Nyle Hendrix', 152, 27),
    ('Geisel-4.jpg','Axel Horton', 176, 21),
    ('Geisel-5.jpg','Courtney Mcneil', 172, 64)
]

cursor.executemany(query,values)
db.commit()

db.close()