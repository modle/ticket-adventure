class Options():
    options = {
        0:'quit',
        1:'show tickets',
        2:'add ticket',
        3:'ticket summary',
        4:'search tickets home',
        5:'search tickets files'
    }
    record_fields = {
        1:'id',
        2:'approval',
        3:'web_portal_url',
        4:'approval_url',
        5:'date_issued',
        6:'date_added',
        7:'user',
        8:'assignee',
        9:'issue',
        10:'category',
        11:'name',
        12:'key_info',
        13:'last_updated',
        14:'status',
        15:'notes',
        16:'similar_issue',
        17:'hypothesis',
        18:'root_cause',
        19:'resolution',
        20:'tables',
        21:'dir',
        22:'reproduce',
        23:'solution_discovery',
        24:'date_completed'
    }
    appendable_fields = ('issue', 'notes', 'similar_issue', 'hypothesis', 'root_cause', 'resolution', 'tables')
    include_in_create = ('id', 'date_issued', 'user', 'assignee', 'issue', 'category', 'doc', 'key_info')
    timestampable = ('issue', 'notes', 'hypothesis', 'root_cause', 'resolution')
    secondary_field_updates = ('category', 'approval')
    status_fields = {
        1:'PENDING: investigate',
        2:'WAIT: user approval',
        3:'HIDDEN: closed',
        4:'HIDDEN: cancelled',
        5:'HIDDEN: transferred',
        6:'WAIT: user inquiry',
    }
    closed_statuses = ('HIDDEN: closed', 'HIDDEN: cancelled')
    reproduce_steps = {
        'Thing 1': 'Some actions',
        'Thing 2': 'Some other actions'
    }
    yes_list = ('y', 'yes')

    def get_status_name(self, key):
        try:
            return self.status_fields.get(int(key))
        except (ValueError, TypeError) as e:
            return key

    def get_field_number(self, field_name):
        field_num = -1
        for key, value in sorted(self.record_fields.items()):
            if value == field_name:
                field_num = key
                return field_num

    def get_field_name(self, key):
        try:
            return self.record_fields.get(int(key))
        except ValueError:
            return key
