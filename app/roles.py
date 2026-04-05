# logged in user accounts
class Roles():
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

    # Role Groups
    staffers = [
        'super',
        'admin',
        'mod'
    ]
    
    senior = [
        'super',
        'admin'
    ]

    # Non staff, client or paid member accounts
    members = [
        'enterprise',
        'pro',
        'user',
        'viewer'
]
    
    paid = [
        'enterprise',
        'pro'
    ]
    
    inactive = [
        'disabled',
        'banned'
    ]
    
    all = [*staffers, *members]
    
    roleGroups = {
        'all' : all,
        'staffers' : staffers,
        'senior' : senior,
        'paid' : paid,
        'members' : members,
        'inactive' : inactive
    }
    
    @classmethod
    def roleHierarchy(cls):
        _user_h = { key[0]:n for n,key in enumerate(cls.allUsers) }
        _inac_h = { key[0]:len(_user_h) for key in cls.allInactive }
        return _user_h | _inac_h # nb: | operator combines dicts
        
    @classmethod
    def compareSeniority(cls, u1=None, u2=None):
        h = cls.roleHierarchy()
        return h[u1] < h[u2] if (u1 in h and u2 in h) else False