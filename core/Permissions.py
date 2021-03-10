import json

class Main:
    def __init__(self, filename):
        self.permissions = {}
        self.filename = filename
        self.load_permissions()

    def test_user(self, user_id, perm_node):
        if str(user_id) in self.permissions[perm_node]:
            return True
        else:
            return False

    def load_permissions(self):
        json_file = open(self.filename, 'r')
        self.permissions = json.load(json_file)