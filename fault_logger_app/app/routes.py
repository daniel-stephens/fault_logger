from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, MotorForm, FunctionForm, FaultForm, SearchForm
from app.models import User, Motors, Function, Fault_log, Location, Starter, Faults, Position
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title = 'Home')


@app.route('/register', methods = ['GET', 'POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name  = form.last_name.data, 
                    email=form.email.data, position =form.position.data ,password=hashed_password )
        db.session.add(user)
        db.session.commit()
        flash (f'Your account has been created! You are now able to log in', 'Success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form = form)


@app.route('/login',  methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()   
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')        
    return render_template("login.html", title='login', form = form)



@app.route('/about')
def about():
    return '<h1>This page will talk about this app</h1>'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account',  methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.position= form.position.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.position.data = current_user.position
        form.email.data = current_user.email

    return render_template('account.html', title='Account',
                             form = form)


@app.route('/motors',  methods = ['GET', 'POST'])
def motor_log():
    form = MotorForm()
    if form.validate_on_submit():
        motor = Motors(serial_number = form.serial_number.data, rating=form.rating.data, voltage  = form.voltage.data, current=form.current.data, 
                    frame_size = form.frame_size.data, number_of_poles=form.number_of_poles.data)
        db.session.add(motor)
        db.session.commit()
        flash (f'Motor has been created in the database', 'Success')
        return redirect(url_for('home'))

    return render_template('motors.html', title='Motors',
                             form = form)


@app.route('/function',  methods = ['GET', 'POST'])
def functions_log():
    form = FunctionForm()
    if form.validate_on_submit():
        function = Function(number = form.number.data, name = form.name.data, rating = form.rating.data,
                            motor = form.motor.data, location = form.location.data, starter = form.starter.data)
        db.session.add(function)
        db.session.commit()
        flash (f'Motor usage has been created in the database', 'Success')
        return redirect(url_for('home'))

    return render_template('functions.html', title='Function', form = form)


@app.route('/faults',  methods = ['GET', 'POST'])
@login_required
def faults_log():
    form = FaultForm()

    if form.validate_on_submit():
        fault = Fault_log(fault = form.faults.data, reporter = form.reporter.data,
                    usage= form.usage.data)
        db.session.add(fault)
        db.session.commit()
        flash (f'Motor fault has been created in the database', 'Success')
        return redirect(url_for('home'))
    
    return render_template('faults.html', title='Fault', form = form)



@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    form.validate_on_submit()
    motor = form.motors.data
    motors = Motors.query.filter_by(id=motor).first()
    #motors = Motors.query.()
    return render_template('search.html',motors = motors, form = form )
    
# @app.route('/try', methods=['GET', 'POST'])
# def trial():
#     form = TryForm()
#     form.validate_on_submit()
#     motor = form.motors.data
#     motors = Motors.query.filter_by(id=motor).first()
#     return render_template('try.html', results = results, form = form)
    