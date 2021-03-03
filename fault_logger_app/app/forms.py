from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from  wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Position, Location, Motors, Starter, Faults, Function

def user_query():
    return User.query

def motors_query():
    return Motors.query

def funciton_query():
    return Function.query

def position_query():
    return Position.query

def location_query():
    return Location.query

def starter_query():
    return Starter.query

def fault_query():
    return Faults.query


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    position = QuerySelectField(query_factory = position_query, allow_blank=True, get_label='position')
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has already been registered')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    position = StringField('Position',
                        validators=[DataRequired(), Email()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
     
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email has already been registered')


class MotorForm(FlaskForm):
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    voltage = IntegerField('Voltage', validators=[DataRequired()])
    current = IntegerField('Current', validators=[DataRequired()])
    frame_size = StringField('Frame Size', validators=[DataRequired()])
    number_of_poles = IntegerField('Number of Poles', validators=[DataRequired()]) 
    submit = SubmitField('Submit')



class FunctionForm(FlaskForm):
    number = StringField('Number', validators=[DataRequired()])
    name = StringField('Function Name', validators=[DataRequired()])
    rating = IntegerField('rating', validators=[DataRequired()])
    motor = StringField('Motor')
    location =  QuerySelectField(query_factory = location_query, allow_blank=False, get_label='location')
    starter = QuerySelectField(query_factory = starter_query, allow_blank=False, get_label='name')
    submit = SubmitField('Submit')


class FaultForm(FlaskForm):
    faults = QuerySelectField(query_factory = fault_query, allow_blank=True, get_label='fault')
    reporter = StringField('Reporter')
    usage = StringField('Function') 
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    motors = StringField('Search Motors', validators=[DataRequired()])
    submit = SubmitField('Search')

# class Form(FlaskForm):
#     motors = StringField('Search Motor', validators=[DataRequired()])
#     submit = SubmitField('Search')

class LocationForm(FlaskForm):
    location = StringField('Search Location', validators=[DataRequired()])
    submit = SubmitField('Search')