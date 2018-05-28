import datetime
from time import sleep

from file_manager import FileManager
import global_vars
from options import Options
from printer import Printer
from queries import Queries
from validations import validate_id_num

myOptions = Options()
myQueries = Queries()

def add_ticket(param=None):
    new_record = collect_new_ticket_info()
    set_ticket_defaults(new_record)
    update_data_dict(new_record)
    FileManager.save_tickets()
    # print status
    print('\nTicket record added.')
    myPrinter.one_ticket(myQueries.check_for_ticket('id', global_vars.current_ticket))


def collect_new_ticket_info():
    new_record = {}
    properties = FileManager.properties['app']
    for key, value in sorted(myOptions.record_fields.items()):
        # only prompt for certain fields
        if value not in myOptions.include_in_create:
            continue
        # get user input for field value
        new_record[value] = get_user_input(value)
        # validate id num
        if value == 'id':
            validate_id_num(new_record, value)
            global_vars.current_ticket = new_record['id']
            new_record['web_portal_url'] = properties['web_portal_url'] + new_record['id']
            print('Generated URL: {}'.format(new_record['web_portal_url']))
            continue

        # cancel to exit
        if new_record[value] in ['cancel', 'quit', 'exit', 'abort']:
            print('Aborting ticket add!')
            return

        # do things if category is updated
        if value == 'category':
            # generate working directory name
            folder_name = get_working_dir(new_record['category'])
            new_record['dir'] = '{}{}'.format(properties['working_dir'], folder_name)
            # provide basic steps to navigate the GUI
            new_record['reproduce'] = get_reproduce_steps(new_record['category'])
    return new_record


def get_user_input(value):
    return (input('{}: '.format(value)).strip())


def get_working_dir(value):
    folder_name = 'T{}_{}'.format(global_vars.current_ticket, value.replace(' ', '-'))
    print('Use this for the folder name:\n\n{}'.format(folder_name))
    print('Tickets home: {}'.format(FileManager.properties['app']['tickets_home']))
    return folder_name


def get_reproduce_steps(category):
    for key, value in myOptions.reproduce_steps.items():
        if key in category:
            return value
    return ''


def set_ticket_defaults(new_record):
    if not new_record['assignee']: new_record['assignee'] = 'USRODT'
    new_record['status'] = myOptions.get_status_name(1)
    # time stamps
    new_record['date_added'] = get_time()
    new_record['last_updated'] = get_time()


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')


def update_data_dict(new_ticket):
    # update the data dict and save tickets
    FileManager.data.append(new_ticket)


def get_category(id):
    return myQueries.get_current_value(id, 'category')


def print_value_difference(id, field_name, new_value):
    print('Updating field: {}............ '.format(field_name))
    current_value = myQueries.get_current_value(id, field_name)
    if current_value:
        print('current value: {}'.format(current_value))
    print('new value: {}'.format(new_value))


def update_field(id, field_num, new_value, source):
    field_name = myOptions.get_field_name(field_num)
    new_value = prepare_update_contents(id, field_name, new_value, source)
    print_value_difference(id, field_name, new_value)
    if input('Is this OK? (y/n)').lower() in myOptions.yes_list: ## OK up to this point
        perform_updates(id, field_name, new_value)
    else:
        print('Aborting!')


def prepare_update_contents(id, field_name, new_value, source):
    # special field updates for cli entry
    if source != 'edit':
        new_value = handle_dir_string_updates(id, field_name, new_value)
        new_value = timestamp_entry_if_applicable(field_name, new_value)
        new_value = append_to_old_contents_if_applicable(id, field_name, new_value)
    return new_value


def handle_dir_string_updates(id, field_name, new_value):
    properties = FileManager.properties['app']
    if field_name in ['approval_url'] and properties['approval_url'] not in new_value:
        new_value = '{}{}'.format(properties[field_name], new_value)
    return new_value


def timestamp_entry_if_applicable(field_name, new_value):
    if (field_name in myOptions.timestampable):
        new_value = '{}: {}'.format(get_time(), new_value)
    return new_value


def append_to_old_contents_if_applicable(id, field_name, new_value):
    current_value = myQueries.get_current_value(id, field_name)
    if field_name in myOptions.appendable_fields and current_value:
        new_value = '{}\n{}'.format(current_value, new_value)
    return new_value


def perform_updates(id, field_name, new_value):
    updated = False
    # update notes with change info
    if field_name is not 'notes':
        update_notes_with_change_info(id, field_name, new_value)
    updated = update_the_record(id, field_name, new_value)
    update_secondary_fields(id, field_name, new_value)
    if updated:
        timestamp_ticket(id, field_name, new_value)
        print()
        print('Ticket updated')
        myPrinter.one_ticket(myQueries.check_for_ticket('id', id))
    FileManager.save_tickets()


def update_notes_with_change_info(id, field_name, new_value):
    NOTE_TEMPLATE = {
        'status': '{}\n{}: changed status from <<{}>> to <<{}>>',
        'other': '{}\n{}: field updated: <<{}>>'
    }
    current_note = myQueries.get_current_value(id, 'notes')
    current_value = myQueries.get_current_value(id, field_name)
    if field_name in ['status']:
        update_string = NOTE_TEMPLATE['status'].format(current_note, get_time(), current_value, new_value)
    else:
        update_string = NOTE_TEMPLATE['other'].format(current_note, get_time(), field_name)
    print("notes are " + update_string)
    update_the_record(id, 'notes', update_string)


def update_the_record(id, field_name, new_value):
    for i in FileManager.data:
        for key, value in i.copy().items():
            if key == 'id' and value == id:
                myQueries.check_for_ticket('id', id)
                i[field_name] = str(new_value)
                return True


def update_secondary_fields(id, field_name, new_value):
    properties = FileManager.properties['app']
    FIELD_VALUE_TEMPLATE = {
        'category': '{}T{}_{}\\',
        'approval': '{}{}'
    }
    if field_name not in list(FIELD_VALUE_TEMPLATE.keys()): # myOptions.secondary_field_updates
        return
    if field_name is 'category':
        update_the_record(id, 'dir', FIELD_VALUE_TEMPLATE[field_name].format(properties['working_dir'], id, new_value.replace(' ', '-')))
    if field_name is 'approval':
        update_the_record(id, 'approval_url', FIELD_VALUE_TEMPLATE[field_name].format(properties['approval_url'], new_value))


def timestamp_ticket(id, field_name, new_value):
    # time stamp the ticket
    update_the_record(id, 'last_updated', get_time())
    if field_name in ['status'] and new_value in myOptions.closed_statuses:
        update_the_record(id, 'date_completed', get_time())

myPrinter = Printer()
