#from MySQLdb.constants.CR import NULL_POINTER 
# NULL_POINTER no existe en Python 3, lo reemplazamos por None
NULL_POINTER = None
from DatabaseConnector import DatabaseConnector 
from NetworkDevices import Company 
from NetworkDevices import Route
from NetworkDevices import Router
from NetworkDevices import NetworkDevice

db = DatabaseConnector(user="root", password="")  # Change credentials 
db.connect() 
#company = Company(NULL_POINTER, "Claro", "Bogota") 
#db.insert_company(company) 

"""list_companies = db.get_all_companies() 

for company in list_companies: 
    company.print_company() """

"""list_routers=db.get_routers_by_company(8)
for router in list_routers:
    router.print_router()"""
#consulta 2    
list_route=db.get_routing_table(2) 
for route in list_route:
    route.display_info()
#consulta 1
print("consulta 1")
list_empty_companies=db.get_companies_without_routers()
for company in list_empty_companies:
    company.print_company()
    
#consulta3
company_counts = db.get_company_device_counts()

# Imprimir resultados
print("Conteo de dispositivos por compañía:\n")
for company in company_counts:
    print(f"ID: {company['id']} | Nombre: {company['name']} | #Devices: {company['num_devices']}")

# consulta 5
interface, count = db.get_most_used_interface()
if interface:
    print(f"La interfaz más usada es '{interface}' con {count} usos.")
else:
    print("No hay rutas registradas en la base de datos.")
    
#consulta 6
avg_hops = db.get_average_hops_per_router()

    # Imprimir resultados
print("Promedio de saltos por router:")
for router_id, promedio in avg_hops.items():
    print(f"Router {router_id} -> promedio de {promedio:.2f} saltos")

db.disconnect() 
