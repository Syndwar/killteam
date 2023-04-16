#/usr/bin/env python3

import ktdb

KILL_TEAM_PAGE = """
<html>
    <head>
        <title>Kill Team 2.0</title>
    </head>
    <body>
        <h1 align='center'>Kill Teams</h1>
{body}
    </body>
</html>
"""

FIRE_TEAM_PAGE = """
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
    </body>
</html>
"""

g_kill_teams = {}
g_fire_teams = {}
g_units = []
g_weapons = {}

def tab(n):
    return n*' '

class KillTeam():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

class FireTeam():
    def __init__(self, data):
        self.id = data['id']

class Unit():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.fireteam = data['fireteam']
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
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']

def create_kill_teams():
    for data in ktdb.KILLTEAMS:
       kt = KillTeam(data)
       g_kill_teams[kt.id] = kt

def create_fire_teams():
    for data in ktdb.FIRETEAMS:
        ft = FireTeam(data)
        g_fire_teams[ft.id] = ft

def create_units():
    for data in ktdb.UNITS:
        unit = Unit(data)
        g_units.append(unit)

def create_weapons():
    for data in ktdb.WEAPONS:
        weapon = Weapon(data)
        g_weapons[weapon.id] = weapon

def serialize():
    create_main_page()
    create_team_pages()

def create_main_page():
    body = ""
    for data in ktdb.KILLTEAMS:
        body = f"{body}{tab(2)}<h2>{data['name']}</h2>\n"
        for fdata in ktdb.FIRETEAMS:
            if (data['id'] == fdata['killteam']):
                body = f"{body}{tab(2)}<h3><a href=\"{fdata['id']}.html\">{fdata['name']}</a></h3>\n"

    page = KILL_TEAM_PAGE.replace('{body}', body)
    with open('main.html', 'w') as f:
        f.write(page)

def create_team_pages():
    for fdata in ktdb.FIRETEAMS:
        body = ""
        for unit in g_units:
            if ("" == body):
                body = f"{tab(4)}<table class=\"center\">"
            if (fdata['id'] == unit.fireteam):
                unit_table = unit.serialize()
                body = f"{body}{unit_table}\n"
        if ("" != body):
            body = f"{body}{tab(4)}</table>"

        with open(f"{fdata['id']}.html", 'w') as f:
            page = FIRE_TEAM_PAGE.replace('{body}', body).replace('{header}', fdata['name'])
            f.write(page)

def create_unit_tables():
    pass

def main():
    create_kill_teams()
    create_fire_teams()
    create_weapons()
    create_units()
    serialize()

if __name__ == '__main__':
    main()
