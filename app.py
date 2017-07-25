from flask import Flask, request, g
from error import DiceError
from logic import generate_command, calculate_roll
import os
from response import success_response, error_response, help_response

app = Flask(__name__)

SECRET_TOKEN = os.environ['DICE_TOKEN']
TEAM_ID = os.environ['DICE_TEAM_ID']


@app.route('/roll', methods=['POST'])
def roll():
    validate_authenticity(request.form['token'], request.form['team_id'])
    if not generate_command(request.form):
        return help_response()
    calculate_roll()
    return success_response()


def validate_authenticity(request_token, request_team_id):
    if request_token != SECRET_TOKEN:
        raise DiceError(message="Authentication Failed: Invalid token")

    if request_team_id != TEAM_ID:
        raise DiceError(message="Authentication Failed: Invalid team_id")

    return None


@app.errorhandler(DiceError)
def dice_error(e):
    return error_response(e.message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4390)