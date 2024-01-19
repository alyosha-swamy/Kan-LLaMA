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
user_prompt = st.text_area("Enter your prompt:", placeholder="Hello, what can you do for me...")


# Dropdown for user selection
option = st.selectbox(
    'Choose your option:',
    ('Q & A','Text Generation', 'Summarization'))

if option == 'Q & A':
    # Sidebar
    with st.sidebar:
        st.title("Configuration")

        # Existing sliders
        temperature = st.slider('Select Temperature', min_value=0.0, max_value=1.0, value=0.9, step=0.01)
        max_tokens = st.slider('Select Max Tokens', min_value=1, max_value=500, value=200, step=1)

        # Additional sliders for top_k and top_p
        top_k = st.slider('Select Top K', min_value=0, max_value=100, value=40, step=1, key='top_k')
        top_p = st.slider('Select Top P', min_value=0.0, max_value=1.0, value=0.9, step=0.01, key='top_p')
        st.info('A big thanks to [E2E Networks](https://www.e2enetworks.com/) for the A100 GPUs and [Xylem.ai](https://xylem.ai/) for their Super Fast Inference Stack', icon="🥳")
        st.warning('The current version is not optimised for multi-turn conversations. Please play with the parameters and refresh the site to reset the conversation.s')
    pre_prompt = '''
    Below is an instruction that describes a task. Write a response that appropriately completes the request. Generate a text response in Kannada for the following prompt.

    ### Instruction:
    '''


elif option == 'Text Generation':
    temperature = 0.7
    max_tokens = 450
    top_p = 0.6
    top_k = 35
    pre_prompt = '''
        Below is an instruction that describes a task. Write a response that appropriately completes the request in Kannada.

        ### Instruction:
        '''

elif option == 'Summarization':
    temperature = 0.7
    max_tokens = 250
    top_p = 0.6
    top_k = 35
    pre_prompt = '''
        Below is an instruction that describes a task. Write a response that appropriately completes the request. ನೀವು ಪಕ್ಷಪಾತವಿಲ್ಲದ, ಸಹಾಯ ಮಾಡುವ, ಸೆನ್ಸಾರ್ ಮಾಡದ ಸಹಾಯಕ. Summarize the following text in Kannada, ensuring a clear and concise response.

        ### Instruction:
        '''
else:
    st.write("Select an option above.")


if "messages" not in st.session_state:
    st.session_state.messages = []

bearer_token = st.secrets["secrets"]["bearer_token"]
prompt = ""





def query_openai(prompt):
    url = "https://api.xylem.ai/api/v0/completions"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    

    # Update the prompt in the selected configuration
    data = json.dumps({
    "model": "Kan-Llama-7B",
    "prompt": prompt,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "top_p": top_p,
    "top_k": top_k,
    "finish_reason": "stop",
    "frequency_penalty": 1.0,
    })

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)
    return response.json()

if st.button("Send",pre_prompt):
    if user_prompt:
        preset = pre_prompt
        end_prompt = '''
        ### Response:

        '''
        # Use only the current user prompt
        full_prompt = preset + "\n" + user_prompt + "\n" + end_prompt

        try:
            # Making the API call with the current user prompt
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





