from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import URLField,DateField,DateTimeField,DateTimeLocalField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError
from models import User


class TripForm(Form):
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
    privacy = BooleanField('Is this a private Trip')

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


class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(Form):
    username = StringField('Your Username:', validators=[DataRequired(), Length(3, 80),
                                                         Regexp('^[A-Za-z0-9_]{3,}$',
                                                                message='Username consists of numbers, letters and underscores')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('This email has been used by another user.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
