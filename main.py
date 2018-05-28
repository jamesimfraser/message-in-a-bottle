from flask import Flask
from flask_ask import Ask, statement, session, question

import boto3

app = Flask(__name__)
ask = Ask(app, "/")

def is_leaving_message():
    leaving_message = session.attributes.get("leaving_message")
    return leaving_message

def connect_to_db():
    db = boto3.resource("dynamodb")
    table = db.Table("message_bottle")

    return table

def get_user():
    table = connect_to_db()
    user_id = session.user.userId

    user = table.get_item(Key={"user_id": user_id})
    user_data = user.get("Item")

    if user_data is None:
        add_user({"user_id": str(user_id), "message": False})
        user = table.get_item(Key={"user_id": user_id})
        user_data = user.get("Item")

    return user_data

def add_user(data):
    table = connect_to_db()

    table.put_item(Item=data)

def update_user(user, message):
    table = connect_to_db()

    table.update_item(Key={"user_id": str(user)},
                      UpdateExpression="SET message = :val",
                      ExpressionAttributeValues={
                          ":val": message
                      })

@ask.launch
def start_skill():
    user = get_user()

    if not user["message"]:
        speech_text = "The bottle is empty, would you like to leave a message?"
    else:
        speech_text = "<speak>There is a message <break time=\"1s\" />{}.<break time=\"1s\" />The bottle is now empty, would you like to leave a message?</speak>".format(user["message"])
        update_user(user["user_id"], False)

    return question(speech_text)

@ask.intent("YesIntent")
def yes_response(yes_message):
    leaving_message = is_leaving_message()

    if leaving_message is None:
        session.attributes["leaving_message"] = True
        return question("Please leave your message.")
    else:
        return add_message(yes_message)

@ask.intent("NoIntent")
def no_response(no_message):
    leaving_message = is_leaving_message()

    if leaving_message is None:
        return statement("Ok, come back later. Maybe someone will have left a message.")
    else:
        return add_message(no_message)

@ask.intent("MessageIntent")
def add_message(message):
    user = get_user()
    leaving_message = is_leaving_message()

    if user["message"] or leaving_message is None:
        return start_skill()
    else:
        update_user(user["user_id"], message)
        return statement("Thank you, your message is now in the bottle.")

if __name__ == "__main__":
    app.run(debug=True)
