from includes.Cursor import Cursor
from mysql.connector import connect 
from mysql.connector.connection_cext import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

class Database:
    def __init__ (self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __data_to_dict(self, data_keys: dict, data_dict: dict) -> list:
        result = []
        for data in data_dict:
            temp_dict = {data_keys[i]: data[i] for i in range(len(data))}
            result.append(temp_dict)
        return result

    def __Process_command(self, command) -> dict:
        with Cursor(self.db_access_point) as cursor:
            cursor.execute(command)
            querryData = cursor.fetchall()
            query_keys = list(cursor.column_names)
        return self.__data_to_dict(query_keys, querryData)
    
    def connect(self) -> CMySQLConnection:
        self.db_access_point = connect(
                                  host = self.host,
                                  user = self.user,
                                  password = self.password,
                                  database = self.database
                              )
        return self.db_access_point

    def disconnect(self) -> None:
        self.db_access_point.disconnect()
    
    def getCursor(self) -> CMySQLCursor:
        self.cursor = self.db_access_point.cursor()
        return self.cursor
    
    def update(self, command):
        with Cursor(self.db_access_point) as cursor:
            cursor.execute(command)
        self.db_access_point.commit()

    # Modifying functions
    def addPerson(self, pers_id: str, pers_name: str, 
                        pers_email: str, pers_address: str = "") -> None:
        command = f"INSERT INTO Persoana(id, nume, email, adresa) \
                    VALUES ({pers_id}, '{pers_name}', '{pers_email}', \
                    '{pers_address}');"
        self.update(command)
    
    def addDevice(self, id_d: int,  id_client: int, id_depanator: int,
                        aparat: str, data_introducere:str, data_constatare: str, 
                        data_finalizare: str, simptome: str, defect: str = '',
                        durata: int = 0, manopera_ora: float = 0, 
                        total: float = 0) -> None:
        command = f"INSERT INTO Deviz (id_d, data_introducere, aparat, simptome, \
                                       defect, data_constatare, data_finalizare, \
                                       durata, manopera_ora, total, id_client, \
                                       id_depanator) \
                   VALUES ({id_d}, {data_introducere}, '{aparat}', '{simptome}', \
                           '{defect}', {data_constatare}, {data_finalizare}, \
                            {durata}, {manopera_ora}, {total}, {id_client}, \
                            {id_depanator})"
        self.update(command)
    
    def addComponent(self, id_p: int, descriere: str, fabricant: str, 
                           cantitate_stoc:int , pret_c: float) -> None:
        command = f"INSERT INTO Piesa (id_p, descriere, fabricant, \
                                       cantitate_stoc, pret_c) \
                    VALUES ({id_p}, '{descriere}', '{fabricant}', \
                            {cantitate_stoc}, {pret_c});"
        self.update(command)
   

    def addDeviceComponent(self, id_d: int, id_p: int, 
                                 cantitate: int, pret_r: float) -> None:
        command = f"INSERT INTO Piesa_Deviz(id_d, id_p, cantitate, pret_r) \
                    VALUES ({id_d}, {id_p}, {cantitate}, {pret_r})"
        self.update(command)
    
    def deleteFromTableByValue(self, table_name: str, column_name: str, 
                           row_value: str) -> None:
        command = f"DELETE FROM {table_name} \
                    WHERE {column_name} = {row_value}"
        self.update(command)

     
    def deleteFromTableByCondition(self, table_name: str, condition: str) -> None:
        command = f"DELETE FROM {table_name} \
                    WHERE {condition}"
        self.update(command)

    def updateTableByValue(self, table_name: str, column_name: str, 
                                     row_value:str, *args: str) -> None:
        command = f"Update {table_name} \
                    SET {', '.join(args[0])} \
                    WHERE {column_name} = {row_value}"
        self.update(command)

    def updateTableByCondition(self, table_name: str, condition: str, 
                                     *args: str) -> None:
        command = f"Update {table_name} \
                    SET {', '.join(args[0])} \
                    WHERE {condition}"
        self.update(command)

    # Alter functions
    def addColumn(self, table_name: str, column_name: str,
                        datatype: str) -> None:
        command = f"ALTER TABLE {table_name} \
                    ADD {column_name} {datatype};"
        
        self.update(command)

    def deleteColumn(self, table_name: str, column_name: str) -> None:
        command = f"ALTER TABLE {table_name} \
                    DROP COLUMN {column_name};"
        
        self.update(command)

    def modifyColumn(self, table_name: str, column_name: str,
                        datatype: str) -> None:
        command = f"ALTER TABLE {table_name} \
                    MODIFY COLUMN {column_name} {datatype};"
        
        self.update(command)

    # Listing functions
    def getAllFromTable(self, table_name: str) -> None:
        rows = self.querryData(f"SELECT * \
                                 FROM {table_name}")
        return rows   
     
    def getAllFromTableWithCondition(self, table_name: str, 
                                            condition: str) -> None:
        rows = self.querryData(f"SELECT * \
                                 FROM {table_name} \
                                 WHERE {condition}")
        return (rows)

    def querryData(self, command: str) -> list:
        if ("INSERT" or "DELETE" or 
            "ALTER" or "CREATE" or "REPLACE") in command.upper():
            print("This function is for queries!\n")
            return []
        return self.__Process_command(command)
    
    def callProcedure(self, procedure_name):
        with Cursor(self.db_access_point) as cursor:
            cursor.callproc(procedure_name)
            results = cursor.stored_results()
            for result in results:
                querryData = result.fetchall()
                query_keys = [desc[0] for desc in result.description]
        return self.__data_to_dict(query_keys, querryData)
    
    # TODO: one function for ADDERS?