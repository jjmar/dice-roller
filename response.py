from flask import jsonify, g

DEFAULT_RESPONSE = {
        "response_type": "in_channel",
        "attachments": [
            {
                "color": "#36a64f",
                "pretext": "",
                "mrkdwn_in": [
                    "pretext"
                ],
                "fields": [
                    {
                        "title": "Dice",
                        "value": "",
                        "short": True
                    },
                    {
                        "title": "Rolls",
                        "value": "",
                        "short": True
                    }
                ]
            }
        ]
    }

HELP_RESPONSE = {
        "attachments": [
            {
                "fields": [
                    {
                        "title": "Command",
                        "value": "/roll XdY \n" \
                                 "/roll 2dY [a|adv|advantage]\n" \
                                 "/roll 2dY [d|disadv|disadvantage]\n" \
                                 "/roll XdY [+N]\n" \
                                 "/roll XdY [-N]",
                        "short": True
                    },
                    {
                        "title": "Result",
                        "value": "Roll a Y-sided dice X times\n" \
                                 "Roll 2 dice, take highest\n" \
                                 "Roll 2 dice, take lowest\n" \
                                 "Roll and add N to result\n" \
                                 "Roll and subtract N from result",
                        "short": True
                    }
                ]
            }
        ]
    }


def success_response():
    response = DEFAULT_RESPONSE.copy()

    # Pretext string
    response['attachments'][0]['pretext'] = '@{} rolled a *{}*'.format(g._command['author'], g._response['result'])

    # Dice String                                                                    )
    response['attachments'][0]['fields'][0]['value'] = '({}d{})'.format(g._command['num_dice'], g._command['dice_type'])

    if g._command['modifier']:
        response['attachments'][0]['fields'][0]['value'] += ' {}{}'.format(g._command['modifier'], g._command['modifier_amount'])

    if g._command['advantage']:
        response['attachments'][0]['fields'][0]['value'] += ' Advantage'
    elif g._command['disadvantage']:
        response['attachments'][0]['fields'][0]['value'] += ' Disadvantage'

    # Rolls String
    response['attachments'][0]['fields'][1]['value'] = '{}'.format(g._response['rolls'])

    return jsonify(response)


def help_response():
    response = HELP_RESPONSE.copy()
    return jsonify(response)


def error_response(data):
    response = {}
    response['text'] = data
    return jsonify(response)