from flask import Blueprint

home_bp = Blueprint('home', __name__) # ignored url_prefix

@home_bp.route('/')
def index():
    return "Hello, World Index!"

@home_bp.route('/home/') # Trialing / is important
def home():
    return "Hello, World Home!"
# end home
