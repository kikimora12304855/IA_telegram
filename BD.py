import time
import psycopg2
from psycopg2 import Error
import config
import logging
from urllib.parse import quote


logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DateBeas:
    def __init__(self, name, user, password, host, port):
        while True:
            try:
                self.conn = psycopg2.connect(f"postgresql://{user}:{password}@{host}:{port}/{name}")
                logging.info("Connected to the database.")
                print("Connected to the database.")
                break

            except psycopg2.Error as e:
                logging.error(f"Unable to connect to the database: {e} ")
                print(f"Unable to connect to the database: {e}")
                time.sleep(2)
            
    def komand_ran(self, string):
        with self.conn.cursor() as cur:
            cur.execute(string)
            self.conn.commit()

    def insert_table(self, string):
        with self.conn.cursor() as cur:
            try:
                insert_query = f"""INSERT INTO reps (id, full_name, readme, description, topics, stargazers, forks, watchers, created_date, updated_date, pushed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(insert_query, string)
                self.conn.commit()

            except (Exception, Error) as error:
                self.conn.rollback()
                logging.warning("ROLLBACK: {error}")
                print("Произошла ошибка:", error)
                time.sleep(5)

    def init_daese(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS reps (    
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
                );
                        """)
            self.conn.commit()

    def init_daese2(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS reps_rating ( 
                    id INT PRIMARY KEY REFERENCES reps(id), 
                    trash BOOLEAN, 
                    not_interesting BOOLEAN, 
                    interesting BOOLEAN
                );
                        """)
            self.conn.commit()



    def reade(self, table):
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table};")
                record = cur.fetchall()
                print(f"Server version: {record}")


    def close_connection(self):
        self.conn.close()
        logging.info("Connection closed.")
        print("Connection closed.")


def main():
    DB = DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)
    DB.init_daese()
    DB.init_daese2()

    DB.reade("reps")
    DB.close_connection()

if __name__ == "__main__":
    main()





