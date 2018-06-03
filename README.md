A small experiment on the amazon echo, where a user can leave a message for someone else to find.

### Setup

* Follow [instructions](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) to setup and configure aws-cli
* Set up new dynamo db table on aws with primary key `user_id`
* Run `pip install -r requirements.txt`
* Add .env file to the project root directory with `DYNAMO_TABLE_NAME={{ your table name }}` 
* Run `zappa init`
* Run `zappa deploy` and copy the endpoint that's returned
* Create a skill [here](https://developer.amazon.com/alexa/console/ask), using 3 intents (YesIntent, NoIntent and MessageIntent), copying cs_literal.txt for the MessageIntent schema, cs_yes for the YesIntent schema and cs_no for the NoIntent schema
* Set the endpoint to the url returned by zappa
* Either start testing in the test tab, or on an amazon echo device