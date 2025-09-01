#---------------CRUD----------------------
class CLI:
    def __init__(self, db):
        self.db = db  # Aquí va tu DatabaseConnector
    
    def run(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Gestionar Compañías")
            print("2. Gestionar Routers")
            print("3. Gestionar Routes")
            print("4. Gestionar Switches")
            print("5. Gestionar MACs")
            print("6. Gestionar Modems")
            print("7. Salir")
            
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.menu_company()
            elif opcion == "2":
                self.menu_router()
            elif opcion == "3":
                self.menu_route()
            elif opcion == "4":
                self.menu_switch()
            elif opcion == "5":
                self.menu_mac()
            elif opcion == "6":
                self.menu_modem()
            elif opcion == "7":
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida.")

    # ------------------- CRUD COMPANY -------------------
    def menu_company(self):
        print("\n--- CRUD COMPANY ---")
        print("1. Crear Compañía")
        print("2. Listar Compañías")
        print("3. Actualizar Compañía")
        print("4. Eliminar Compañía (borra todo lo relacionado)")
        opcion = input("Opción: ")

        if opcion == "1":
            name = input("Nombre: ")
            city = input("Ciudad: ")
            query = "INSERT INTO Company (name, city) VALUES (%s, %s)"
            self.db.execute_query(query, (name, city))
            print("Compañía creada.")
        
        elif opcion == "2":
            companies = self.db.fetch_query("SELECT * FROM Company")
            for c in companies:
                print(f"{c['id']} - {c['name']} ({c['city']})")
        
        elif opcion == "3":
            company_id = input("ID de la compañía a actualizar: ")
            new_name = input("Nuevo nombre: ")
            new_city = input("Nueva ciudad: ")
            query = "UPDATE Company SET name=%s, city=%s WHERE id=%s"
            self.db.execute_query(query, (new_name, new_city, company_id))
            print("Compañía actualizada.")
        
        elif opcion == "4":
            company_id = input("ID de la compañía a eliminar: ")
            # Aquí deberías borrar en cascada routers, switches, modems, routes, macs
            query = "DELETE FROM Company WHERE id=%s"
            self.db.execute_query(query, (company_id,))
            print("Compañía eliminada junto con sus dispositivos.")

    # ------------------- CRUD ROUTER -------------------
    def menu_router(self):
        company_id = input("ID de la compañía a la que pertenece el router: ")
        companies = self.db.fetch_query("SELECT * FROM Company WHERE id=%s", (company_id,))
        if not companies:
            print("La compañía no existe.")
            return
        
        print("\n--- CRUD ROUTER ---")
        print("1. Crear Router")
        print("2. Listar Routers")
        print("3. Actualizar Router")
        print("4. Eliminar Router (borra sus routes)")
        opcion = input("Opción: ")

        if opcion == "1":
            name = input("Nombre del router: ")
            model = input("Modelo: ")
            query = "INSERT INTO Router (company_id, device_name, model) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (company_id, name, model))
            print("Router creado.")
        
        elif opcion == "2":
            routers = self.db.fetch_query("SELECT * FROM Router WHERE company_id=%s", (company_id,))
            for r in routers:
                print(f"{r['router_id']} - {r['device_name']} ({r['model']})")
        
        elif opcion == "3":
            router_id = input("ID del router a actualizar: ")
            new_name = input("Nuevo nombre: ")
            query = "UPDATE Router SET device_name=%s WHERE router_id=%s"
            self.db.execute_query(query, (new_name, router_id))
            print("Router actualizado.")
        
        elif opcion == "4":
            router_id = input("ID del router a eliminar: ")
            # Primero borro routes asociadas
            self.db.execute_query("DELETE FROM Route WHERE router_id=%s", (router_id,))
            # Luego el router
            self.db.execute_query("DELETE FROM Router WHERE router_id=%s", (router_id,))
            print("Router eliminado junto con sus routes.")

    # ------------------- CRUD ROUTE -------------------
    def menu_route(self):
        router_id = input("ID del router al que pertenece la route: ")
        routers = self.db.fetch_query("SELECT * FROM Router WHERE router_id=%s", (router_id,))
        if not routers:
            print("El router no existe.")
            return

        print("\n--- CRUD ROUTE ---")
        print("1. Crear Route")
        print("2. Listar Routes")
        print("3. Actualizar Route")
        print("4. Eliminar Route")
        opcion = input("Opción: ")

        if opcion == "1":
            dest = input("Dirección destino: ")
            hop = input("Next hop: ")
            metric = input("Métrica: ")
            interface = input("Interfaz: ")
            query = "INSERT INTO Route (router_id, destination_address, next_hop, metric, interface) VALUES (%s, %s, %s, %s, %s)"
            self.db.execute_query(query, (router_id, dest, hop, metric, interface))
            print("Route creada.")

        elif opcion == "2":
            routes = self.db.fetch_query("SELECT * FROM Route WHERE router_id=%s", (router_id,))
            for route in routes:
                print(f"{route['id']} - {route['destination_address']} → {route['next_hop']} (métrica {route['metric']})")

        elif opcion == "3":
            route_id = input("ID de la route a actualizar: ")
            new_dest = input("Nueva dirección destino: ")
            query = "UPDATE Route SET destination_address=%s WHERE id=%s"
            self.db.execute_query(query, (new_dest, route_id))
            print("Route actualizada.")

        elif opcion == "4":
            route_id = input("ID de la route a eliminar: ")
            self.db.execute_query("DELETE FROM Route WHERE id=%s", (route_id,))
            print("Route eliminada.")

    # ------------------- CRUD SWITCH -------------------
    def menu_switch(self):
        company_id = input("ID de la compañía a la que pertenece el switch: ")
        companies = self.db.fetch_query("SELECT * FROM Company WHERE id=%s", (company_id,))
        if not companies:
            print("La compañía no existe.")
            return
        
        print("\n--- CRUD SWITCH ---")
        print("1. Crear Switch")
        print("2. Listar Switches")
        print("3. Actualizar Switch")
        print("4. Eliminar Switch (borra sus MACs)")
        opcion = input("Opción: ")

        if opcion == "1":
            name = input("Nombre del switch: ")
            model = input("Modelo: ")
            num_ports = input("Número de puertos: ")
            query = "INSERT INTO Switch (company_id, device_name, model, num_ports) VALUES (%s, %s, %s, %s)"
            self.db.execute_query(query, (company_id, name, model, num_ports))
            print("Switch creado.")

        elif opcion == "2":
            switches = self.db.fetch_query("SELECT * FROM Switch WHERE company_id=%s", (company_id,))
            for s in switches:
                print(f"{s['switch_id']} - {s['device_name']} ({s['model']}, {s['num_ports']} puertos)")

        elif opcion == "3":
            switch_id = input("ID del switch a actualizar: ")
            new_name = input("Nuevo nombre: ")
            query = "UPDATE Switch SET device_name=%s WHERE switch_id=%s"
            self.db.execute_query(query, (new_name, switch_id))
            print("Switch actualizado.")

        elif opcion == "4":
            switch_id = input("ID del switch a eliminar: ")
            self.db.execute_query("DELETE FROM Mac WHERE switch_id=%s", (switch_id,))
            self.db.execute_query("DELETE FROM Switch WHERE switch_id=%s", (switch_id,))
            print("Switch eliminado junto con sus MACs.")

    # ------------------- CRUD MAC -------------------
    def menu_mac(self):
        switch_id = input("ID del switch al que pertenece la MAC: ")
        switches = self.db.fetch_query("SELECT * FROM Switch WHERE switch_id=%s", (switch_id,))
        if not switches:
            print("El switch no existe.")
            return
        
        print("\n--- CRUD MAC ---")
        print("1. Crear MAC")
        print("2. Listar MACs")
        print("3. Eliminar MAC")
        opcion = input("Opción: ")

        if opcion == "1":
            mac_addr = input("Dirección MAC: ")
            port = input("Puerto: ")
            query = "INSERT INTO Mac (switch_id, mac_address, port) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (switch_id, mac_addr, port))
            print("MAC creada.")

        elif opcion == "2":
            macs = self.db.fetch_query("SELECT * FROM Mac WHERE switch_id=%s", (switch_id,))
            for m in macs:
                print(f"{m['mac_id']} - {m['mac_address']} en puerto {m['port']}")

        elif opcion == "3":
            mac_id = input("ID de la MAC a eliminar: ")
            self.db.execute_query("DELETE FROM Mac WHERE mac_id=%s", (mac_id,))
            print("MAC eliminada.")

    # ------------------- CRUD MODEM -------------------
    def menu_modem(self):
        company_id = input("ID de la compañía a la que pertenece el modem: ")
        companies = self.db.fetch_query("SELECT * FROM Company WHERE id=%s", (company_id,))
        if not companies:
            print("La compañía no existe.")
            return
        
        print("\n--- CRUD MODEM ---")
        print("1. Crear Modem")
        print("2. Listar Modems")
        print("3. Actualizar Modem")
        print("4. Eliminar Modem")
        opcion = input("Opción: ")

        if opcion == "1":
            name = input("Nombre del modem: ")
            model = input("Modelo: ")
            query = "INSERT INTO Modem (company_id, device_name, model) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (company_id, name, model))
            print("Modem creado.")

        elif opcion == "2":
            modems = self.db.fetch_query("SELECT * FROM Modem WHERE company_id=%s", (company_id,))
            for m in modems:
                print(f"{m['modem_id']} - {m['device_name']} ({m['model']})")

        elif opcion == "3":
            modem_id = input("ID del modem a actualizar: ")
            new_name = input("Nuevo nombre: ")
            query = "UPDATE Modem SET device_name=%s WHERE modem_id=%s"
            self.db.execute_query(query, (new_name, modem_id))
            print("Modem actualizado.")

        elif opcion == "4":
            modem_id = input("ID del modem a eliminar: ")
            self.db.execute_query("DELETE FROM Modem WHERE modem_id=%s", (modem_id,))
            print("Modem eliminado.")

