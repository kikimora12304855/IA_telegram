import requests
import datetime
import log_system
import base64

class Sckred:
    def __init__(self, headers) -> None:
        self.headers = headers
        self.log = log_system.LogSystem()

    def content_from_readme(self, full_name: str) -> ( str | None ):
        get_path = requests.get(f"https://api.github.com/repos/{full_name}/contents/", headers=self.headers)

        if get_path.ok:
            get_path = get_path.json()

            for item in get_path:
                if item["path"].upper().startswith("README") :
                    readme = item["path"]
                    content = requests.get(f"https://api.github.com/repos/{full_name}/contents/{readme}", headers=self.headers).json()
                    
                    if "content" in content:
                        content = content.get("content")
                        if content != '':
                            return content
        else:
            self.log.seve_to_log("E", f"content_from_readme in skreb.py", f"{get_path.json()} get_path.status_code")
        return None


    def date_difference(self, date_created, date_pushed, date_updated):

        if date_created != None:
            date_created_at = int(datetime.datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        else:
            date_created_at = None

        if date_pushed != None:
            date_pushed_at  = int(datetime.datetime.strptime(date_pushed, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        else:
            date_pushed_at = None

        if date_updated != None:
            date_updated_at = int(datetime.datetime.strptime(date_updated, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        else:
            date_updated_at = None

        return date_created_at, date_pushed_at, date_updated_at


    def get_content(self, json):
        full_name = str(json['full_name'])
        id_rep = int(json['id'])

        get_rep = requests.get(f"https://api.github.com/repos/{full_name}", headers=self.headers).json()

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

        created_at_int, pushed_at_int, updated_at_int = self.date_difference(created_at, pushed_at, updated_at)
        content_base64 = self.content_from_readme(full_name)
        content_base64 = base64.b64decode(content_base64).decode('utf-8') if content_base64 != None else None
     
        return id_rep, full_name, content_base64, description, topics, stargazers_count, forks, watchers, created_at_int, updated_at_int, pushed_at_int


