from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hqwETl0Sxi4I9ox9jOBeT16OYpDsEcNLnyIbYGqJcZE'

from . import views
