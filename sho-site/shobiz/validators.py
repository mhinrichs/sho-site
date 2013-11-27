from django.core.exceptions import ValidationError

def valid_emp_id(emp_id):
    if len(emp_id) != 7:
        raise ValidationError('Must be 7 characters long')
    if emp_id[0] != 'e':
        raise ValidationError('Must start with "e"')
    if not emp_id[1:].isalnum():
        raise ValidationError('Must be "e" + 6 numbers. Ex. e000001, e000002, etc.')

def valid_store_id(store_id):
    if len(store_id) != 5:
        raise ValidationError('Must be 7 characters long')
    if store_id[0] != 's':
        raise ValidationError('Must start with "e"')
    if not store_id[1:].isalnum():
        raise ValidationError('Must be "s" + 4 numbers. Ex. s0001, sss0002, etc.')


