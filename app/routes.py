from flask import render_template,jsonify,send_file,abort
import os
import json
config_setting = json.load(open('app/config_setting.json'))

project_path = config_setting['project_path']
AUDIO_FOLDER = 'source'



def init_routes(app):
    @app.route('/audio/sample')
    def index():
        return render_template('index.html')

    @app.route('/audio/<filename>')
    def get_audio(filename):
        try:
            file_path = os.path.join(AUDIO_FOLDER, filename)
            file_path = os.path.join(project_path,file_path)
            if 1:
                return send_file(file_path, mimetype='audio/mp3')
            else:
                abort(404, description="Resource not found")
        except Exception as e:
            return jsonify({"error": str(e)}), 500