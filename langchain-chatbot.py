#Importing necessary dependencies
import os
from dotenv import load_dotenv, dotenv_values
import anthropic
from langchain.llms import Anthropic
from langchain.chat_models import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
import streamlit as st
from gtts import gTTS
from io import BytesIO
import tempfile

#Using dotenv to store confidential datas
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

headers = {
  "authorization": st.secrets['auth_token'],
  "content-type": "application/json"
}

#Used the most basic model provided by Anthropic for this case
model = Anthropic(
                  model="claude-v1",
                  max_tokens_to_sample = 512,
                  temperature = 0.4
                  )
st.title("Solve your problem just ask your question to our bot? 🧠")
raw_prompt = st.text_input("Enter your question? ")
#The propmpt format the model understands
prompt = f"{anthropic.HUMAN_PROMPT} {raw_prompt}{anthropic.AI_PROMPT}"
response = model(prompt)
st.write(response)

#Using google-text-to-speech library
tts = gTTS(response, lang='en')

# Save audio to temporary file
with tempfile.NamedTemporaryFile(delete=False) as fp:
    tts.save(fp.name)
    audio_path = fp.name

# Read the audio file
with open(audio_path, 'rb') as f:
    audio_bytes = f.read()

# Play the audio
st.audio(audio_bytes, format='audio/mp3')
