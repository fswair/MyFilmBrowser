from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from random import shuffle, randint
from pandas import DataFrame
from database import db

"""
[input("Enter movie name: "),input("Your score: "),input("Enter movie genre: "),input("Words associated with movie: ")]
"""
class InvalidInput(Exception):
    pass

class Input:
    def ask(self, type_: type = str, message: str = "What's up?"):
        try:
            data = type_.__call__(input(message))
            return data
        except ValueError:
            raise InvalidInput("Invalid input. Please try again.")

class Films:
    """
    This class is used to manage films in the database.
    
    Methods:
    - add: Add a new film to the database.
    - remove: Remove a film from the database.
    - drop: Drop the table from the database.
    - list_films: List all films in the database.
    - restore_deleted_films: Restore all deleted films.
    - show_deleted_films: Show all deleted films.
    - get_films: Get all films from the database.
    - suggest: Suggest a list of films from IMDb.
    
    Returns:
    - DataFrame: A pandas DataFrame object.
    - None: If the method does not return anything."""
    def __init__(self):
        self.input = Input()
    
    def add(self, name: str, rate: str, kind: str, related_words: str | list[str]):
        film_id = randint(100000, 999999)
        formatted_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        if isinstance(related_words, list):
            related_words = ", ".join(related_words)
        db.insert('films', {
            'id': film_id,
            'is_active': 1,
            'name': name,
            'rate': rate,
            'kind': kind,
            'related_words': related_words,
            'time': formatted_time
        })
    
    def delete(self, film_id: int):
        films = db.select("films")
        for film in films:
            if film_id == film.get("id"):
                db.update("films", {"is_active": 0}, {"id": film_id})
                break
    
    def drop(self):
        db.drop("films")
    
    def list_films(self):
        films = db.select("films")
        data = {
        "id": [],
        "name":[],
        "rate":[],
        "kind":[],
        "related":[],
        "time":[]

        }
        for film_id, film in enumerate(films):
            data["id"].append(film.get("id"))
            data["name"].append(film.get("name"))
            data["rate"].append(film.get("rate"))
            data["kind"].append(film.get("kind"))
            data["related"].append(film.get("related_words"))
            data["time"].append(film.get("time"))
        df = DataFrame(data)
        return df
    
    def restore_deleted_films(self):
        films = db.select("films")
        for film in films:
            if film.get("is_active") == 0:
                db.update("films", {"is_active": 1}, {"id": film.get("id")})
    
    def show_deleted_films(self):
        deleted_films = db.select("films")
        for i, film in enumerate(deleted_films):
            print(f"{i+1}. {film.get('name')}", end="\n********************")
    
    def get_films(self, year: int | str = None):
        films = db.select("films")
        fdata = {
        "id": [],
        "name":[],
        "rate":[],
        "kind":[],
        "related":[],
        "time":[]

        }
        for i, film in enumerate(films):
            time_data = film.get("time")
            expected_year = year or datetime.now().today().year
            if str(expected_year) == [time_data[z:z+4] for z in range(len(time_data))][6]:
                    fdata["id"].append(film.get("id"))
                    fdata["name"].append(film.get("name"))
                    fdata["rate"].append(film.get("rate"))
                    fdata["kind"].append(film.get("kind"))
                    fdata["related"].append(film.get("related_words"))
                    fdata["time"].append(film.get("time"))
            
        df = DataFrame(fdata)
        return df
    
    def suggest(self, piece: int = 10, m_max: int = 50):
        soup = BeautifulSoup(get("https://www.imdb.com/list/ls075103447/?st_dt=&sort=user_rating,desc&mode=detail&page=1").content, "html.parser")
        names = [name[:name.find("(")] for name in [x.text.replace("\n","")[x.text.replace("\n","").find(".")+1:] for x in soup.find_all("h3",{"class":"lister-item-header"})]][:m_max]
        rates = [x.text.replace("\n", "") for x in soup.find_all("div", {"class":"ipl-rating-star small"})][:m_max]
        genres  = [x.text.replace("\n", "").replace(" ","") for x in soup.find_all("span", {"class":"genre"})][:m_max]
        years = [x.text.replace("\n", "").replace(" ","").replace("Video","").replace("TVMovie","") for x in soup.find_all("span", {"class":"lister-item-year text-muted unbold"})][:m_max]

        ids = list(range(m_max))
        shuffle(ids)
        ids = ids[:piece]
        names, rates, genres, years = [], [], [], []


        for _id in ids:
            names.append(names[_id])
            rates.append(rates[_id])
            genres.append(genres[_id])
            years.append(years[_id])

        df = DataFrame({
            "name": names,
            "rate": rates,
            "genres": genres,
            "year": years
        })

        return df

films = Films()

homepage_message = \
"""Welcome to the film database.
What do you want to do?

1. Add a new film
2. Remove a film
3. Drop the table
4. List all films
5. Restore deleted films
6. Show deleted films
7. Get films by current year
8. Get films by a specific year
9. Suggest films
10. Suggest films by a specific number
11. Exit the program
"""
def main():
    match (films.input.ask(type_=int, message=f"{homepage_message}\n\nYour choice: ")):
        case 1:
            name  =  films.input.ask(message="Enter the name of the film: ")
            rate  =  films.input.ask(message="Enter the rate of the film: ")
            kind  =  films.input.ask(message="Enter the kind of the film: ")
            words =  films.input.ask(message="Enter the related words of the film: ")
            films.add(name, rate, kind, words)
        case 2:
            film_id = films.input.ask(type_=int, message="Enter the id of the film: ")
            films.delete(film_id)
        case 3:
            films.drop()
        case 4:
            print(films.list_films())
        case 5:
            films.restore_deleted_films()
        case 6:
            films.show_deleted_films()
        case 7:
            print(films.get_films())
        case 8:
            year = films.input.ask(type_=int, message="Enter the year: ")
            print(films.get_films(year))
        case 9:
            print(films.suggest())
        case 10:
            piece = films.input.ask(type_=int, message="Enter the number of films to suggest: ")
            print(films.suggest(piece))
        case 11:
            print("Goodbye!")
            return
        case _:
            print("Invalid option!")
    verify = films.input.ask(message="Wanna see the control menu again? (Y/n): ")
    if "y" in verify.lower():
        main()
    else:
        print("Goodbye!")
        return

if __name__ == "__main__":
    main()