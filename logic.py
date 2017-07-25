from flask import g
import re
from random import randint
from error import DiceError

DICE_REGEX = "(\d+)d(\d+)"
MODIFIER_REGEX = "(\+|\-)(\d+)"
INVALID_USAGE_ERROR = "Sorry that command failed for some reason. See /roll help for usage instructions"
ADVANTAGE_STRINGS = ["a", "adv", "advantage"]
DISADVANTAGE_STRINGS = ["d", "disadv", "disadvantage"]


def generate_command(data):
    command = {
        'author': data['user_name'],
        'num_dice': None,
        'dice_type': None,
        'advantage': False,
        'disadvantage': False,
        'modifier': None,
        'modifier_amount': None
    }

    arguments = data['text'].split()

    if len(arguments) == 0 or len(arguments) > 3:
        raise DiceError(INVALID_USAGE_ERROR)

    # Parse dice roll
    diceRoll = re.search(DICE_REGEX, arguments[0])
    if not diceRoll:
        raise DiceError(INVALID_USAGE_ERROR)
    else:
        command['num_dice'] = diceRoll.groups()[0]
        command['dice_type'] = diceRoll.groups()[1]
        arguments.remove(diceRoll.string)

    # Parse Advantage or Disadvantage
    if set(ADVANTAGE_STRINGS).intersection(arguments):
        command['advantage'] = True
        arguments.remove(set(ADVANTAGE_STRINGS).intersection(arguments).pop())

    if set(DISADVANTAGE_STRINGS).intersection(arguments):
        command['disadvantage'] = True
        arguments.remove(set(DISADVANTAGE_STRINGS).intersection(arguments).pop())

    if command['advantage'] and command['disadvantage']:
        raise DiceError(INVALID_USAGE_ERROR)

    # Parse modifier
    if arguments:
        modifier = re.search(MODIFIER_REGEX, arguments[0])
        if not modifier:
            raise DiceError(INVALID_USAGE_ERROR)
        else:
            command['modifier'] = modifier.groups()[0]
            command['modifier_amount'] = modifier.groups()[1]
            arguments.remove(modifier.string)

    g._command = command


def calculate_roll():
    response = {
        'rolls': [],
        'result': 0
    }

    for _ in range(int(g._command['num_dice'])):
        roll = randint(1, int(g._command['dice_type']))
        response['rolls'].append(roll)
        response['result'] += roll

    if g._command['advantage'] and len(response['rolls']) == 2:
        response['result'] -= min(response['rolls'])

    if g._command['disadvantage'] and len(response['rolls']) == 2:
        response['result'] -= max(response['rolls'])

    if g._command['modifier'] == '+':
        response['result'] += int(g._command['modifier_amount'])
    elif g._command['modifier'] == '-':
        response['result'] -= int(g._command['modifier_amount'])

    if response['result'] < 0:
        response['result'] = 0

    g._response = response




