from shobiz.models import Store, Employee
from datetime import datetime

DEFAULT_STORE = Store.objects.get_or_create(store_id = 's0001',

                                            defaults= {
                                                'name': 'Default',
                                                'romaji': 'Default',
                                                'post_code': '000-0000',
                                                'address1': 'Default',
                                                'address2': 'Default',
                                                'phone': '000000000000',
                                                'email': 'email@fakeemail.com',
                                                'entry_date': datetime.now(),
                                                'last_edited': datetime.now(),
                                                'valid_profile': True,
                                                'note': 'Default note',
                                                }
                                            )[0]

DEFAULT_EMPLOYEE = Employee.objects.get_or_create(emp_id = 'e000001',

                                                  defaults= {
                                                      'name': 'Default',
                                                      'romaji': 'Default',
                                                      'post_code': '000-0000',
                                                      'address1': 'Default',
                                                      'address2': 'Default',
                                                      'phone': '000000000000',
                                                      'email': 'email@fakeemail.com',
                                                      'entry_date': datetime.now(),
                                                      'last_edited': datetime.now(),
                                                      'valid_profile': True,
                                                      'note': 'Default note',
                                                      'birthday': datetime.now(),
                                                      }
                                                  )[0]
