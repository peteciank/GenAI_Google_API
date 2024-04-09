# Import necessary libraries
import streamlit as st  # Import Streamlit library for creating web application
import google.generativeai as genai  # Import Google's generative AI library
import google.ai.generativelanguage as glm  # Import Google's generative language library
import os  # Import os module for operating system functionalities

# Configure Google API key
GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']  # Retrieve Google API key from Streamlit secrets
genai.configure(api_key=GOOGLE_API_KEY)  # Configure generative AI with API key

# Define model configuration
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

# Set page configuration
st.set_page_config(page_title="Gemini-ChatBot", layout='wide')

# Display title and description
st.title('Gemini-ChatBot')
st.markdown("""
Welcome to Gemini-ChatBot! This interactive chatbot is powered by Google's generative AI.
Feel free to ask anything and enjoy the conversation!
""")

# Create sidebar for selecting input type
with st.sidebar:
    st.title('Type of input:')
    add_radio = st.radio(
        "Type of input",
        ("Text ✏", "Image 📷"),
        key='input_param',
        label_visibility='collapsed'
    )

# Initialize or update previous input type in session state
if "previous_input_type" not in st.session_state:
    st.session_state.previous_input_type = None

if st.session_state.previous_input_type != add_radio:
    st.session_state.messages = []
    st.session_state.previous_input_type = add_radio

# Initialize or update messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# Process input based on selected input type
if add_radio == 'Text ✏':
    model = genai.GenerativeModel(model_name="gemini-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)
    prompt = st.chat_input("Ask anything")

    if prompt:
        message = prompt
        st.session_state.messages.append({
            "role": "user",
            "parts": [message],
        })
        with st.chat_message("user"):
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role": "model",
            "parts": [response.text],
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
            "role": "user",
            "parts": [image_input],
        })
        with st.chat_message("user"):
            st.image(image_input, width=300)
            st.markdown(prompt)
        response = model.generate_content(st.session_state.messages)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response.text)
        st.session_state.messages.append({
            "role": "model",
            "parts": [response.text],
        })
# Display badge
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img src="https://raw.githubusercontent.com/peteciank/public_files/main/mugshot_light.png" alt="Profile Picture" style="border-radius: 50%; margin-right: 20px;width: 50px; height: 50px;">
        <div>
            <p style="font-weight: bold; margin-bottom: 5px;">Created by Pete Ciank</p>
            <p style="margin: 0;">Streamlit enthusiast, Tech Lover, Product and Project Manager 💪</p>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.expander("📃 Check my personal links, Resume, Cover Letter and More", expanded=False):
    st.markdown('📖 My [LinkedIn](https://www.linkedin.com/in/pedrociancaglini/) Profile.')
    st.markdown('🌎 My [Website](https://sites.google.com/view/pedrociancaglini)')
    st.markdown('👩‍💻 My [Github](https://github.com/peteciank/)')
    st.markdown('🔽 [Download](https://github.com/peteciank/public_files/blob/main/Ciancaglini_Pedro_Resume_v24.pdf) my Resume')
    st.markdown('🔽 [Download](https://github.com/peteciank/public_files/blob/main/Cover%20Letter.pdf) my Letter')
