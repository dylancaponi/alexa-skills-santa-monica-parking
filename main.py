from __future__ import print_function

from pprint import pprint

import requests


base_api = 'http://parking.api.smgov.net'
headers = {"Accept" : "application/json"}

def get_all_lots():
	r = requests.get(base_api + '/lots/', headers=headers)	
	return r.json()


def get_all_lot_names():
	for lot in get_all_lots():
		print lot['name']


def get_lot_matching(lot_name):
	r = requests.get(base_api + '/lots/matching/' + lot_name, headers=headers)
	return r.json()[0]


def get_lot_details(lot_name):
	lot = get_lot_matching(lot_name)
	print lot['description']
	print lot['available_spaces']
	print lot['street_address']


def get_lot_with_most_spaces():
	lot_with_most_spaces = None
	max_spaces = None
	for lot in get_all_lots():	
		if max_spaces < lot['available_spaces']:
			max_spaces = lot['available_spaces']
			lot_with_most_spaces = lot['name']
	return lot_with_most_spaces


# def recent_meter_events():
# 	r = requests.get(base_api + '/meters/events', headers=headers)
# 	pprint(r.json())

# def get_lot_names():

get_all_lot_names()
# print get_lot_matching('Beach House')
# get_lot_details('library')
# get_lot_with_most_spaces()
# recent_meter_events()


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Santa Monica parking information. " \
                    "Possible commands are, " \
                    "List parking structures," \
                    "My favorite parking lot is Structure 1," \
                    "Details for name of parking lot," \
                    "How is parking at name of parking lot"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Possible commands are, " \
                    "List parking lots," \
                    "My favorite parking lot is Structure 1," \
                    "Details for name of parking lot," \
                    "How is parking at name of parking lot" 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for checking parking in Santa Monica. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_lot_attributes(favorite_lot):
    return {"favoriteLot": favorite_lot}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")