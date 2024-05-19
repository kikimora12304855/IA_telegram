import time
import psycopg2
from psycopg2 import Error
import config
import log_system


class DateBeas:
    def __init__(self, name, user, password, host, port) -> None: 
        self.log = log_system.LogSystem()
        while True:
            try:
                self.conn = psycopg2.connect(f"postgresql://{user}:{password}@{host}:{port}/{name}")
                self.log.seve_to_log("i", "Connected to the database", None)
                break

            except Error as e:
                self.log.seve_to_log("b", "Unable to connect to the database", e)
                time.sleep(2)
            
    def komand_ran(self, string: str):
        with self.conn.cursor() as cur:
            cur.execute(string)
            self.conn.commit()


    def last_line_in_the_table(self, column, table, id="id"):
        """
        SELECT {column} FROM {table} ORDER BY {id} DESC LIMIT 1;
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT {column} FROM {table} ORDER BY {id} DESC LIMIT 1;")
                return cur.fetchone()

        except (Exception, Error) as error:
            self.log.seve_to_log("w", "no table or data in function last_line_in_the_table", error)
            return None 
            

    def ramdom_from_table(self, display_column, filter_column, table) -> (tuple[int, str] | None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT {display_column} FROM {table} WHERE {filter_column} != true ORDER BY RANDOM() LIMIT 1;")
                return cur.fetchone()

        except (Exception, Error) as error:
            self.log.seve_to_log("w", "ramdom_from_table", error)
            return None 


    def check_mark(self, filter_column, id_column, string, table) -> None:
        """ filter_column - column where you need to put true """
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"UPDATE {table} SET {filter_column} = true WHERE {id_column} = %s;", (string,))

        except (Exception, Error) as error:
            self.log.seve_to_log("w", "ramdom_from_table", error)
         


    def insert_table(self, table: str, int_inlet: int, column: str, string):
        with self.conn.cursor() as cur:
            try:
                insert_query = f"""
                INSERT INTO {table} ({column})
                VALUES ({', '.join(['%s'] * int_inlet)})
                """
                cur.execute(insert_query, string)
                self.conn.commit()

            except (Exception, Error) as error:
                self.conn.rollback()
                self.log.seve_to_log("w", "ROLLBACK in insert_table", error)
                time.sleep(5)


    def init_daese(self, table, request):
        with self.conn.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({request});")
            self.conn.commit()


    def reade(self, table):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table};")
            record = cur.fetchall()
            print(f"Server version: {record}")


    def close_connection(self):
        self.conn.close()
        self.log.seve_to_log("i", "Connection closed", None)
        print("Connection closed.")


def main():
    DB = DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)
    request_reps = """
    id SERIAL PRIMARY KEY,    
    full_name VARCHAR,    
    readme TEXT,    
    description TEXT,    
    topics TEXT[],    
    stargazers INT,    
    forks INT,    
    watchers INT,    
    created_date INT,    
    updated_date INT,    
    pushed_date INT 
            """
    DB.init_daese("reps", request_reps)

    DB.reade("reps")
    DB.close_connection()

if __name__ == "__main__":
    main()





