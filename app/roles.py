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
        'paid' : paid,
        'members' : members,
        'inactive' : inactive
    }