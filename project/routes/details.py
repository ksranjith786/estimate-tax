from flask import Blueprint, render_template

details_bp = Blueprint('details', __name__, url_prefix='/details')

@details_bp.route('/', methods=['GET', 'POST']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def details():
    return render_template('details.html')
# end estimate
