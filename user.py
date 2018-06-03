from flask_ask import statement, session, question
from dotenv import load_dotenv
import boto3
import os

class User():
    def __init__(self):
        load_dotenv(".env")
        db = boto3.resource("dynamodb")
        self.table = db.Table(os.getenv("DYNAMO_TABLE_NAME"))

    def is_leaving_message(self):
        leaving_message = session.attributes.get("leaving_message")
        return leaving_message

    def get_user(self):
        user_id = session.user.userId

        user = self.table.get_item(Key={"user_id": user_id})
        user_data = user.get("Item")

        if user_data is None:
            self.add_user({"user_id": str(user_id), "message": False})
            user = self.table.get_item(Key={"user_id": user_id})
            user_data = user.get("Item")

        return user_data

    def add_user(self, data):
        self.table.put_item(Item=data)

    def update_user(self, user_id, message):
        self.table.update_item(Key={"user_id": str(user_id)},
                        UpdateExpression="SET message = :val",
                        ExpressionAttributeValues={
                            ":val": message
                        })