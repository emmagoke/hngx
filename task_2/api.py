import os
from datetime import datetime, timezone
from os import getenv

import bleach

# from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from sqlalchemy.orm.exc import NoResultFound

from db import DB

# load_dotenv()

# print("mysql+mysqldb://{}:{}@{}/{}".format("goke", password, host, database))
db = DB()
FORMAT = "%Y-%m-%dT%H:%M:%SZ"
WEEKDAY_FORMAT = "%A"


def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)

    # Settings up CORS. Allow '*' for origins
    CORS(app, resource={r"/api/*": {"origin": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Context-Type, Authorization, True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", ["GET", "POST", "PUT", "DELETE"]
        )

        return response

    @app.route("/api", methods=["POST"])
    def home():
        name = request.json.get("name")
        email = request.json.get("email")

        if name and email:
            name = bleach.clean(name, strip=True)
            email = bleach.clean(email, strip=True)
            try:
                user = db.find_user_by(email=email)
                error = "email {} already registered".format(email)
                return jsonify({"error": error}), 400
            except NoResultFound:
                user = db.add_user(email, name)
                _id = user.id
                return (
                    jsonify({"id": _id, "email": email, "message": "user created"}),
                    201,
                )
        else:
            return (
                jsonify({"error": "you must provide a name and an email"}),
                400,
            )

    @app.route("/api/<user_id>", methods=["GET"], strict_slashes=False)
    def get_users(user_id) -> str:
        """This handles the post request of the users route."""

        try:
            if user_id is None:
                abort(404)
            user = db.find_user_by(id=user_id)
            _id = user.id
            user_email = user.email
            user_name = user.name
            return jsonify({"id": _id, "email": user_email, "name": user_name}), 200
        except NoResultFound:
            return jsonify({"message": "user not found"}), 404

    @app.route("/api/<user_id>", methods=["PUT"], strict_slashes=False)
    def update_users(user_id) -> str:
        """This handles the put request of the api/<user_id> route."""
        input_arg = dict()
        if request.json.get("name"):
            name = bleach.clean(request.json.get("name"), strip=True)
            input_arg["name"] = name
        if request.json.get("email"):
            email = bleach.clean(request.json.get("email"), strip=True)
            input_arg["email"] = email
        # TODO: uncomment print(name, email)

        try:
            if user_id is None:
                abort(404)
            if input_arg:
                user = db.update_user(user_id, **input_arg)
            else:
                abort(400)
            message = "Datails updated"
            return jsonify({"message": message}), 200
        except NoResultFound:
            return jsonify({"message": "user not found"}), 404
        else:
            return (
                jsonify({"error": "you must provide a name and email"}),
                400,
            )

    @app.route("/api/<user_id>", methods=["DELETE"], strict_slashes=False)
    def delete_user(user_id) -> str:
        """
        This handles the delete request of the api route
        using the user_id."""

        try:
            db.remove_user(user_id)
            message = "user was successfully deleted"
            return jsonify({"message": message}), 200
        except ValueError:
            return jsonify({"message": "user not found"}), 404

    return app

    @app.errorhandler(401)
    def unauthorized(error) -> str:
        """Unauthorized Error Handler"""
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error) -> str:
        """Forbidden Error Handler"""
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(error) -> str:
        """Not found handler"""
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def not_found(error) -> str:
        """Server Error handler"""
        return jsonify({"error": "Server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
