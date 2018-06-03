from flask import Flask
from flask_ask import Ask, statement, session, question

from user import User

app = Flask(__name__)
ask = Ask(app, "/")
current_user = User()


@ask.launch
def start_skill():
    user = current_user.get_user()

    if not user["message"]:
        speech_text = "The bottle is empty, would you like to leave a message?"
    else:
        speech_text = "<speak>There is a message <break time=\"1s\" />{}.<break time=\"1s\" />The bottle is now empty, would you like to leave a message?</speak>".format(user["message"])
        current_user.update_user(user["user_id"], False)

    return question(speech_text)

@ask.intent("YesIntent")
def yes_response(yes_message):
    leaving_message = current_user.is_leaving_message()

    if leaving_message is None:
        session.attributes["leaving_message"] = True
        return question("Please leave your message.")
    else:
        return add_message(yes_message)

@ask.intent("NoIntent")
def no_response(no_message):
    leaving_message = current_user.is_leaving_message()

    if leaving_message is None:
        return statement("Ok, come back later. Maybe someone will have left a message.")
    else:
        return add_message(no_message)

@ask.intent("MessageIntent")
def add_message(message):
    user = current_user.get_user()
    leaving_message = current_user.is_leaving_message()

    if user["message"] or leaving_message is None:
        return start_skill()
    else:
        current_user.update_user(user["user_id"], message)
        return statement("Thank you, your message is now in the bottle.")

if __name__ == "__main__":
    app.run(debug=True)
