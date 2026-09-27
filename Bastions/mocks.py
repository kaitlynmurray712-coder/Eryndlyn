import json

class MockCharacter:
    def __init__(self):
        self.cvars = {}

    def set_cvar(self, key, string_value):
        self.cvars[key] = string_value

    def delete_cvar(self, key):
        del self.cvars[key]

def get_gvar(gvar_id):
    return open('gvar.json','r').read()
def load_json(string):
    return json.loads(string)
def dump_json(obj):
    return json.dumps(obj)
def vroll(a):
    # placeholder, rereal vroll returns a complex object
    return a