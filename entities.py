class User:
    
    def __init__(self, username, encrypted_password, role):
        self.username = username
        self.encrypted_password = encrypted_password
        self.role = role

class Role:
    
    permissions = {}
    
    def __init__(self, rid, name, resource_actions):
        self.rid = rid
        self.name = name
        for resource in resource_actions:
            self.permissions[resource] = resource_actions[resource]
        
    def checkPermission(self, resource, action):
        allowed=False
        if resource in self.permissions:
            if action in self.permissions[resource]:
                allowed = True
        return allowed
            
    def addResource(self, resource, action):
        if resource not in self.permissions:
            self.permissions[resource] = [action]
        else:
            if action not in self.permissions[resource]:
                self.permissions[resource].append(self.permissions[resource])
        
    def removeAction(self, resource, action):
        if resource not in self.permissions:
            if action in self.permissions[resource]:
                self.permissions[resource].remove(action)

        
class Task:
    
    def __init__(self, tid, name, message):
        self.tid = tid
        self.name = name
        self.message = 'Press '+ str(tid) + ' to ' + message
        
        
class Action:
    
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action

        
class Resource:
    def __init__(self, resid, name, actions):
        self.resid = resid
        self.name = name
        self.actions = actions
        
