from flask import Flask, jsonify


def register_routes(app: Flask):
    @app.route("/foo")
    def get_foo():
        return jsonify({})
