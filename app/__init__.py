from flask import Flask, render_template,session
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, validators
from wtforms.validators import Required
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app

    class NameForm(Form):
        name = StringField('What is your name?', validators=[Required()])
        email = StringField('email?', validators=[Required()])
        submit = SubmitField('Submit')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = NameForm()
        if form.validate_on_submit():
    	    user =User.query.filter_by(username=form.name.data).first()
    	    if user is None:
    		    user = User(username = form.name.data)
    		    db.session.add(user)
    		    session['known'] = False
    		    if app.config['TUKLAB_ADMIN']:
    		    	send_email(app.config['TUKLAB_ADMIN'], 'New User',
                            'mail/new_user', user=user)
    	    else:
    	        session['known'] = True
    	    session['name'] = form.name.data
    	    form.name.data=''
    	    return redirect(url_for('index'))
        return render_template('index.html',
            form = form, name = session.get('name'),
            known = session.get('known', False))

    @app.route('/user/<name>')
    def user(name):
        return render_template('user.html',name=name)


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404 

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app                 