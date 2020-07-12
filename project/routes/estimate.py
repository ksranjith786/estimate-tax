from flask import Blueprint, render_template, request

estimate_bp = Blueprint('estimate', __name__, url_prefix='/estimate')

@estimate_bp.route('', methods=['GET', 'POST']) # .../estimate can be called.
def estimate():
    return render_template('coming_soon.html')
# end estimate
