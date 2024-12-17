from mysql.connector.cursor_cext import CMySQLCursor

class Cursor:
    def __init__(self, db_access_point) -> None:
        self.db_access_point = db_access_point
    
    def __enter__(self) -> CMySQLCursor:
        self.cursor = self.db_access_point.cursor()
        return self.cursor

    def __exit__(self, *args) -> None:
        self.cursor.close()