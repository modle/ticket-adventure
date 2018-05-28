from datetime import datetime, timedelta
import os

from file_manager import FileManager
import global_vars
from terminalsize import get_terminal_size

class Queries():
    field_padding = {}
    records_to_show = FileManager.properties['app']['history_records_to_show']
    max_file_matches = FileManager.properties['app']['max_file_matches']
    file_search_history_days = FileManager.properties['app']['file_search_history_days']

    def get_ticket_by_status(self, status):
        return self.get_startswith_tickets(status)

    def get_startswith_tickets(self, specific_type):
        tickets = self.get_all_tickets()
        specific_tickets = []
        for t in tickets:
            status = self.get_current_value(t, 'status').lower()
            if status[:len(specific_type)].lower() == specific_type:
                specific_tickets.append(t)
        return specific_tickets

    def get_current_value(self, ticket, field_name):
        # there's probably a better way to query for a specific field match
        for i in FileManager.data:
            for key, value in i.items():
                if key == 'id' and value == ticket:
                    try:
                        return i[field_name].rstrip()
                    except KeyError:
                        return ''

    def update_field_padding(self, target_tickets):
        padding = 2
        self.field_padding['id_padding'] = self.get_max_length('id', target_tickets) + padding
        self.field_padding['approval_padding'] = self.get_max_length('approval', target_tickets) + padding
        self.field_padding['submitted_padding'] = 10 + padding
        self.field_padding['updated_padding'] = 10 + padding
        self.field_padding['completed_padding'] = 10 + padding
        self.field_padding['status_padding'] = self.get_max_length('status', target_tickets) + padding
        self.field_padding['assignee_padding'] = self.get_max_length('assignee', target_tickets) + padding
        self.field_padding['category_padding'] = self.get_max_length('category', target_tickets) + padding
        self.field_padding['web_portal_url'] = self.get_max_length('web_portal_url', target_tickets) + padding
        self.field_padding['dir'] = self.get_max_length('dir', target_tickets) + padding

    def get_max_length(self, field_name, tickets):
        max_length = 0
        for t in tickets:
            length = len(self.get_current_value(t, field_name))
            if length > max_length:
                max_length = length
        if len(field_name) > max_length:
            max_length = len(field_name)
        if max_length == 0:
            max_length = 3
        return max_length

    def get_all_tickets(self):
        tickets_ints = []
        tickets = []
        for i in FileManager.data:
            for key, value in i.items():
                if key == 'id':
                    tickets_ints.append(int(value))

        # make them into strings. Ugh. Probably a smell to convert back and forth just to sort.
        for t in sorted(tickets_ints, reverse = True):
            tickets.append(str(t))

        return tickets

    def get_ticket_info(self, field_to_check, value_to_check):
        print()
        ticket = self.check_for_ticket(field_to_check, value_to_check)
        if (ticket):
            print('Ticket {} found'.format(value_to_check))
            return ticket

    def check_for_ticket(self, field_to_check, value_to_check):
        for i in FileManager.data:
            for key, value in i.items():
                if key == field_to_check and value == value_to_check:
                    return i.items()

    def get_tickets(self, level):
        get_functions = {
            "all": self.get_all_tickets,
            "active": self.get_active_tickets,
            "open": self.get_open_tickets
        }
        return get_functions[level]()

    def get_active_tickets(self):
        active_tickets = []
        for t in self.get_all_tickets():
            status = self.get_current_value(t, 'status').lower()
            if not status.startswith(('hidden', 'wait', 'blocked')):
                active_tickets.append(t)
        return active_tickets

    def get_open_tickets(self):
        open_tickets = []
        for t in self.get_all_tickets():
            status = self.get_current_value(t, 'status').lower()
            if status[:6].lower() != 'hidden':
                open_tickets.append(t)
        return open_tickets

    def get_minimal_ticket_details(self, tickets):
        tickets_with_details = {}
        self.update_field_padding(tickets)
        for t in tickets:
            approval = self.get_current_value(t, 'approval')
            submitted = self.get_current_value(t, 'date_issued')[:10]
            updated = self.get_current_value(t, 'last_updated')[:10]
            completed = self.get_current_value(t, 'date_completed')[:10]
            status = self.get_current_value(t, 'status').lower()
            assignee = self.get_current_value(t, 'assignee').lower()
            category = self.get_current_value(t, 'category')
            tickets_with_details[t] = '{}{}{}{}{}{}'.format(
                approval.ljust(self.field_padding['approval_padding'])
                ,submitted.ljust(self.field_padding['submitted_padding'])
                ,updated.ljust(self.field_padding['updated_padding'])
                ,completed.ljust(self.field_padding['completed_padding'])
                ,status.ljust(self.field_padding['status_padding'])
                ,category.ljust(self.field_padding['category_padding'])
                ,assignee.ljust(self.field_padding['assignee_padding'])
            )
            working_dir = self.get_current_value(t, 'dir')
            web_portal_url = self.get_current_value(t, 'web_portal_url')
            if self.include_extras(len(tickets_with_details[t]) + len(working_dir)):
                tickets_with_details[t] = '{}{}'.format(
                    tickets_with_details[t],
                    working_dir.ljust(self.field_padding['dir'])
                )
            if self.include_extras(len(tickets_with_details[t]) + len(web_portal_url)):
                tickets_with_details[t] = '{}{}'.format(
                    tickets_with_details[t]
                    , web_portal_url.ljust(self.field_padding['web_portal_url'])
                )
        return tickets_with_details

    def include_extras(self, record_length):
        return get_terminal_size()[0] > record_length + 20

    def get_filtered_tickets(self, filter_type):
        tickets = self.get_all_tickets()
        filtered_tickets = []
        for t in tickets:
            status = self.get_current_value(t, 'status').lower()
            if status.lower().find(filter_type) != -1:
                filtered_tickets.append(t)
        return filtered_tickets

    def get_ticket_summary(self):
        ticket_summary = {'all':0,'active':0,'open':0,'blocked':0,'wait':0,'hidden':0,'priority':0,'hidden: closed':0,'hidden: transferred':0,'hidden: cancelled':0}

        for t in self.get_all_tickets():
            ticket_summary['all'] += 1
            status = self.get_current_value(t, 'status').lower()
            if 'hidden' not in status and 'wait' not in status and 'blocked' not in status :
                ticket_summary['active'] += 1
            if 'hidden' not in status:
                ticket_summary['open'] += 1
            if 'blocked' in status:
                ticket_summary['blocked'] += 1
            if 'wait' in status:
                ticket_summary['wait'] += 1
            if 'hidden' in status:
                ticket_summary['hidden'] += 1
            if 'hidden: closed' in status:
                ticket_summary['hidden: closed'] += 1
            if 'hidden: transferred' in status:
                ticket_summary['hidden: transferred'] += 1
            if 'hidden: cancelled' in status:
                ticket_summary['hidden: cancelled'] += 1
            if 'priority' in status:
                ticket_summary['priority'] += 1

        return ticket_summary

    def search_tickets_home(self, search_string):
        tickets_home = FileManager.properties['app']['tickets_home']
        tickets_history = os.listdir(tickets_home)
        ticket_matches = []
        print("\nSearching for folder name matches to <<{}>> at {}".format(search_string, tickets_home))
        for ticket_name in reversed(tickets_history):
            if search_string.lower() in ticket_name.lower():
                ticket_matches.append(ticket_name)
        if len(ticket_matches) == 0:
            print("\nNo folder name matches for <<{}>> found at {}".format(search_string, tickets_home))
            return
        print("\nTotal matches found: {}".format(len(ticket_matches)))
        print("Showing 30 most recent matches:")
        print("\n")
        for ticket_name in ticket_matches[:self.records_to_show]:
            print ('{}{}'.format(tickets_home, ticket_name))

    def search_tickets_home_contents(self, search_string):
        tickets_home = FileManager.properties['app']['tickets_home']
        print('\nbeginning search for sql and txt file content matches to <<{}>> at {}'.format(search_string, tickets_home))
        print('...')
        print('...')
        print('...')
        # get list of files in dir
        tickets_history = os.listdir(tickets_home)
        days_since_mod = self.file_search_history_days
        # create a new list with only files starting with T and modified in last x days
        x_days_ago = datetime.now() - timedelta(days = days_since_mod)
        ticket_dirs = []
        print('getting dirs that start with T and have been modified in the last {} days'.format(days_since_mod))
        for ticket in reversed(tickets_history):
            filepath = '{}{}'.format(tickets_home, ticket)
            last_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            if ticket.startswith("T") and last_modified > x_days_ago:
                ticket_dirs.append(ticket)

        # for each entry in T list
        print ('searching all sql and txt files related to tickets')
        matching_files = []
        for ticket_dir in ticket_dirs:
            # stop after matching at least max_file_matches files
            if len(matching_files) >= max_file_matches:
                break
            # get files in that dir
            try:
                ticket_files = os.listdir('{}{}'.format(tickets_home, ticket_dir))
            except NotADirectoryError:
                continue
            # create a list of files ending in .txt and .sql
            sql_and_txt_files = []
            for ticket_file in ticket_files:
                if ticket_file.endswith(".txt") or ticket_file.endswith(".sql"):
                    sql_and_txt_files.append(ticket_file)
            # for each file in list of files ending in .txt. and .sql
            for target_file in sql_and_txt_files:
                # get the file path
                file_path = '{}{}/{}'.format(tickets_home, ticket_dir, target_file)
                # open the file
                result = self.search_the_file(search_string, file_path)
                # if search_string is found in the file
                if result:
                    # add filename to matched files
                    matching_files.append(file_path)

    def search_the_file(self, search_string, path):
        try:
            with open(path, 'r') as searchfile:
                for line in searchfile:
                    if search_string.lower() in line.lower():
                        print('file: {}'.format(path))
                        print('match found: {}'.format(line))
                        return True
        except:
            return False
        return False
        # print("\nSearching .txt and .sql files for content matches to <<{}>> at {}".format(search_string, properties['tickets_home']))
