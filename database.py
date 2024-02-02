from MentoDB import Mento, MentoConnection
from models import Films

# Create a new MentoConnection object
connection = MentoConnection()
db = Mento(connection)

# Create a new table
db.create('films', model=Films)