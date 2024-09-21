import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.chat_message_histories.upstash_redis import (
    UpstashRedisChatMessageHistory,
)
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
gemini_api_key = os.getenv("GEMINI_API_KEY")
langchain_api_key = os.getenv("LANGSMITH_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])


URL = ""
TOKEN =""
history = UpstashRedisChatMessageHistory(
    url=URL, token=TOKEN, ttl=500, session_id="chat1"
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    chat_memory=history,
)

# chain = prompt | model
chain = LLMChain(
    llm=model,
    prompt=prompt,
    verbose=True,
    memory=memory
)


# Prompt 1
q1 = { "input": "My name is Leon" }
resp1 = chain.invoke(q1)
print(resp1["text"])

# Prompt 2
q2 = { "input": "What is my name?" }
resp2 = chain.invoke(q2)
print(resp2["text"])