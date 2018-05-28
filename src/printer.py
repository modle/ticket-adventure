import global_vars
from options import Options
from queries import Queries
from terminalsize import get_terminal_size

class Printer():
    myOptions = Options()
    myQueries = Queries()

    def line_break(self, lines_to_print):
        for i in range(lines_to_print):
            for i in range(get_terminal_size()[0]):
                print('=', end='')
        print('\n')

    def options(self):
        self.line_break(2)
        print('Options:')
        for key, value in sorted(self.myOptions.options.items()):
            print ('{}: {}'.format(key, value))
        print()
        print("--OR-- enter '!' followed by your ticket number to enter ticket details mode. e.g. !12345 for id 12345")
        self.line_break(3)

    def one_ticket(self, ticket):
        print()
        field_list = []

        for key, value in sorted(self.myOptions.record_fields.items()):
            field_list.append((value,key))

        print('Ticket details:')
        for i in field_list:
            for key, value in ticket:
                if key == i[0]:
                    if key in('notes', 'issue', 'reproduce'): print()
                    print('({}) {}: {}'.format(i[1], key, value))
                    if key in('notes', 'issue', 'reproduce'): print()

    def multiple_tickets(self, level):
        print(level)
        tickets = self.myQueries.get_tickets(level)
        self.delegate(tickets, level)

    def delegate(self, tickets, level):
        print()
        self.summary()
        self.priority()
        tickets_with_details = self.myQueries.get_minimal_ticket_details(tickets)
        self.print_the_dict(tickets, tickets_with_details, level)

    def summary(self, param=None):
        ticket_summary = self.myQueries.get_ticket_summary()
        for key, value in ticket_summary.items():
            print("{} {} TICKETS FOUND! Type '1 {}' to view".format(value, key.upper(), key))

    def priority(self):
        tickets = self.myQueries.get_startswith_tickets('priority')
        tickets_with_details = self.myQueries.get_minimal_ticket_details(tickets)
        self.print_the_dict(tickets, tickets_with_details, 'priority')

    def print_the_dict(self, all_tickets, target_tickets, ticket_type):
        self.myQueries.update_field_padding(target_tickets)
        self.headers(len(target_tickets), ticket_type.upper())
        # print all tickets in the target_tickets list
        for t in all_tickets:
            for key, value in target_tickets.items():
                if key == t:
                    print('{}{}'.format(key.ljust(self.myQueries.field_padding['id_padding']), value))
        self.line_break(2)

    def startswith(self, specific_type):
        tickets = self.myQueries.get_startswith_tickets(specific_type)
        self.delegate(tickets, specific_type)

    def statuses(self):
        print()
        print('Available Statuses:')
        for key, value in sorted(self.myOptions.status_fields.items()):
            print ('{}: {}'.format(key, value))
        print()

    def fields(self):
        print()
        print('Available Fields:')
        for key, value in sorted(self.myOptions.record_fields.items()):
            print ('{}: {}'.format(key, value))
        print()

    def headers(self, qty, ticket_type):
        print('\n\n')
        print('***************** ALL {} TICKETS *****************\n'.format(ticket_type))
        print('{} {} TICKETS FOUND!'.format(qty, ticket_type))
        print()
        print(
            '{}{}{}{}{}{}{}'.format(
                'ID#'.ljust(self.myQueries.field_padding['id_padding'])
                ,'APPROVAL#'.ljust(self.myQueries.field_padding['approval_padding'])
                ,'SUBMITTED'.ljust(self.myQueries.field_padding['submitted_padding'])
                ,'UPDATED'.ljust(self.myQueries.field_padding['updated_padding'])
                ,'COMPLETED'.ljust(self.myQueries.field_padding['completed_padding'])
                ,'STATUS'.ljust(self.myQueries.field_padding['status_padding'])
                ,'CATEGORY'.ljust(self.myQueries.field_padding['category_padding'])
                ,'ASSIGNEE'.ljust(self.myQueries.field_padding['assignee_padding'])
            )
        )
        print()

    def filtered(self, specific_type):
        tickets = self.myQueries.get_filtered_tickets(specific_type)
        self.delegate(tickets, specific_type)

