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