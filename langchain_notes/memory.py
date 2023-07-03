# Best way to see how this works is to run it in a Jupyter Notebook


from langchain.memory import ConversationBufferWindowMemory
import warnings
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

warnings.filterwarnings('ignore')


memory = ConversationBufferWindowMemory(k=1)

memory.save_context({"input": "Hi"},
                    {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

memory.load_memory_variables({})

llm = ChatOpenAI(temperature=0.0)
memory = ConversationBufferWindowMemory(k=1)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

conversation.predict(input="Hi, my name is Andrew")

conversation.predict(input="What is 1+1?")

#   ____          _      _   _           _           _ 
#  / ___|___   __| | ___| \ | | ___  ___| |_ ___  __| |
# | |   / _ \ / _` |/ _ \  \| |/ _ \/ __| __/ _ \/ _` |
# | |__| (_) | (_| |  __/ |\  |  __/ (__| ||  __/ (_| |
#  \____\___/ \__,_|\___|_| \_|\___|\___|\__\___|\__,_|
                                                     


conversation.predict(input="What is my name?")
