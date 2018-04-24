#-- How to set 2 apps in Openshift
from flask import Flask
from bs4 import BeautifulSoup
import requests
import psycopg2
import os
application = Flask(__name__)

def connect_postgres():
    try:
        dbname = os.environ.get("POSTGRESQL_DBNAME","NOT FOUND")
        user =  os.environ.get("POSTGRESQL_USER","NOT FOUND")
        host =  os.environ.get("POSTGRESQL_HOST ","NOT FOUND")
        password= os.environ.get("POSTGRESQL_PASSWORD ","NOT FOUND")
        connect_str = "dbname={} user={} host={} password={}".format(dbname,user,host,password)
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
    return conn

def init_table():
    url = r"https://en.wikipedia.org/wiki/List_of_stations_of_the_Paris_M%C3%A9tro"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    connection = connect_postgres()
    cursor = connection.cursor()

    table = soup.find('table')

    data = []
    nbr_stations = 0
    for tr in table.findAll('tr'):

        index = 0
        station = ""
        lignes = []
        for td in tr.findAll('td')[::3]:
            for a in td.findAll('a'):
                if index == 0:
                    station = a.text
                    nbr_stations +=1
                else:
                    lignes.append(a.text)
                    #print(lignes)
            index += 1
            data.append([station, lignes])


    # extrait des infos
    for x in data:
        for t in x[1]:
            for i in t:
                try:
                    cursor.execute("""INSERT INTO metro_data (name,ligne) 
                           VALUES (%s,%s::integer)""", (x[0], i))
                except (Exception, psycopg2.DatabaseError) as error:
                    val = error
                connection.commit()
    return val


@application.route("/")
def hello():
    err = init_table()
    return 'il y a {} stations de metro  \n'.format(err)
if __name__ == "__main__":
    application.run()
