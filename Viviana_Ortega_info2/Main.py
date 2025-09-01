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

#--------------CONSULTAS---------------------
#consulta 1
devices = db.get_devices_with_companies()
for d in devices:
    print(f"Dispositivo {d['device_name']} (ID {d['device_id']}) pertenece a la compañía {d['company_name']} (ID {d['company_id']})")

#consulta 2    
list_route=db.get_routing_table(2) 
for route in list_route:
    route.display_info()
    
#consulta 3
list_empty_companies=db.get_companies_without_routers()
for company in list_empty_companies:
    company.print_company()
    
#consulta 4
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

#dos consultas propuestas 

# consulta 7
macs = db.get_mac_table(6)
    
# Imprimir resultados
if macs:
    print(f"MACs del switch {6}:")
    for m in macs:
        print(f"ID: {m.mac_id}, MAC: {m.mac_address}, Puerto: {m.port}")
else:
    print(f"No se encontraron MACs para el switch {6}")
# consulta 8
#encontrar el puerto mas usado 
port, usage_count = db.get_most_used_port(6)

if port is not None:
    print(f"El puerto más usado del switch {6} es {port} con {usage_count} MACs asociadas.")
else:
    print(f"No se encontraron MACs para el switch {6}.")

db.disconnect() 
