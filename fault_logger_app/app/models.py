from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(60), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    motor_id = db.Column(db.Integer, db.ForeignKey('motors.id'))
    location_id = db.Column(db.String(60), db.ForeignKey('location.id'))
    starter_id = db.Column(db.String(60), db.ForeignKey('starter.id'), unique=False, nullable=True)
    function = db.relationship('Fault_log', backref='usage')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Function('{self.number}', '{self.name}', '{self.rating}', '{self.date_created}')"




class Fault_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fault_id = db.Column(db.Integer, db.ForeignKey('faults.id'), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    function_id = db.Column(db.Integer, db.ForeignKey('function.id'), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Fault_log('{self.fault_id}', '{self.user_id}', '{self.function_number}')"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(60), unique=True, nullable=False)
    user_position = db.relationship('User', backref='position')
    
    def __repr__(self):
        return f"Position('{self.position}')"


class Faults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fault = db.Column(db.String(60), unique=False, nullable=False)
    error = db.relationship('Fault_log', backref='fault')

    def __repr__(self):
        return f"Faults('{self.fault}')"


class Motors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(60), unique=True, nullable=False )
    rating = db.Column(db.Integer, unique=False, nullable=False)
    voltage = db.Column(db.Integer, unique=False, nullable=False)
    current = db.Column(db.Integer, unique=False, nullable=False)
    frame_size = db.Column(db.String(60), nullable=False)
    number_of_poles = db.Column(db.Integer, unique=False, nullable=True)
    function = db.relationship('Function', backref='motor', uselist = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Motors('{self.serial_number}','{self.rating}', '{self.voltage}', '{self.current}', '{self.frame_size}', '{self.number_of_poles}', '{self.date_created}')"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(60), unique=True, nullable=False)
    place = db.relationship('Function', backref='location')

    def __repr__(self):
        return f"Location('{self.location}')"


class Starter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    starter = db.relationship('Function', backref='starter')

    def __repr__(self):
        return f"Starter('{self.name}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name =  db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reporter = db.relationship('Fault_log', backref='reporter')
    password = db.Column(db.String(60), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey ('position.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

