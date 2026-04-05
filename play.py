class Test():
                    
    @property
    def user_id(self):
        return getattr(self,'id',None)
    
    @user_id.setter
    def user_id(self,id):
        self.id = id
        
    @property
    def user(self):
        return f'User {self.user_id}'
    
    
t = Test()
t.user_id = '11'
print (t.user_id)
print (t.user)

d1 = {'staus' : 'success', 'message' : 'OK'}
d2 = {'status' : 'error', 'message' : 'SQL failed'}

print ({'userdb' : d1, 'inactivedb':d2})

allUsers =  [ 
        ('super', 'Owner Super Admin'),
        ('admin', 'Administrator'),
        ('mod', 'Moderator'),
        ('enterprise', 'Enterprise User'),
        ('pro', 'Pro User'),
        ('user', 'User'),
        ('viewer', 'Viewer')
]

# deactivated user accounts. Cannot log in but have tabled data
allInactive = [
    ('disabled', 'Disabled Account'),
    ('banned', 'Banned')
]

def roleHierarchy():
    u_hierarchy = { key[0]:n for n,key in enumerate(allUsers) }
    i_hierachy = { key[0]:len(u_hierarchy) for key in allInactive}
    return u_hierarchy | i_hierachy

print (roleHierarchy())
    
