from psycopg2 import Error
import random
import requests 
import config
import time 
import BD
import log_system
import skreb


BD = BD.DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)
log = log_system.LogSystem()

table_reps = "reps"
column = "id, full_name, readme, description, topics, stargazers, forks, watchers, created_date, updated_date, pushed_date"
int_inlet = 11

table_url = "url"
column_url = "url"
column_id_url = "id, url"
column_url_id = "id"
column_url_filter = "analyzed"

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

headers = {
        'Authorization': f'Bearer {config.API_GITHUB}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github+json',
        }


def main():
    time.sleep(30)
    BD.init_daese(table_reps, request_reps)
    sb = skreb.Sckred(headers)

    while True:
        if random.randint(1, 10) == random.randint(1, 10):
            time.sleep(random.randint(10, 300))
        try:
            ramdom = BD.ramdom_from_table(column_id_url, column_url_filter, table_url)

            if ramdom is None:
                time.sleep(60*60)
                continue

            url = ramdom[1]
            id_from_ramdom = ramdom[0]

            get_url = requests.get(url, headers=headers)
            
            while get_url.ok is not True:
                time.sleep(60*1)
                get_url = requests.get(url, headers=headers)

            get_url_json = get_url.json()

            print(url)

            for json_page in get_url_json:

                time.sleep(2.3)

                content_from_get_content = sb.get_content(json_page)

                if content_from_get_content != None:

                    if content_from_get_content[2] != None:

                        BD.insert_table(table_reps, int_inlet, column, content_from_get_content)

            BD.check_mark(column_url_filter, column_url_id, id_from_ramdom, table_url)


        except (Exception, Error) as error:
            log.seve_to_log(level_logging="E", message="FROM main.py", error=error )
            print(error)


if __name__ == "__main__": 
    main()
