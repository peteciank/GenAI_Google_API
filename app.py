import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
import PIL 
import io

GOOGLE_API_KEY= st.secrets['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

# model config
generation_config = {
"temperature": 0.9,
"top_p": 1,
"top_k": 1,
"max_output_tokens": 2048,
}

safety_settings = [
{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
},
{
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
},
{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
},
{
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
},
]

st.set_page_config(page_title="Gemini-ChatBot", layout = 'wide')

st.title('Gemini-ChatBot')
st.markdown("""
Welcome to Gemini-ChatBot! This interactive chatbot is powered by Google's generative AI.
Feel free to ask anything and enjoy the conversation!
""")

# Using "with" notation
with st.sidebar:
    st.title('Type of input:')
    add_radio = st.radio(
        "Type of input",
        ("Text ✏", "Image 📷"),
        key = 'input_param',
        label_visibility='collapsed'
    )

# Initialize previous_input_type in session_state if it doesn't exist
if "previous_input_type" not in st.session_state:
    st.session_state.previous_input_type = None

# Check if the input type has changed
if st.session_state.previous_input_type != add_radio:
    # Clear the messages
    st.session_state.messages = []
    # Update previous_input_type
    st.session_state.previous_input_type = add_radio

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])


if add_radio == 'Text ✏':
    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    prompt = st.chat_input("Ask anything")

    if prompt:
        message = prompt
        st.session_state.messages.append({
            "role":"user",
            "parts":[message],
        })
        with st.chat_message("user"):
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role":"model",
            "parts":[response.text],
        })

elif add_radio == 'Image 📷':
    st.warning("Please upload an image and ask a question! Do not just send a text prompt, Gemini doesnt support that yet.", icon="🤖")
    model = genai.GenerativeModel('gemini-pro-vision',
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    prompt = st.chat_input("Ask anything")


    if image and prompt:
        st.session_state.messages = []
        # save image to buffer
        buffer = io.BytesIO()
        PIL.Image.open(image).save(buffer, format="JPEG") 
        image_input = PIL.Image.open(buffer)
        st.session_state.messages.append({
            "role":"user",
            "parts":[image_input],
        })
        with st.chat_message("user"):
            st.image(image_input, width=300)
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role":"model",
            "parts":[response.text],
        })
