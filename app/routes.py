from flask import render_template,jsonify,send_file,abort
import os

AUDIO_FOLDER = ''



def init_routes(app):
    @app.route('/audio/sample')
    def index():
        return render_template('index.html')

    @app.route('/audio/<filename>')
    def get_audio(filename):
        try:
            file_path = os.path.join(AUDIO_FOLDER, filename)
            if 1:
                return send_file('/Users/lijinliang/Project/visually_impaired_news_app_backend/tts.mp3', mimetype='audio/mp3')
            else:
                abort(404, description="Resource not found")
        except Exception as e:
            return jsonify({"error": str(e)}), 500