class Company: 
    def __init__(self, company_id, name, city): 
        self.company_id = company_id 
        self.name = name 
        self.city = city 
        self.routers = []  # Each company can have multiple routers 
        self.modems=[] 
        self.switches=[] 

    def add_router(self, router): 
        self.routers.append(router) 

    def add_routers(self, routers): 
        self.routers.extend(routers) 
        
    def add_modem(self, modem): 
        self.modems.append(modem) 

    def add_modems(self, modems): 
        self.modems.extend(modems) 
        
    def add_switch(self, switch): 
        self.switches.append(switch) 

    def add_switches(self, switches): 
        self.switches.extend(switches) 

    def print_company(self): 
        print(f"\nCompany: {self.name} (ID: {self.company_id}), City: {self.city}") 
        print("Routers:") 
        for router in self.routers: 
            router.print_router() 
        print("Modems:")
        for modem in self.modems: 
            modem.print_modem()
        print("Switches:") 
        for switch in self.switches: 
            switch.print_switch() 
        


# Base class
class NetworkDevice:
    def __init__(self, device_name: str, manufacturer: str, model: str):
        self.device_name = device_name
        self.manufacturer = manufacturer
        self.model = model

    def __str__(self):
        return f"{self.device_name} ({self.manufacturer} {self.model})"



# Router inherits from NetworkDevice
class Router(NetworkDevice):
    def __init__(self, id: int, device_name: str, manufacturer: str, model: str):
        super().__init__(device_name, manufacturer, model)  # Call parent constructor
        self.id = id
      
        self.__routing_table = []  # Private routing table

    def add_route(self, destination_address, next_hop, metric, interface):
        self.__routing_table.append(Route(destination_address, next_hop, metric, interface))

    def add_routes(self, routes):
        self.__routing_table.extend(routes)

    def print_router(self):
        print(f"\nRouter ID: {self.id}, Name: {self.device_name}, Manufacturer: {self.manufacturer}, Model: {self.model}")
        print("Routing Table:")
        for route in self.__routing_table:
            route.display_info()

#anothers dispositives
# ----------------- MODEM -----------------
class Modem(NetworkDevice):
    def __init__(self, modem_id:int, device_name: str, manufacturer: str, model: str, ip: str, connection_type: str):
        super().__init__(device_name, manufacturer, model)
        self.modem_id=modem_id
        self.ip = ip
        self.connection_type = connection_type  # Ej: "Fiber", "DSL", "Cable"

    def print_modem(self):
        print(f"\n[Modem]  Name: {self.device_name}, Manufacturer: {self.manufacturer}, Model: {self.model}, IP: {self.ip}, Connection: {self.connection_type}")


# ----------------- SWITCH -----------------
class Switch(NetworkDevice):
    def __init__(self, switch_id: int, device_name: str, manufacturer: str, model: str, num_ports: int):
        super().__init__(device_name, manufacturer, model)
        self.switch_id = switch_id
        self.num_ports = num_ports
        self.__mac_table = []  # Lista privada de objetos Mac

    def add_mac_entry(self, mac_id: int, mac_address: str, port: int):
        self.__mac_table.append(Mac(mac_id, mac_address, port))

    def add_mac_entries(self, entries: list):
        """Agregar varias entradas MAC de una vez (lista de objetos Mac)."""
        self.__mac_table.extend(entries)

    def print_switch(self):
        print(f"\nSwitch ID: {self.switch_id}, Name: {self.device_name}, Manufacturer: {self.manufacturer}, Model: {self.model}, Ports: {self.num_ports}")
        print("MAC Table:")
        for mac in self.__mac_table:
            mac.display_info()

            
class Mac:
    def __init__(self, mac_id,mac_address, port ):
        self.mac_id=mac_id
        self.mac_address=mac_address
        self.port=port
        
    def display_info(self):
        print(f"MAC id: {self.mac_id}, MAC address: {self.mac_address}, Puerto: {self.port}") 
        

class Route: 
    def __init__(self, id, destination_address, next_hop, metric, interface): 
        self.id=id
        self.destination_address = destination_address 
        self.next_hop = next_hop 
        self.metric = metric 
        self.interface = interface 

    def display_info(self): 
        print(f"Route id: {self.id}, Destination: {self.destination_address}, Next Hop: {self.next_hop}, Metric: {self.metric}, Interface: {self.interface}") 

                    
        