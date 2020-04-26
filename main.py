from cerberus import Validator, errors

class CustomErrorHandler(errors.BasicErrorHandler):
    def __init__(self, tree=None, custom_messages=None):
        super(CustomErrorHandler, self).__init__(tree)
        self.custom_messages = custom_messages or {}

    def _format_message(self, field, error):
        tmp = self.custom_messages
        for x in error.schema_path:
            try:
                tmp = tmp[x]
            except KeyError:
                return super(CustomErrorHandler, self)._format_message(field, error)
        if isinstance(tmp, dict):  # if "unknown field"
            return super(CustomErrorHandler, self)._format_message(field, error)
        else:
            return tmp

schema = {
  'username': { 'type': 'string', 'required': True, 'minlength':6, 'maxlength': 10},
  'password': { 'type': 'string', 'required': True, 'minlength':8, 'maxlength': 20},
}

messages = {
  'username': { 'minlength': 'Username should be atleast 6 chars', 'maxlength': 'Username should be atmost 10 chars'},
  'password': { 'minlength': 'Password should be atleast 8 chars ', 'maxlength': 'Password should be atmost 20 chars'}
}

data = { 'username': 'demouser', 'password': 'demouser@123'}

v = Validator(schema, error_handler = CustomErrorHandler(custom_messages = messages))

if v.validate(data, schema):
  print("No error")
else:
  print(v.errors)