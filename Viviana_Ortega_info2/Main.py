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
print("CONSULTA: SELECT nd.id AS device_id, nd.device_name AS device_name,c.id AS company_id, c.name AS company_name FROM NetworkDevice nd JOIN Company c ON nd.company_id = c.id")
print("-------------------------------------------------------")
devices = db.get_devices_with_companies()
for d in devices:
    print(f"Dispositivo {d['device_name']} (ID {d['device_id']}) pertenece a la compañía {d['company_name']} (ID {d['company_id']})")
print("-------------------------------------------------------")

#consulta 2 
print("CONSULTA: SELECT * FROM Route WHERE router_id = %s")
print("-------------------------------------------------------")   
list_route=db.get_routing_table(2) 
for route in list_route:
    route.display_info()
print("-------------------------------------------------------")
#consulta 3
print("CONSULTA: SELECT c.id, c.name, c.city FROM Company c WHERE c.id NOT IN (SELECT nd.company_id FROM NetworkDevice nd INNER JOIN Router r ON nd.id = r.network_id")
print("-------------------------------------------------------")
list_empty_companies=db.get_companies_without_routers()
for company in list_empty_companies:
    company.print_company()
print("-------------------------------------------------------")
#consulta 4
print("CONSULTA: SELECT c.id, c.name, COUNT(nd.id) AS num_devices FROM Company c LEFT JOIN NetworkDevice nd ON c.id = nd.company_id GROUP BY c.id, c.name")
print("-------------------------------------------------------")
company_counts = db.get_company_device_counts()

# Imprimir resultados
print("Conteo de dispositivos por compañía:\n")
for company in company_counts:
    print(f"ID: {company['id']} | Nombre: {company['name']} | #Devices: {company['num_devices']}")
print("-------------------------------------------------------")

# consulta 5
print("CONSULTA: SELECT interface, COUNT(*) as usage_count FROM Route GROUP BY interface ORDER BY usage_count DESCLIMIT 1")
print("-------------------------------------------------------")
interface, count = db.get_most_used_interface()
if interface:
    print(f"La interfaz más usada es '{interface}' con {count} usos.")
else:
    print("No hay rutas registradas en la base de datos.")
print("-------------------------------------------------------")

#consulta 6
print("CONSULTA: SELECT r.id AS router_id, AVG(rt.metric) AS avg_hops FROM Router r JOIN Route rt ON r.id = rt.router_id GROUP BY r.id")
print("-------------------------------------------------------")
avg_hops = db.get_average_hops_per_router()

    # Imprimir resultados
print("Promedio de saltos por router:")
for router_id, promedio in avg_hops.items():
    print(f"Router {router_id} -> promedio de {promedio:.2f} saltos")
print("-------------------------------------------------------")
#dos consultas propuestas 

# consulta 7
print("CONSULTA: SELECT * FROM Mac WHERE switch_id = %s")
print("-------------------------------------------------------")
macs = db.get_mac_table(6)
    
# Imprimir resultados
if macs:
    print(f"MACs del switch {6}:")
    for m in macs:
        print(f"ID: {m.mac_id}, MAC: {m.mac_address}, Puerto: {m.port}")
else:
    print(f"No se encontraron MACs para el switch {6}")
print("-------------------------------------------------------")
# consulta 8
print("SELECT port, COUNT(*) as usage_count FROM Mac WHERE switch_id = %s GROUP BY port ORDER BY usage_count DESC LIMIT 1")
print("-------------------------------------------------------")
#encontrar el puerto mas usado 
port, usage_count = db.get_most_used_port(6)

if port is not None:
    print(f"El puerto más usado del switch {6} es {port} con {usage_count} MACs asociadas.")
else:
    print(f"No se encontraron MACs para el switch {6}.")
print("-------------------------------------------------------")

db.disconnect() 
