#/usr/bin/env python3

import json

FACTIONS_PAGE = """
<html>
    <head>
        <title>Kill Team 2.0</title>
    </head>
    <style>
    table.center {
      margin-left: auto; 
      margin-right: auto;
    }
    table, td, th {
        padding: 5px;
        border: 1px solid black;
        border-collapse: collapse;
    }
    th {
        text-aign: left;
    }
    </style>
    <body>
        <h1 align='center'>Kill Teams</h1>
        <table class=\"center\">
{body}
        </table>
    </body>
</html>
"""

KILL_TEAMS_PAGE = """
<html>
    <head>
        <title>Kill Team 2.0 - {header}</title>
    </head>
    <style>
    table.center {
      margin-left: auto; 
      margin-right: auto;
    }
    table, td, th {
        padding: 5px;
        border: 1px solid black;
        border-collapse: collapse;
    }
    th {
        text-aign: left;
    }
    </style>
    <body>
        <h1 align='center'>{header}</h1>
{body}
        <div align='center'><a href=\"main.html\">Back</a></div>
    </body>
</html>
"""

g_factions = []
g_kill_teams = []
g_units = []
g_locale = {}

def tab(n):
    return n*' '

class Faction():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

class KillTeam():
    def __init__(self, data):
        self.id = data['id']
        self.name = g_locale[data['name']]
        self.faction = data['faction']

class Unit():
    def __init__(self, data):
        self.name = g_locale[data['name']]
        self.kill_team = data['kill_team']
        self.melee = None
        self.ranged = None
        self.amount_cur = 0
        self.amount_max = data['max'] if 'max' in data else 1
        self.addWeapons(data['weapons'])

    def addWeapons(self, weapons):
        if ('ranged' in weapons):
            self.ranged = weapons['ranged']
        if ('melee' in weapons):
            self.melee = weapons['melee']

    def serialize(self):
        ranged_name = self.ranged if self.ranged else "" 
        melee_name = self.melee if self.melee else "" 
        amount = f"{self.amount_cur}/{self.amount_max}"
        output = f"{tab(5)}<tr><th>{self.name}</th><td>{ranged_name}</td><td>{melee_name}</td><td>{amount}</td></tr>"
        return output

class Weapon():
    def __init__(self, id, data):
        self.id = id
        self.name = g_locale[data['name']]
        self.type = data['type']

def create_factions():
    with open('data/factions.json', 'r') as f:
        json_data = json.loads(f.read())
        if json_data:
            for data in json_data:
                g_factions.append(Faction(data))

def create_kill_teams():
    with open('data/kill_teams.json', 'r') as f:
        json_data = json.loads(f.read())
        if json_data:
            for data in json_data:
                g_kill_teams.append(KillTeam(data))

def create_units():
    with open('data/units.json', 'r') as f:
        units_db = json.loads(f.read())
        if units_db: 
            for data in units_db: 
                g_units.append(Unit(data))

def serialize():
    create_main_page()
    create_team_pages()

def create_main_page():
    body = ""
    for faction in g_factions:
        first_row = True
        for kt in g_kill_teams:
            if (faction.id == kt.faction):
                page_url = f"<a href=\"{kt.id}.html\">{kt.name}</a>"
                if first_row:
                    body = f"{body}{tab(2)}<tr><th>{faction.name}</th><td>{page_url}</td></tr>\n"
                else:
                    body = f"{body}{tab(2)}<tr><td></td><td>{page_url}</td></tr>\n"
                first_row = False

    page = FACTIONS_PAGE.replace('{body}', body)
    with open('main.html', 'w') as f:
        f.write(page)

def create_team_pages():
    for kt in g_kill_teams:
        body = ""
        for unit in g_units:
            if ("" == body):
                body = f"{tab(4)}<table class=\"center\">"
            if (kt.id == unit.kill_team):
                unit_table = unit.serialize()
                body = f"{body}{unit_table}\n"
        if ("" != body):
            body = f"{body}{tab(4)}</table>"

        with open(f"{kt.id}.html", 'w') as f:
            page = KILL_TEAMS_PAGE.replace('{body}', body).replace('{header}', kt.name)
            f.write(page)

def create_locales():
    with open('data/locale.json', 'r') as f:
        locale_db = json.loads(f.read())
        if locale_db: 
            for key in locale_db:
                g_locale[key] = locale_db[key]

def main():
    create_locales()
    create_factions()
    create_kill_teams()
    create_units()
    serialize()

if __name__ == '__main__':
    main()
