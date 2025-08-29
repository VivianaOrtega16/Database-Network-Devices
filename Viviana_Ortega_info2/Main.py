#from MySQLdb.constants.CR import NULL_POINTER 
# NULL_POINTER no existe en Python 3, lo reemplazamos por None
NULL_POINTER = None
from DatabaseConnector import DatabaseConnector 
from NetworkDevices import Company 

db = DatabaseConnector(user="root", password="")  # Change credentials 
db.connect() 
company = Company(NULL_POINTER, "ACME2", "Neiva") 
db.insert_company(company) 

list_companies = db.get_all_companies() 

for company in list_companies: 
    company.print_company() 

db.disconnect() 
