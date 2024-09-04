import streamlit as st
import random
import time
import requests
import database_connectivity


def stream_generator(response):
    split = response.split('\n')
    for sentence in split:
      for word in sentence.split():
          yield word + " "
          time.sleep(0.1)
      yield "\n\n"
    


def store_converstation_into_db(user_reponse, bot_response):
        try:
            database_connectivity.bot_user_response_storage(user_reponse, bot_response)
        except Exception as e:
            print("error in storage")
            print(e)

        



def invoking_reset_api(question):
    print(question)
    store_converstation_into_db(question, "user")
    url = "http://localhost:5005/webhooks/rest/webhook"
    data = {"message": question}
    response = requests.post(url, json=data)
    final_resp = response.json()
    print(final_resp)
    temp_resp = ""
    for resp in final_resp:
        temp_resp+=resp['text']    
    print(temp_resp)
    return temp_resp

    




st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        print(prompt)
        response=invoking_reset_api(prompt)
        store_converstation_into_db(prompt, response)
        response = st.write_stream(stream_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})