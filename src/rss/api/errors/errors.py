from flask import jsonify, Response


def error(name: str, message: str, status_code: int) -> Response:
    response = jsonify({"error": name, "message": message})
    response.status_code = status_code
    return response


def bad_request(message: str) -> Response:
    return error("bad request", message, 400)


def unauthorized(message: str) -> Response:
    return error("unauthorized", message, 401)


def forbidden(message) -> Response:
    return error("forbidden", message, 403)


def not_found(message: str) -> Response:
    return error("not found", message, 404)


def internal_server_error(message: str) -> Response:
    return error("internal server error", message, 500)
