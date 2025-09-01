import mysql.connector 
from mysql.connector import Error 
from NetworkDevices import Company 
from NetworkDevices import Router 
from NetworkDevices import Route 
from NetworkDevices import Modem
from NetworkDevices import Switch
from NetworkDevices import Mac
from NetworkDevices import NetworkDevice

"""self.host = host 
        self.user = user 
        self.password = password 
        self.database = database 
        self.connection = None """
        
"""try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(" Conexión exitosa a la base de datos")
        except mysql.connector.Error as err:
            print(f" Error al conectar a la base de datos: {err}")
            self.connection = None
            self.cursor = None"""

class DatabaseConnector: 
    def __init__(self, host="localhost", user="root", password="", database="mynetworkdb"): 
        self.host = host 
        self.user = user 
        self.password = password 
        self.database = database 
        self.connection = None
     
     
        
    def connect(self): 
        try: 
            self.connection = mysql.connector.connect( 
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database 
            ) 
            if self.connection.is_connected(): 
                print("Connected to MySQL Database") 
        except Error as e: 
            print(f"Error: {e}") 

    def disconnect(self): 
        if self.connection: 
            self.connection.close() 
            print("Disconnected from MySQL Database") 

    def execute_query(self, query, params=None): 
        try: 
            cursor = self.connection.cursor() 
            cursor.execute(query, params) 
            self.connection.commit() 
            return cursor.lastrowid 
        except Error as e: 
            print(f"Error: {e}") 
            
    def fetch_query(self, query, params=None): 
        try: 
            cursor = self.connection.cursor(dictionary=True) 
            cursor.execute(query, params) 
            return cursor.fetchall() 
        except Error as e: 
            print(f"Error ejecutando query: {query} con params {params}") 
            print(f"Error: {e}") 
            return []

            
    


    def get_all_companies(self): 
        query = "SELECT * FROM Company" 
        companies_data = self.fetch_query(query) 
        companies = [Company(company["id"], company["name"], company["city"]) for company in companies_data] 
        for company in companies: 
            routers = self.get_routers_by_company(company.company_id) 
            for router in routers: 
                routes = self.get_routing_table(router.id) 
                router.add_routes(routes) 
                company.add_router(router) 
            modems = self.get_modems_by_company(company.company_id)
            switches = self.get_switches_by_company(company.company_id)
            for switch in switches:
                macs=self.get_mac_table(switch.switch_id)
                switch.add_mac_entries(macs)
                company.add_switch(switch)
        return companies 
      

        
        #-------------anexos 8
    def get_modems_by_company(self, company_id):
        query = """
            SELECT m.modem_id, m.network_id AS networkdevice_id, nd.device_name, nd.manufacturer, nd.model
            FROM Modem m
            JOIN NetworkDevice nd ON m.network_id = nd.id
            WHERE nd.company_id = %s"""
        
        modems_data = self.fetch_query(query, (company_id,))
        
        modems = [
            Modem(
                modem["modem_id"],  # id del modem
                modem["device_name"],
                modem["manufacturer"],
                modem["model"]
            ) for modem in modems_data
        ]
        return modems
    def get_switches_by_company(self, company_id):
        query = """
            SELECT s.switch_id, s.network_id AS networkdevice_id, nd.device_name, nd.manufacturer, nd.model
            FROM Switch s
            JOIN NetworkDevice nd ON s.network_id = nd.id
            WHERE nd.company_id = %s"""
        
        switches_data = self.fetch_query(query, (company_id,))
        
        switches = [
            Switch(
                switch["switch_id"],  # id del switch
                switch["device_name"],
                switch["manufacturer"],
                switch["model"]
            ) for switch in switches_data
        ]
        return switches

#this is work acoord hope, his id is of the table router , not from networkdevice        
    def get_routers_by_company(self, company_id):
    
        query = """
            SELECT r.id, r.network_id AS networkdevice_id, nd.device_name, nd.manufacturer, nd.model
            FROM Router r
            JOIN NetworkDevice nd ON r.network_id = nd.id
            WHERE nd.company_id = %s"""
        
        routers_data = self.fetch_query(query, (company_id,))
        
        routers = [
            Router(
                router["id"],# este es el id del router , se ecogio por preferencia para las rutas 
                router["device_name"],
                router["manufacturer"],
                router["model"]
            ) for router in routers_data
        ]
        return routers
    def get_mac_table(db, switch_id):
        query = "SELECT * FROM mac WHERE switch_id = %s"
        mac_data = db.fetch_query(query, (switch_id,))
        
        mac_entries = [
            Mac(
                mac["mac_id"],
                mac["mac_address"],
                mac["port"]
            )
            for mac in mac_data
        ]
        return mac_entries



