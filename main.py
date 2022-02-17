from datetime import datetime as d
from requests import get
from bs4 import BeautifulSoup
from random import shuffle, randint as r
from pandas import DataFrame as frame
import time as t
import sqlite3 as sql



con = sql.connect("database.sql", check_same_thread=False)
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS films (id int, is_active int, name text, rate text, kind text, related_words text, time text)")
con.commit() 


class Films():
    def addFilm(self):
        name, rate, kind, related_words = [input("Enter movie name: "),input("Your score: "),input("Enter movie genre: "),input("Words associated with movie: ")]
        id = r(10000,999999)
        ftime = d.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute(f"INSERT INTO films values ({id},{1},'{name}','{rate}','{kind}','{related_words}','{ftime}')")
        con.commit()
    def removeFilm(self, id):
        cursor.execute("SELECT f.id from films f")
        self.veriler = cursor.fetchall()
        for x in self.veriler:
            if id in x:
                cursor.execute(f"UPDATE films SET is_active=0 WHERE id={id}")
                con.commit()
    def deleteDb(self):
        cursor.execute("DROP TABLE films")
    
    def listAllData(self):
        cursor.execute("SELECT * FROM films where is_active=1")
        veriler = cursor.fetchall()
        data = {
        "id": [],
        "name":[],
        "rate":[],
        "kind":[],
        "related":[],
        "time":[]

        }
        for x in range(len(veriler)):
            data["id"].append(veriler[x][0])
            data["name"].append(veriler[x][2])
            data["rate"].append(veriler[x][3])
            data["kind"].append(veriler[x][4])
            data["related"].append(veriler[x][5])
            data["time"].append(veriler[x][6])
        df = frame(data)
        print(df)
    def addRemovedFilms(self):
        cursor.execute(f"UPDATE films SET is_active={1} where is_active=0")
        con.commit()
    def showRemovedFilms(self):
        cursor.execute("SELECT f.name from films f")
        silinenler = cursor.fetchall()
        for x in silinenler:
            print(x)
    def filmsIHaveWatchedInThisYear(self):
        cursor.execute(f"SELECT * from films where is_active=1")
        datas = cursor.fetchall()
        fdata = {
        "id": [],
        "name":[],
        "rate":[],
        "kind":[],
        "related":[],
        "time":[]

        }
        for x in range(len(datas)):
            time_data = datas[x][6]
            if str(d.now().today().year) == [time_data[z:z+4] for z in range(len(time_data))][6]:
                    fdata["id"].append(datas[x][0])
                    fdata["name"].append(datas[x][2])
                    fdata["rate"].append(datas[x][3])
                    fdata["kind"].append(datas[x][4])
                    fdata["related"].append(datas[x][5])
                    fdata["time"].append(datas[x][6])
            
        df = frame(fdata)
        print(df)
    def filmsIHaveWatchedInXYear(self):
        year = input("Which year would you like to see data for?\n")    
        cursor.execute(f"SELECT * from films where is_active=1")
        datas = cursor.fetchall()
        data = {
        "id": [],
        "name":[],
        "rate":[],
        "kind":[],
        "related":[],
        "time":[]

        }
        for x in range(len(datas)):
            time_data = datas[x][6]
            if str(year) == [time_data[z:z+4] for z in range(len(time_data))][6]:
                    data["id"].append(datas[x][0])
                    data["name"].append(datas[x][2])
                    data["rate"].append(datas[x][3])
                    data["kind"].append(datas[x][4])
                    data["related"].append(datas[x][5])
                    data["time"].append(datas[x][6])
            
        df = frame(data)
        print(df)

    def suggestFilms(self):
        soup = BeautifulSoup(get("https://www.imdb.com/list/ls075103447/?st_dt=&sort=user_rating,desc&mode=detail&page=1").content, "html.parser")

        names = [name[0:name.find("(")] for name in [x.text.replace("\n","")[x.text.replace("\n","").find(".")+1:] for x in soup.find_all("h3",{"class":"lister-item-header"})]][0:50]
        rates = [x.text.replace("\n", "") for x in soup.find_all("div", {"class":"ipl-rating-star small"})][0:50]
        genres  = [x.text.replace("\n", "").replace(" ","") for x in soup.find_all("span", {"class":"genre"})][0:50]
        years = [x.text.replace("\n", "").replace(" ","").replace("Video","").replace("TVMovie","") for x in soup.find_all("span", {"class":"lister-item-year text-muted unbold"})][0:50]


        indisler = [x for x in range(50)]
        shuffle(indisler)
        indisler = indisler[0:10]
        n,r,g,y = [],[],[],[]


        for x in indisler:
            n.append(names[x])
            r.append(rates[x])
            g.append(genres[x])
            y.append(years[x])

        df = frame({
            "name":n,
            "rate":r,
            "genres":g,
            "year":y
        })

        print(df)
films = Films()

while True:
    print(f"\n{40*'-'}\n\nSelect the action you want to do....\n0) Exit Program\n1) Add Movies\n2) Delete Movies\n3) Data Listing\n4) Restore Removed Movies\n5) Database Cleanup\n\nFilters:\n\t6 - What did I watch this year?\n\t7 - What time did I watch?\nI wonder what I should watch?\n\t8 - Recommend Random Movies (IMDb)\n")
    secim=input("")
    match int(secim):
        case 1:
            films.addFilm()
        case 2:
            films.listAllData()
            t.sleep(2)
            films.removeFilm(id=int(input("Type and enter ID of film you want to remove: ")))
        case 3:
            films.listAllData()
        case 4:
            films.addRemovedFilms()            
        case 5:
            films.deleteDb()
        case 6:
            films.filmsIHaveWatchedInThisYear()
        case 7:
            films.filmsIHaveWatchedInXYear()
        case 8:
            films.suggestFilms()
        case 0:
            quit()
    t.sleep(4)  
