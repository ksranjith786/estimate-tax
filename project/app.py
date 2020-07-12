from flask import Flask, Blueprint

# Blueprints
from .routes.home import home_bp
from .routes.details import details_bp 
from .routes.estimate import estimate_bp 

blueprints = ( home_bp, details_bp, estimate_bp )

def create_app():
    app = Flask(__name__)
    
    register_blueprint(app, blueprints)
    # Configure explicit url routes to home blueprint
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/home', endpoint='home')
    
    error_pages(app)

    return app
# end create_app

def register_blueprint(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
# end register_blueprint


def error_pages(app):
    # HTTP error pages definitions

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("misc/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("misc/404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("misc/405.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("misc/500.html"), 500
# end error_pages
