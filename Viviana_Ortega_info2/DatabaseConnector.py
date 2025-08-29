import mysql.connector 
from mysql.connector import Error 
from NetworkDevices import Company 
from NetworkDevices import Router 
from NetworkDevices import Route 

class DatabaseConnector: 
    def __init__(self, host="localhost", user="root", password="", database="networkdb"): 
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
            print(f"Error: {e}") 

    def get_all_companies(self): 
        query = "SELECT * FROM Company" 
        companies_data = self.fetch_query(query) 
        companies = [Company(company["id"], company["name"], company["city"]) for company in companies_data] 
        for company in companies: 
            routers = self.get_routers_by_company(company.company_id) 
            for router in routers: 
                routes = self.get_routing_table(router.router_id) 
                router.add_routes(routes) 
                company.add_router(router) 
        return companies 

    def get_routers_by_company(db, company_id): 
        query = "SELECT * FROM Router WHERE company_id = %s" 
        routers_data = db.fetch_query(query, (company_id,)) 
        routers = [ 
            Router(router["id"], router["device_name"], router["manufacturer"], router["model"], router["ip"]) 
            for router in routers_data 
        ] 
        return routers 

    def get_routing_table(db, router_id): 
        query = "SELECT * FROM Route WHERE router_id = %s" 
        routes_data = db.fetch_query(query, (router_id,)) 
        routes = [ 
            Route(route["destination_address"], route["next_hop"], route["metric"], route["interface"]) 
            for route in routes_data 
        ] 
        return routes 

    def insert_company(db, company): 
        query = "INSERT INTO Company (name, city) VALUES (%s, %s)" 
        company_id = db.execute_query(query, (company.name, company.city)) 
        return company_id 

    def insert_router(db, router, company_id): 
        query = "INSERT INTO Router (device_name, manufacturer, model, ip, company_id) VALUES (%s, %s, %s, %s, %s)" 
        router_id = db.execute_query(query, (router.device_name, router.manufacturer, router.model, router.ip, company_id)) 
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
