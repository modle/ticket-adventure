import json
import os

class FileManager():
    current_file_dir = os.path.dirname(__file__)
    tickets_rel_path = "db/tickets.json"
    files = {
        "app": "resources/application.properties",
        # "config": "resources/application.config",
        "templates": "resources/reproduce_templates.properties",
        "printer_values": "resources/printer_values.properties"
    }
    data = []
    properties = {}

    def __init__(self):
        self.load_ticket_data()
        self.load_app_properties()

    @classmethod
    def load_ticket_data(cls):
        fpath = cls.get_path(cls.tickets_rel_path)
        try:
            with open(cls.get_path(fpath)) as data_file:
                cls.data = json.load(data_file)
        except (IOError, ValueError):
            with open(cls.get_path(fpath), 'w+') as data_file:
                json.dump(data, data_file)

    @classmethod
    def get_path(cls, filename):
        return os.path.join(cls.current_file_dir, filename)

    @classmethod
    def load_app_properties(cls):
        for key, value in cls.files.items():
            cls.properties[key] = cls.load_property_file(value)

    @classmethod
    def load_property_file(cls, filename):
        fpath = cls.get_path(filename)
        with open(fpath) as data_file:
            return json.load(data_file)

    @classmethod
    def save_tickets(cls):
        fpath = cls.get_path(cls.tickets_rel_path)
        with open(fpath, 'w') as data_file:
            json.dump(cls.data, data_file)

FileManager()
