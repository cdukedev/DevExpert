import os
import openai
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import mysql.connector
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
# for shorter memory
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set up MySQL connection
db = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE")
)

# Set up Slack API
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
auth_response = slack_client.auth_test()
bot_user_id = auth_response["user_id"]
# Event handler for app mentions


llm = ChatOpenAI(temperature=0.0)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)


@app.event("app_mention")
def handle_app_mentions(body, say):
    prompt = body["event"]["text"]
    user_id = body["event"]["user"]
    if user_id == bot_user_id:
        return

    # Remove @devexpert mention from the prompt
    prompt = prompt.replace("<@{}>".format(bot_user_id), "").strip()

    # Generate AI response using OpenAI API
    response = conversation.predict(
        input=prompt,
    )
    print(response)

    # Save conversation to MySQL database
    cursor = db.cursor()
    query = "INSERT INTO conversations (user_id, user_input, ai_response) VALUES (%s, %s, %s)"
    values = (user_id, prompt, response)
    cursor.execute(query, values)
    db.commit()

    say(response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
