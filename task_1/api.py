import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from datetime import datetime, timezone


FORMAT = '%Y-%m-%dT%H:%M:%SZ'
WEEKDAY_FORMAT = "%A"

def create_app(test_config=None):
	# create and configure app
	app = Flask(__name__)

	# Settings up CORS. Allow '*' for origins
	CORS(app, resource={r'/api/*': {'origin': '*'}})

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Context-Type, Authorization, True')
		response.headers.add('Access-Control-Allow-Methods', 'GET')

		return response

	@app.route('/api', methods=['GET'])
	def home():
                time_now = datetime.now(timezone.utc).strftime(FORMAT)
                weekday = datetime.now(timezone.utc).strftime(WEEKDAY_FORMAT)

                git_repo_file = 'https://github.com/emmagoke/hngx/blob/master/task_1/api.py'
                git_repo = 'https://github.com/emmagoke/hngx/tree/master/task_1'
                
                #  query parameters
                print(request.args)
                track = request.args.get('track')
                slack_name = request.args.get('slack_name')
                
                if slack_name and track:
                        response = {
			'slack_name': slack_name,
                        'current_day': weekday,
                        "utc_time": time_now,
			'track': track,
			'github_file_url': git_repo_file,
                        'github_repo_url': git_repo,
                        'status_code': 200,
			}
                
                        return jsonify(response), 200
                return jsonify(
                        {"error": 'Your include the query parameters slack_name and track'}), 400

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, host='0.0.0.0')
