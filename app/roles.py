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
        return { key[0]:n for n,key in enumerate(cls.allUsers) }
        
    @classmethod
    def compareSeniority(cls, u1=None, u2=None):
        h = cls.roleHierarchy()
        return h[u1] < h[u2] if (u1 in h and u2 in h) else False