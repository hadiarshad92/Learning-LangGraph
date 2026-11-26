import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# define config
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# session state -> dict -> that does not refresh
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# {'role': 'user', 'content': 'hi'}
# {'role': 'assistant', 'content': 'hello'}


user_input = st.chat_input('Type here')
if user_input:
    # first add the message to user history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # streaming messages
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadat in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
 