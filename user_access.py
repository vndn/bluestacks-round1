import json, logging
import bcrypt
from entities import User, Role, Task, Resource


def getUserInput(msg, toInt=False):
    '''Returns validated user input.'''
    #TODO - Later added sanity checks
    try:
        userInput =  int(input(msg)) if toInt else input(msg)
    except (ValueError):
        userInput = -1
    return userInput

        
def createDummyUsers(roles):
    '''Creates dummy users based on raw_users array(name, pwd, roleid).'''
    raw_users =[ ['vandan','crackit','DEVELOPER'], ['om', 'test','DEVELOPER'], ['admin', 'minad','ADMIN'] ]
    users={}
    for i in range(len( raw_users) ):
        print(roles[raw_users[i][2]].name)
        user = User(raw_users[i][0], bcrypt.hashpw(raw_users[i][1].encode('utf-8'),
                 bcrypt.gensalt() ), roles[raw_users[i][2]])
        #logging.debug(user.username + ' user created')
        logging.info(user.role.name)
        logging.info(user.role.permissions)
        users[raw_users[i][0]] = user
    return users

def showMenu(tasks):
    '''Display Menu.'''
    print('\n########### -- MENU -- #########')
    for i in tasks:
        print(tasks[i].message)

def login(user, pwd, users):
    '''Returns True if used authenticated else False.'''
    authenticated=False
    if user in users:
        if bcrypt.hashpw(pwd.encode('utf-8'), users[user].encrypted_password):
            logging.info('Logged in as ' + user)
            authenticated=True
        else:
            logging.warning('Login failed, please try again')
    else:
        logging.warning('User does not exist')
    return authenticated

def showResponse(response):
    '''This shows all responses in same format, prefix, suffix etc.'''
    print('\nResponse: ' + response)

if __name__=='__main__':
    
    #Program initialisation
    logging.basicConfig(level=logging.DEBUG, )
    tasks = {1: Task(1,'CHANGE_USER','login or change user'),
             2: Task(2,'ACCESS_RESOURCE','access a resouce'),
             3: Task(3,'EDIT_ROLE','edit a role')}
    #, '2':'VIEW_ROLES', '3':'ACCESS_RESOURCE'
    actions = ['DELETE', 'UPDATE', 'WRITE', 'READ', 'EXECUTE', 'EDIT']
    
    resources = [ Resource('RDS_123','Project 1 RDS DB instance', ['DELETE','UPDATE', 'WRITE', 'READ'] ),
                 Resource('LAMBDA_234','Project 2 lambda/sercice2', ['DELETE','UPDATE', 'WRITE', 'READ'] ),
                 Resource('ROLE_*','Role edit itself is a resouce', ['EDIT','READ'] )]
    
    roles={}
    roles['ADMIN'] = Role(1, 'ADMIN', { 'RDS_123': ['DELETE','UPDATE', 'WRITE', 'READ'],
                                'LAMBDA_234': ['READ','EXECUTE','DELETE','UPDATE'],
                                'ROLE_*': ['EDIT','READ']}),
    roles['DEVELOPER'] =  Role(2, 'DEVELOPER', {'RDS_123': ['READ'],
                                'LAMBDA_234': ['READ','EXECUTE','UPDATE'] } )
    
    #Roles['admin'] should not be tuple but instance of Roles class. This is creating further issues
    print(type(roles), type(roles['ADMIN']))
    print(roles['ADMIN'].permissions)
    users = createDummyUsers(roles)
    for i in users:
        print(users[i].username, users[i].role.permissions)

    #program run
    print('\nPlease login to start session')
    showMenu(tasks)
    loggedIn=False
    choice = getUserInput('Choose action: ', True)
    while(1):
        if choice in tasks:
            if tasks[choice].name=='CHANGE_USER':
                username= getUserInput('Enter username: ')
                password=getUserInput('Enter password:')
                loggedIn = login(username, password, users)
                
                user=users[username]
                print(user.role.permissions)
            elif loggedIn:
                if tasks[choice].name =='ACCESS_RESOURCE':
                    resouce=getUserInput('Enter resource: ')
                    action =getUserInput('Enter action: ') 
                    decision = user.role.checkPermission(resouce, action)
                    response = 'Action allowed !' if decision else 'Action not allowed'
                    showResponse(response)
                elif tasks[choice].name =='EDIT_ROLE':
                    #This check whether current users role supports this op
                    decision = user.role.checkPermission('ROLE_*', 'EDIT')
                    if decision:
                        role = getUserInput('Enter role to edit: ') 
                        resource = getUserInput('Enter resource to change permissions: ')
                        
                        if role in roles:
                            if resouce in roles[role]:
                                
                                addRemove = getUserInput('Press 1 to add 2 to remove: ', True)
                                if addRemove==1:
                                    action = getUserInput('Enter action to add: ')
                                    if action in roles[role][resource]:
                                        showResponse('Action already present')
                                    elif action not in roles[role][resource]:
                                        roles[role].addResource(resource, action)
                                        showResponse('Action added if not present')
                                elif addRemove==2:
                                    roles[role].removeAction(resource, action)
                                    showResponse('Action removed if existed.')
                                else:
                                    showResponse('Invalid choice')
                            else:
                                action = getUserInput('Enter action to add ( remove not possible as resouce new to role): ') 
                                roles[role].addResource(resource, action)
                        addOrRemove = getUserInput('1 to add and 2 to remove: ') 
                    else:
                        showResponse('User not allowed to edit roles')
            else:
                showResponse('You must login to perform this action')
        else:
            showResponse('Invalid choice')
        showMenu(tasks)
        choice = getUserInput('Choose action: ', True)
        