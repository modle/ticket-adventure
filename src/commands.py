import json
import re

from field_editor import open_editor
from file_manager import FileManager
import global_vars
from options import Options
from printer import Printer
from queries import Queries
from updating import update_field

myPrinter = Printer()
myOptions = Options()
myQueries = Queries()

class Commands():
    def __init__(self):
        self.command_map = {
            'fields': self.ticket_fields,
            'properties': self.ticket_properties,
            'props': self.ticket_properties,
            'links': self.ticket_properties,
            'templates': self.ticket_templates,
            't': self.ticket_templates
        }

    def split_on_first_space(self, string_to_split):
        try:
            parsed_command = string_to_split.split(' ', 1)
        except ValueError:
            parsed_command = []
        return parsed_command

    # TODO refactor with submethods
    def parse_command(self, command):
        command = command.strip()

        # generic cases
        if command in list(self.command_map.keys()):
            self.command_map[command]()
            return

        # special cases
        m = re.match('^(p|priority)\d+', command)
        if m:
            self.match_priority_tickets(m)
            return

        if command[:1] == '!':
            # this is a ticket selector; enter ticket details mode; ignores all text beyond first split entry
            self.load_ticket_details(command)
            return

        if command in ['info', 'i'] and global_vars.current_ticket:
            myPrinter.one_ticket(myQueries.get_ticket_info("id", global_vars.current_ticket))
            return

        # if we get this far, this is an operation against the previously selected ticket
        if global_vars.current_ticket:
            self.manage_current_ticket(command)
            return

        print("{} is not a valid command".format(command))
        return

    def match_priority_tickets(self, match):
        # find tickets with status that matches m.group(0)
        ticket_to_find = match.group(0)
        matched_tickets = myQueries.get_ticket_by_status(ticket_to_find)
        if not matched_tickets:
            try:
                # if match is not found with raw match, replace the p with priority and look for a matching status with priority + num
                ticket_to_find = match.group(0).replace('p', 'priority')
                matched_tickets = myQueries.get_ticket_by_status(ticket_to_find)
            except AttributeError:
                pass
        if not matched_tickets:
            print('no matching tickets found')
            return
        elif len(matched_tickets) == 1:
            global_vars.current_ticket = matched_tickets[0]
            ticket = myQueries.get_ticket_info("id", global_vars.current_ticket)
            myPrinter.one_ticket(ticket)
        elif len(matched_tickets) > 1:
            print('found too many tickets matching {}: {}'.format(ticket_to_find, matched_tickets))

    def load_ticket_details(self, command):
        global_vars.current_ticket = self.parse_id_num(command)
        ticket = myQueries.get_ticket_info("id", global_vars.current_ticket)
        if not ticket:
            print("ID# {} NOT FOUND.\n\nEnter '1' to see open tickets or '1 all' to see all tickets.".format(global_vars.current_ticket))
            global_vars.current_ticket = ""
            return
        myPrinter.one_ticket(ticket)

    def parse_id_num(self, command):
        try:
            parsed_command = self.split_on_first_space(command)
            return parsed_command[0].replace('!','').strip()
        except ValueError:
            return

    def manage_current_ticket(self, command):
        # split the string on the first space [target_field, requested_value]
        parsed_command = self.split_on_first_space(command)
        param = ''
        if len(parsed_command) > 1: param = parsed_command[1]

        if parsed_command[0] == 'edit' and global_vars.current_ticket:
            self.edit_field(param)
            return

        if parsed_command[0] == 'cat':
            parsed_command[0] = 'category'

        if parsed_command[0] == 's':
            parsed_command[0] = 'status'

        # target_field must exist in the field list
        if not self.validate_field(parsed_command[0]):
            return

        # parsed array length 1 means list details
        if len(parsed_command) == 1:
            self.list_details(parsed_command[0])
            return

        # parsed array length 2 means update field (index 0) with requested value (index 1)
        if len(parsed_command) > 1:
            field_number = myOptions.get_field_number(parsed_command[0])
            new_value = parsed_command[1]
            # user can enter a status field number instead of the status itself, so return the status name
            if parsed_command[0] in ['status', 's']:
                new_value = myOptions.get_status_name(parsed_command[1])
            update_field(global_vars.current_ticket, field_number, new_value, 'direct')
            FileManager.save_tickets()

    # consider moving this to validations.py
    def validate_field(self, command):
        if not command:
            print("{} is an invalid field name".format(command))
            return False
        field = command.lower()
        # command is a string!
        if field not in myOptions.record_fields.values():
            print("{} is an invalid field name".format(field))
            return False
        return True

    def edit_field(self, field):
        myPrinter.fields()
        if not field:
            field = input("Choose field to edit: ").strip()

        query_param = myOptions.get_field_name(field)

        if not self.validate_field(query_param):
            return

        current_value = ''
        # field may not exist on ticket record
        try:
            current_value = myQueries.get_current_value(global_vars.current_ticket, query_param)
        except KeyError:
            pass

        update_field(global_vars.current_ticket, myOptions.get_field_number(query_param), open_editor(current_value), 'edit' )

    def list_details(self, target_field):
        if target_field in ['status','s']:
            myPrinter.statuses()
        try:
            current_value = myQueries.get_current_value(global_vars.current_ticket, target_field)
            print("current value: {}".format(current_value))
        except KeyError:
            pass

    def ticket_fields(self):
        myPrinter.fields()

    def ticket_properties(self):
        print(json.dumps(FileManager.properties['app'], sort_keys=True, indent=4, separators=(',', ': ')))

    def ticket_templates(self):
        print(json.dumps(FileManager.properties['templates'], sort_keys=True, indent=4, separators=(',', ': ')))
