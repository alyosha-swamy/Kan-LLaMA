import streamlit as st
import requests
import json

st.set_page_config(
    page_title="TENSOIC - Kan-LLaMA",
    page_icon="favicon.png",
)
st.title(":orange[Kan-LLaMA]")
st.header("", divider="rainbow")



# User input
user_prompt = st.text_input("Enter your prompt:", placeholder="Hello, what can you do for me...")
temperature = st.slider('Select Temperature', min_value=0.0, max_value=1.0, value=0.9, step=0.01)
max_tokens = st.slider('Select Max Tokens', min_value=1, max_value=500, value=200, step=1)

if "messages" not in st.session_state:
    st.session_state.messages = []

bearer_token = st.secrets["secrets"]["bearer_token"]



# Function to send a request to the OpenAI endpoint
def query_openai(prompt):
    url = "https://api.xylem.ai/api/v0/completions"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "model": "Kan-Llama-7B",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Button to send the prompt
# Button to send the prompt
if st.button("Send"):
    if user_prompt:
        pre_prompt = '''
        Below is an instruction that describes a task. Write a response that appropriately completes the request in Kannada.

        ### Instruction:
        '''
        end_prompt = '''
        ### Response:

        '''
        # Concatenate all previous messages to form the conversation history
        conversation_history = " ".join([message["content"] for message in st.session_state.messages])
        full_prompt = pre_prompt + "\n" + conversation_history + " " + user_prompt
        full_prompt = full_prompt + "\n" + end_prompt

        try:
            # Making the API call with the full conversation history
            response = query_openai(full_prompt)

            # Update session state with the user's prompt and model's response
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            response_text = response['choices'][0]['text']
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"API request error: {e}")
    else:
        st.warning("Please enter a prompt.")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

