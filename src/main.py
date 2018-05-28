#!/usr/bin/python3

import sys

from commands import Commands
from printer import Printer
from queries import Queries
from updating import add_ticket
from file_manager import FileManager

def main():
    myRouter = Router()
    while 1:
        myRouter.myPrinter.options()
        option_selected = input('Choose your path: ').strip()

        parsed_option = myRouter.myCommands.split_on_first_space(option_selected)
        if not parsed_option[0]:
            continue

        if parsed_option[0] not in list(myRouter.executions.keys()):
            if option_selected[:1]:
                myRouter.myCommands.parse_command(option_selected)
                continue

        myRouter.executions.get(parsed_option[0])(parsed_option)


class Router():
    myQueries = Queries()
    myPrinter = Printer()
    myCommands = Commands()
    executions = {}

    def __init__(self):
        self.executions = {
            "0": self.exit_tickets_adventure,
            "1": self.show_active,
            "2": add_ticket,
            "3": self.myPrinter.summary,
            "4": self.search_tickets,
            "5": self.search_sql_and_txts
        }

    def exit_tickets_adventure(self, param=None):
        print('Goodbye')
        sys.exit()

    def show_active(self, parsed_option):
        if len(parsed_option) == 1:
            self.myPrinter.multiple_tickets('active')
        else:
            parsed_sub_option = self.myCommands.split_on_first_space(parsed_option[1])
            if len(parsed_sub_option) == 1:
                self.simple_ticket_query(parsed_sub_option)
            else:
                self.filtered_ticket_query(parsed_sub_option)

    def simple_ticket_query(self, parsed_sub_option):
        if parsed_sub_option[0] in ['all', 'open', 'active']:
            print('sub option matched')
            self.myPrinter.multiple_tickets(parsed_sub_option[0])
        else:
            self.myPrinter.startswith(parsed_sub_option[0])

    def filtered_ticket_query(self, parsed_sub_option):
        if parsed_sub_option[0] in ['contains', 'filter']:
            self.myPrinter.filtered(parsed_sub_option[1])

    def search_tickets(self, parsed_option):
        if len(parsed_option) == 1:
            print("\n")
            print(FileManager.properties['printer_values']['bunch_of_dashes'])
            print(FileManager.properties['printer_values']['search_ticket_dir_no_param'])
            print(FileManager.properties['printer_values']['bunch_of_dashes'])
            return
        self.myQueries.search_tickets_home(parsed_option[1])

    def search_sql_and_txts(self, parsed_option):
        if len(parsed_option) == 1:
            print("\n")
            print(FileManager.properties['printer_values']['bunch_of_dashes'])
            print(FileManager.properties['printer_values']['search_sqls_no_param'])
            print(FileManager.properties['printer_values']['bunch_of_dashes'])
            return
        self.myQueries.search_tickets_home_contents(parsed_option[1])

if __name__ == "__main__":
    main()
