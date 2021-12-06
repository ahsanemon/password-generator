import flask
from flask import Flask, request
from flask_restx import Resource, Api
import string
import secrets
from prometheus_flask_exporter import PrometheusMetrics

# pip install flask-restx
# pip install prometheus-flask-exporter


app = Flask(__name__)
api = Api(app)

metrics = PrometheusMetrics(app)

# Create an API that generates secure passwords.
# As input parameters the user must provide the
# minimum length,
# the number of special characters,
# the number of numbers and
# the number of passwords that shall be created.
# Then generate the passwords and return them in an array.

#


def get_pass(min_len, min_sc, min_num):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    tried = 0
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(min_len))
        tried = tried + 1
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum((True if c in string.punctuation else False) for c in password) >= min_sc
                and sum(c.isdigit() for c in password) >= min_num):
            print(f'Had to iterate {tried} times to get the password: {password}')
            return password
            # break


@api.route("/<int:min_length>,<int:min_sp_char>,<int:min_number>,<int:pass_count>")
class TodoSimple(Resource):

    def get(self, min_length, min_sp_char, min_number, pass_count):

        if pass_count < 1 or pass_count > 5:
            response = flask.Response("Invalid input - Max 1-5 password at a time")
            response.status_code = 400
            return response

        if min_length < 6 or min_length > 15:
            response = flask.Response("Invalid input - choose length between 6-15")
            response.status_code = 400
            return response

        if min_length < min_sp_char + min_number \
                or min_sp_char < 0 \
                or min_number < 0:
            response = flask.Response("Invalid input")
            response.status_code = 400
            return response

        n = 1
        passwords = []
        while n <= pass_count:
            n = n + 1
            passwords.append(get_pass(min_length, min_sp_char, min_number))

        return passwords


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",  port=5000)

