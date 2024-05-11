from psycopg2 import Error
import requests
import config
import time
import BD
import log_system
import skreb


BD = BD.DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)
log = log_system.LogSystem()



url = f'https://api.github.com/repositories'
headers = {
        'Authorization': f'Bearer {config.API_GITHUB}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github+json',
        }


def main(url):
    BD.init_daese()
    BD.init_daese2()
    sb = skreb.Sckred(headers)


    if log.read_to_file() != None:
        url = log.read_to_file()

    while url:
        get_url = requests.get(url, headers=headers)
        log.save_to_file(url)

        try:
            get_url_json = get_url.json()

            print(url)

            for json_page in get_url_json:
                if sb.get_content(json_page) != None:

                    #TODO: сделать тут что то получе 
                    content_from_get_content = sb.get_content(json_page)
                    if content_from_get_content[2] != None:

                        BD.insert_table(content_from_get_content)
                time.sleep(3)

        except KeyboardInterrupt:
            print(url)
            log.save_to_file(url)
            break

        except (Exception, Error) as error:
            log.seve_to_log(level_logging="E", message="FROM main.py in 59", error=error )
            print(url)
            print(error)
            log.save_to_file(url)


if __name__ == "__main__": 
    main(url)
