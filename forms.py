from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField, DateField, PasswordField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from models import Executive

class ExecutiveSetupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    post = SelectField("Select Post", validators=[DataRequired()], choices=[])
    date_elect = DateField("Elected Date", validators=[DataRequired], format='%d/%m/%Y')
    alias = SelectField("Alias", validators=[DataRequired()], choices=[])
    arm = SelectField("Where", validators=[DataRequired()], choices=[('KSM', 'KSM'), ('LSM','LSM'), ('Zone1', 'Zone1'),('Zone2', 'Zone2')]) #
    submit = SubmitField("Save Entry")

class OfficeSetupForm(FlaskForm):
    post = StringField("Name", validators=[DataRequired()])
    alias = StringField("Alias", validators=[DataRequired()])
    arm = SelectField("Where", validators=[DataRequired()], choices=[('KSM', 'KSM'), ('LSM','LSM'), ('Zone1', 'Zone1'),('Zone2', 'Zone2')]) #
    submit = SubmitField("Save Entry")

class NewsForm(FlaskForm):
    topic = StringField("Topic", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post News")
    # date_created = DateTimeField("Date/Time", format='%D/%m/%Y %H:%M:%S')
    # posted_by

class MemberForm(FlaskForm):
    ksmno  = StringField('KSM Number')
    firstname = StringField('First Name', validators=[DataRequired(message="First Name is required")])
    lastname = StringField('Last Name', validators=[DataRequired(message="Larst Name is required")])
    midname = StringField('Other Name', validators=[DataRequired(message="Othername is required")])
    address = TextAreaField('Address', validators=[DataRequired(message="Address is required")])
    gender = SelectField('Gender', validators=[DataRequired(message="Gender is required")], choices=[('M', 'Male'),('F','Female')])
    dob = DateField('Date of Birth', validators=[DataRequired(message="Date of Birth is required")], format='%d/%m/%Y')
    phone1 = StringField('Phone', validators=[DataRequired(message="Phone is required")])
    phone2 = StringField('Other Phone')
    email = StringField('Email', validators=[DataRequired(message="Email is required")])
    state_of_origin = StringField('State of Origin', validators=[DataRequired()])
    home_town = StringField('Home Town', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    # state_of_origin = SelectField('State of Origin', validators=[DataRequired(message="State of Origin is required")], choices=[])
    nationality = StringField('Nationality', validators=[DataRequired(message="Nationality is required")])
    degree_in_order  = StringField('Degree', validators=[DataRequired(message="Degree is required")])
    date_initiated = DateField('Date Initiated', validators=[DataRequired(message="Date Initiated is required")], format='%d/%m/%Y')
    lastInvested = DateField('Date of Investiture', validators=[DataRequired(message="Date Initiated is required")], format='%d/%m/%Y')
    place_initiated = StringField('Initiated At', validators=[DataRequired(message="Initiated Venue is required")])
    initiated_sc  = StringField('Initiated Sub-Council', validators=[DataRequired(message="Initiated Sub-Council is required")])
    # initiated_sc  = SelectField('Initiated Sub-Council', validators=[DataRequired()], choices=[], coerce=int)
    current_sc = StringField('Current Sub-Council', validators=[DataRequired()])
    # current_sc = SelectField('Current Sub-Council', validators=[DataRequired()], choices=[], coerce=int)
    membership_status = StringField('Status', validators=[DataRequired(message="Status is required")])
    submit = SubmitField('Submit')
