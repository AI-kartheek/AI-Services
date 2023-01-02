from flask import Flask 

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'e8d28a0e41cd45c770e15c49a132d156'

## load and register blue prints
from aiServices.main.routes import main 
from aiServices.fakeNewsClassification.routes import fakeNewsClassif
from aiServices.smsSpamClassification.routes import smsSpamClassif

app.register_blueprint(main)
app.register_blueprint(fakeNewsClassif)
app.register_blueprint(smsSpamClassif)
