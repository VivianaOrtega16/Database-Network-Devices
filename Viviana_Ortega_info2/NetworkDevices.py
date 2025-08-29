class Company: 
    def __init__(self, company_id, name, city): 
        self.company_id = company_id 
        self.name = name 
        self.city = city 
        self.routers = []  # Each company can have multiple routers 

    def add_router(self, router): 
        self.routers.append(router) 

    def add_routers(self, routers): 
        self.routers.extend(routers) 

    def print_company(self): 
        print(f"\nCompany: {self.name} (ID: {self.company_id}), City: {self.city}") 
        print("Routers:") 
        for router in self.routers: 
            router.print_router() 


class Router: 
    def __init__(self, router_id, device_name, manufacturer, model, ip): 
        self.router_id = router_id 
        self.device_name = device_name 
        self.manufacturer = manufacturer 
        self.model = model 
        self.ip = ip 
        self.__routing_table = []  # The routing table 

    def add_route(self, destination_address, next_hop, metric, interface): 
        self.__routing_table.append(Route(destination_address, next_hop, metric, interface)) 

    def add_routes(self, routes): 
        self.__routing_table.extend(routes) 

    def print_router(self): 
        print(f"\nRouter ID: {self.router_id}, Name: {self.device_name}, Manufacturer: {self.manufacturer}, Model: {self.model}, IP: {self.ip}") 
        print("Routing Table:") 
        for route in self.__routing_table: 
            route.display_info() 


class Route: 
    def __init__(self, destination_address, next_hop, metric, interface): 
        self.destination_address = destination_address 
        self.next_hop = next_hop 
        self.metric = metric 
        self.interface = interface 

    def display_info(self): 
        print(f"Destination: {self.destination_address}, Next Hop: {self.next_hop}, Metric: {self.metric}, Interface: {self.interface}") 

                    
        