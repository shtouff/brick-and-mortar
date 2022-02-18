from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_errorhandlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_werkzeug_exception(err):
        """
        This intercepts every HTTPException from werkzeug and tries to display it smartly in JSON.
        """
        if err.code and 400 <= err.code < 500:
            data = getattr(err, "data", None)
            if data:
                # error was triggered by the user, ok to expose him the reason
                headers = data.get("headers", None)
                messages = data.get("messages", None)

                if headers:
                    return jsonify({"message": messages}), err.code, headers
                elif messages:
                    return jsonify({"message": messages}), err.code
                else:
                    return jsonify({"message": str(data)}), err.code
            else:
                return (
                    jsonify(
                        {"message": err.description if err.description else str(err)}
                    ),
                    err.code,
                )
        elif err.code:
            # we don't want to expose the error
            return jsonify(), err.code
