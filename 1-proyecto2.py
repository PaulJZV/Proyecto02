import requests
from tabulate import tabulate
import mysql.connector

    

URL = 'https://restcountries.com/v3.1/region/America'

response = requests.get(URL)

if response.status_code == 200:
    print('conexión a api exitosa')
    data = response.json()
    rows = []
    for dic_user in data:
        nombre = dic_user['name']['common'] + ' / ' + dic_user['name']['official']
        capital = dic_user['capital'][0]
        region = dic_user['region']
        populacion = dic_user['population']

        rows.append([nombre,capital,region,populacion])
        
    headers = ['Nombre','Capital','Region','Populacion']
    print(tabulate(rows,headers,tablefmt='grid'))
    
    # CARGAMOS DATA EN LA BASE DE DATOS
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='db_g6'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS country(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(255) NOT NULL,
            capital VARCHAR(255),
            region VARCHAR(255),
            populacion VARCHAR(100)
            );
            """
        )
        #INSERTAMOS LOS COUNTRIESS A LA BD
        for country in rows:
            cursor.execute(
                """
                insert into country(nombre,capital,region,populacion)
                values(%s,%s,%s,%s)
                """,
                country
            )
        connection.commit()
        connection.close()
        print(f' Registros importados a la base de datos')
    else:
        print('Error al conectarse a la base de datos')
else:
    print(f'error : {response.status_code}')