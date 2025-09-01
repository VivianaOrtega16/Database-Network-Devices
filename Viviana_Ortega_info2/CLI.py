from DatabaseConnector import DatabaseConnector

db = DatabaseConnector(
    host="localhost",
    user="root",
    password="",   # tu clave real
    database="mynetworkdb"  # tu base real
)

if db.connection:
    print("Conexión OK")
else:
    print(" Conexión fallida")
from DatabaseConnector import DatabaseConnector
from MainCLI import CLI

def main():
    db = DatabaseConnector(
        host="localhost",
        user="root",
        password="",    
        database="mynetworkdb"    
    )
    cli = CLI(db)
    cli.run()
    db.close()

if __name__ == "__main__":
    main()

