LOGIC FLOW
    1. The program begins with initialising the users, tasks, roles and resouces
    2. User prompt lets user login
        Slight change from the expected flow as the question description said we initially are logged in with admin.
        I have the script in loggedOut state at beginning and you must login to perform any action
    3. Login requires username and password
        Passwords are stored as encrypted strings and not plain text
        If user exists and password hash matches then loggedIn flag is True and user is set to the relavant user object
    4. Resouce access
        Users are given roles and roles are given permissions to access resouces
        So when a user requests action on resouce, it is checked whether role has required permissions
    5. Edit role
        During initialisation admin role is given 'ROLE_*' resource's ['EDIT'' and 'READ' permissions
        So only if you are ADMIN role user, you can do this action
        5.1 If validated then you can enter resouce, action to be added or removed from a role.
        
Entities
    1. User
        User stores name and encrypted password
    2. Task
        Task stores menu items with details- ID, taskname, task message on menu
    3. Resource
        Resouce store resouce name and actions possible on the resouce. 
        TODO- A resouce type should have action constraints rather then resouces
        This helps in ensuring role edits do not give actions which are not allowed on a resouce
    4. Role
        Role stores role id, name, permissions on different resouces as an associative array of actions
        Role provides functions to check permission for a given resouce and action 


TODO
    The program is currently not in working state because of some issue with Role objects not getting properly stored in dictionaries
    But the flow is functional and can be evaludated against expected Design

Usernames and passwords

    Dummy Users - createDummyUsers() function creates 2 DEVELOPER role users and 1 admin role user
    For your reference you can check plain text username and password in this function.
    Ideally this will come from a DB or rather login attempts will hit DB to check authentication but not implmented as not required