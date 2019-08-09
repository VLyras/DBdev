from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField,DateField,DateTimeField,DateTimeLocalField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError
from models import User


class BookmarkForm(Form):
    # global url -- might want to remove url validator from here
    url = URLField('If you have a trip bookmark input it here:')
    destination = StringField('Add your destination:', validators=[DataRequired()])
    description = StringField('Add a trip description:')
    #Can I add DateField?
    outbound_date = StringField('Add your trip outbound date:')
    #outbound_date = DateField('Add your trip outbound date:')
    outbound_time = StringField('Add your trip outbound time:')
    #outbound_time = DateTimeLocalField('Add your trip outbound time:', format='%Y-%m-%dT%H:%M')
    inbound_date = StringField('Add your trip inbound date:')
    #inbound_date = DateField('Add your trip inbound date:')
    inbound_time = StringField('Add your trip inbound time:')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message='Tags can only contains letters and numbers')])

    def validate(self):
        #if not self.url.data.startswith("http://") or \
        #        self.url.data.startswith("https://"):
        #    self.url.data = "http://" + self.url.data

        if not Form.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        # filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True



