from psycopg2 import Error
import os
import requests
import datetime
import config
import time
import BD
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

url = f'https://api.github.com/repositories'
headers = {
        'Authorization': f'Bearer {config.API_GITHUB}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github+json',
        }

BD = BD.DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)

def save_to_file(url):
    with open(f"tmp.txt", "w") as file:
        file.write(url)

def read_to_file():
    if os.path.exists("tmp.txt"):
        with open(f"tmp.txt", "r") as file:
            return file.read()
    return None

def content_from_readme(full_name: str) -> ( str | None ):
    get_path = requests.get(f"https://api.github.com/repos/{full_name}/contents/", headers=headers)

    if get_path.ok:
        get_path = get_path.json()

        for item in get_path:
            if item["path"].upper().startswith("README") :
                readme = item["path"]
                content = requests.get(f"https://api.github.com/repos/{full_name}/contents/{readme}", headers=headers).json()
                
                if "content" in content:
                    content = content.get("content")
                    if content != '':
                        return content
    return None


def date_difference(date_created, date_pushed, date_updated):

    if date_created is None:
        date_created_at = None
    else:
        date_created_at = int(datetime.datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%SZ").timestamp())

    if date_pushed is None:
        date_pushed_at = None
    else:
        date_pushed_at  = int(datetime.datetime.strptime(date_pushed, "%Y-%m-%dT%H:%M:%SZ").timestamp())

    if date_updated is None:
        date_updated_at = None
    else:
        date_updated_at = int(datetime.datetime.strptime(date_updated, "%Y-%m-%dT%H:%M:%SZ").timestamp())

    return date_created_at, date_pushed_at, date_updated_at


def search_next_url(get_url):
    link = get_url.headers.get('Link')
    if link:
        parts = link.split(',')
        for part in parts:
            if 'rel="next"' in part:
                next_url = part.split(';')[0].strip('<> ')
                return next_url


def get_content(json):
    full_name = str(json['full_name'])
    id_rep = int(json['id'])

    get_rep = requests.get(f"https://api.github.com/repos/{full_name}", headers=headers).json()

    if get_rep.get("message"):
        return None

    topics           = list(get_rep['topics'])
    watchers         = int(get_rep['watchers'])
    stargazers_count = int(get_rep['stargazers_count'])
    forks            = int(get_rep['forks'])
    description      = get_rep['description']
    
    created_at       = get_rep['created_at']
    updated_at       = get_rep['updated_at']
    pushed_at        = get_rep['pushed_at']

    created_at_int, pushed_at_int, updated_at_int = date_difference(created_at, pushed_at, updated_at)
    content_base64 = content_from_readme(full_name)
 
    return id_rep, full_name, content_base64, None, description, topics, stargazers_count, forks, watchers, created_at_int, updated_at_int, pushed_at_int

def main(url):

    BD.init_daese()
    BD.init_daese2()

    if read_to_file() != None:
        url = read_to_file()


    while url:
        get_url = requests.get(url, headers=headers)

        try:
            get_url_json = get_url.json()

            print(url)

            for json_page in get_url_json:
                if get_content(json_page) != None:
                    content_from_get_content = get_content(json_page)
                    if content_from_get_content[2] != None:
                        BD.insert_table(content_from_get_content)
                time.sleep(5)

            url = search_next_url(get_url)
            time.sleep(120)

        except KeyboardInterrupt:
            print(url)
            save_to_file(url)
            break

        except (Exception, Error) as error:
            logging.error("FROM main.py in 140: {error}" )
            print(url)
            print(error)
            save_to_file(url)

if __name__ == "__main__": 
    main(url)
