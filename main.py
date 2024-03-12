import streamlit as st
from db import initialize_prompt_and_text
from llm import generate_responses
from openai import OpenAI
import dotenv

dotenv.load_dotenv()


default_project_value = '''Category: Interior Painting
Travel Preferences: Professional must travel to my address.
Property Type: Home
Number of Rooms: 4 rooms
Surfaces: Walls
Ceiling Height: 8 - 10 feet (standard ceiling)
Painting Type: Repainting, with same color
Wall Condition: Excellent - clean and smooth
Paint Supplier: Homeowner or property manager
New Construction: No, this is not new construction
Room Prep Needed: No, I will move things out of the way myself
Zip Code: 33611
'''

### Sidebar
st.sidebar.title("Inputs")
#Hi {lead_first_name}, Buzz from the Bazaar here. We have limited stock of {product} available at {price} per {unit}. Interested?
st.sidebar.write('modify these then press Start/Restart on the right')
lead_first_name = st.sidebar.text_input("Lead First Name", value = "Susan")
product = st.sidebar.text_input("Product", value = "fidget spinners")
price = st.sidebar.text_input("Price", value = "$10.00")
unit = st.sidebar.text_input("Unit", value = "dozen")
business_type = st.sidebar.selectbox("Business Type", ['Retail','Wholesale/Distributor','Ecommerce','Other'], index = 0)
temp = 0#st.sidebar.slider("Temperature", min_value = 0.0, max_value = 1.0, value = 0.0, step = 0.1)
model = "gpt-4-1106-preview"#st.sidebar.selectbox("Model", ["gpt-4-1106-preview", "gpt-3.5-turbo"])
max_tokens = 200#st.sidebar.slider("Max Tokens", min_value = 50, max_value = 500, value = 200, step = 50)
####Main Bar
    

client = OpenAI()

st.title("AI Bazaar Chatbot")

if st.button("Start/Restart"):
    #clear all session state
    st.session_state.clear()
    st.session_state.messages = []
    st.session_state.lead_first_name = lead_first_name
    st.session_state.product = product
    st.session_state.price = price
    st.session_state.unit = unit
    st.session_state.business_type = business_type
    st.session_state.temp = temp
    st.session_state.model = model
    st.session_state.max_tokens = max_tokens
    st.rerun()

if "messages" in st.session_state:

    #Initialize system prompt and initial text
    if st.session_state.get('system_prompt') is None and st.session_state.get('initial_text') is None:
        initialize_prompt_and_text(st.session_state)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-1106-preview"

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type response here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            generate_responses(st.session_state)
            








