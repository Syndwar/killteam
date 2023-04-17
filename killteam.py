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

g_factions = {}
g_factions_order = []
g_kill_teams = {}
g_kill_teams_order = []
g_units = []
g_weapons = {}

def tab(n):
    return n*' '

class Faction():
    def __init__(self, id, data):
        self.id = id
        self.name = data['name']

class KillTeam():
    def __init__(self, id, data):
        self.id = id
        self.name = data['name']
        self.kill_team = data['kill_team']

class Unit():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.kill_team = data['kill_team']
        self.melee = None
        self.ranged = None
        self.addWeapons(data['weapons'])

    def addWeapons(self, weapons):
        for id in weapons:
            weapon = g_weapons[id]
            if ('melee' == weapon.type):
                self.melee = weapon
            elif ('ranged' == weapon.type):
                self.ranged = weapon
            elif ('combo' == weapon.type):
                self.melee = weapon
                self.ranged = weapon


    def serialize(self):
        ranged_name = self.ranged.name if self.ranged else "" 
        melee_name = self.melee.name if self.melee else "" 
        output = f"{tab(5)}<tr><th>{self.name}</th><td>{ranged_name}</td><td>{melee_name}</td></tr>"
        return output

class Weapon():
    def __init__(self, id, data):
        self.id = id
        self.name = data['name']
        self.type = data['type']

def create_order():
    with open('data/order.json') as f:
        json_data = json.loads(f.read())
        if json_data:
            for id in json_data['factions']:
                g_factions_order.append(id)
            for id in json_data['kill_teams']:
                g_kill_teams_order.append(id)

def create_factions():
    with open('data/factions.json', 'r') as f:
        json_data = json.loads(f.read())
        if json_data:
            for id in json_data:
                g_factions[id] = Faction(id, json_data[id])

def create_kill_teams():
    with open('data/kill_teams.json', 'r') as f:
        json_data = json.loads(f.read())
        if json_data:
            for id in json_data:
                g_kill_teams[id] = KillTeam(id, json_data[id])

def create_units():
    with open('data/units.json', 'r') as f:
        units_db = json.loads(f.read())
        if units_db: 
            for data in units_db: 
                g_units.append(Unit(data))

def create_weapons():
    with open('data/weapons.json', 'r') as f:
        weapons_db = json.loads(f.read())
        if weapons_db: 
            for id in weapons_db: 
                g_weapons[id] = Weapon(id, weapons_db[id])

def serialize():
    create_main_page()
    create_team_pages()

def create_main_page():
    body = ""
    for f_id in g_factions_order:
        first_row = True
        faction = g_factions[f_id]
        for kt_id in g_kill_teams_order:
            kt = g_kill_teams[kt_id]
            if (f_id == kt.kill_team):
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
    for id in g_kill_teams:
        kt = g_kill_teams[id]
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

def main():
    create_order()
    create_factions()
    create_kill_teams()
    create_weapons()
    create_units()
    serialize()

if __name__ == '__main__':
    main()
