from queries import Queries

myQueries = Queries()

def validate_id_num(new_record, field_to_add):

    ERROR_TEMPLATE = {
        'blank': 'ERROR: {} must not be blank.',
        'numeric': 'ERROR: {} must be numeric.',
        'duplicate': 'ERROR: {} must be unique, existing record found.'
    }

    def try_again():
        new_record[field_to_add] = (input('{}: '.format(field_to_add)).strip())
        validate_id_num(new_record, field_to_add)

    value = new_record[field_to_add]

    if value is 'cancel': return
    if not value:
        print(ERROR_TEMPLATE['blank'].format(field_to_add))
        try_again()
    if not validate_int(value):
        print(ERROR_TEMPLATE['numeric'].format(field_to_add))
        try_again()
    if myQueries.check_for_ticket(field_to_add, value):
        print(ERROR_TEMPLATE['duplicate'].format(field_to_add))
        try_again()


def validate_int(value):
    try:
        value = int(value)
        return True
    except ValueError:
        return False