#---------consulta 1
    def get_devices_with_companies(self):
        query = """
            SELECT nd.id AS device_id, nd.device_name AS device_name,
                c.id AS company_id, c.name AS company_name
            FROM NetworkDevice nd
            JOIN Company c ON nd.company_id = c.id
        """
        return self.fetch_query(query)

#------consulta 3
    def get_companies_without_routers(db):
        query = """
            SELECT c.id, c.name, c.city
            FROM Company c
            WHERE c.id NOT IN (
                SELECT nd.company_id
                FROM NetworkDevice nd
                INNER JOIN Router r ON nd.id = r.network_id
            )
        """
        companies_data = db.fetch_query(query)
        companies = [
            Company(company["id"], company["name"], company["city"]) 
            for company in companies_data
        ]
        return companies

#---------funciona bien, consulta 2
    def get_routing_table(db, router_id): 
        query = "SELECT * FROM Route WHERE router_id = %s" 
        routes_data = db.fetch_query(query, (router_id,)) 
        routes = [ 
            Route(route["id"], route["destination_address"], route["next_hop"], route["metric"], route["interface"]) 
            for route in routes_data 
        ] 
        return routes

#------------------------consulta 4----------------------------------------<<<<<<<<<<<<<<<<<<<<<<<
    def get_company_device_counts(db):
        query = """
            SELECT c.id, c.name, COUNT(nd.id) AS num_devices
            FROM Company c
            LEFT JOIN NetworkDevice nd ON c.id = nd.company_id
            GROUP BY c.id, c.name
        """
        results = db.fetch_query(query)
        company_counts = [
            {"id": row["id"], "name": row["name"], "num_devices": row["num_devices"]}
            for row in results
        ]
        return company_counts

#----find interface more use consulta 5
    def get_most_used_interface(db):
        query = """
            SELECT interface, COUNT(*) as usage_count
            FROM Route
            GROUP BY interface
            ORDER BY usage_count DESC
            LIMIT 1
        """
        result = db.fetch_query(query)

        if result:
            return result[0]["interface"], result[0]["usage_count"]
        else:
            return None, 0

#----promedio de saltos utilizados en cada router consulta 6
    def get_average_hops_per_router(db):
        query = """
            SELECT r.id AS router_id, AVG(rt.metric) AS avg_hops
            FROM Router r
            JOIN Route rt ON r.id = rt.router_id
            GROUP BY r.id
        """
        avg_data = db.fetch_query(query)
        averages = {row["router_id"]: row["avg_hops"] for row in avg_data}
        return averages



    def insert_company(db, company): 
        query = "INSERT INTO Company (name, city) VALUES (%s, %s)" 
        company_id = db.execute_query(query, (company.name, company.city)) 
        return company_id 

    def insert_router(self, router, company_id): 
        query = "INSERT INTO Router (device_name, manufacturer, model, company_id) VALUES (%s, %s, %s, %s)" 
        router_id = self.execute_query(query, (router.device_name, router.manufacturer, router.model, company_id)) 
        return router_id


    def add_routes_to_routing_table(db, router_id, routes): 
        query = """INSERT INTO Route (router_id, destination_address, next_hop, metric, interface)  
                   VALUES (%s, %s, %s, %s, %s)""" 
        for route in routes: 
            db.execute_query(query, (router_id, route.destination_address, route.next_hop, route.metric, route.interface)) 

    def add_route_to_routing_table(db, router_id, route): 
        query = """INSERT INTO Route (router_id, destination_address, next_hop, metric, interface)  
                   VALUES (%s, %s, %s, %s, %s)""" 
        db.execute_query(query, (router_id, route.destination_address, route.next_hop, route.metric, route.interface)) 

#ultimas dos propuestas 
    def get_mac_table(db, switch_id):
        query = "SELECT * FROM Mac WHERE switch_id = %s"
        macs_data = db.fetch_query(query, (switch_id,))
        
        mac_entries = [
            Mac(
                mac["mac_id"],        # id de la MAC
                mac["mac_address"],   # dirección MAC
                mac["port"]           # puerto asociado
            )
            for mac in macs_data
        ]
        
        return mac_entries


    def get_most_used_port(db, switch_id):
        
        query = """
            SELECT port, COUNT(*) as usage_count
            FROM Mac
            WHERE switch_id = %s
            GROUP BY port
            ORDER BY usage_count DESC
            LIMIT 1
        """
        result = db.fetch_query(query, (switch_id,))

        if result:
            return result[0]["port"], result[0]["usage_count"]
        else:
            return None, 0
