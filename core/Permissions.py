import json

class Main:
    def __init__(self, userdb):
        self.permissions = {}
        self.userdb = userdb

    def test_user(self, user_id, perm_node):
        if perm_node in self.userdb.get_perms(user_id):
            return True
        else:
            return False