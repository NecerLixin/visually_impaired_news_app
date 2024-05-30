from flask import render_template

def init_routes(app):
    @app.route('/audio/sample')
    def index():
        return render_template('index.html')
