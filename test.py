
from flask import Flask, render_template_string
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin



class ConfigClass(object):
    """ Flask application config """

    
    SECRET_KEY = 'dskhfhosfjcslcjsmvdsbvdfbdfbndfndcnd'

   
    MONGODB_SETTINGS = {
        'db': 'DTB',
        'host': 'mongodb://localhost:27017/DTB'
    }

   
    USER_APP_NAME = "ES_Auth page"     
    USER_ENABLE_EMAIL = False     
    USER_ENABLE_USERNAME = True    
    USER_REQUIRE_RETYPE_PASSWORD = False   


def create_app():
   
   
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')


    db = MongoEngine(app)

    class User(db.Document, UserMixin):
        active = db.BooleanField(default=True)

      
        username = db.StringField(default='')
        password = db.StringField()

     
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

      
        roles = db.ListField(db.StringField(), default=[])

  
    user_manager = UserManager(app, db, User)

    
    @app.route('/')
    def home_page():
    
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

 
    @app.route('/members')
    @login_required    
    def member_page():
  
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

    return app



if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5005, debug=True)
