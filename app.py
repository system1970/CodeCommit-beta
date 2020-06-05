
# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import *

# from flask import request


# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')

def index():
    return render_template("index.html")
