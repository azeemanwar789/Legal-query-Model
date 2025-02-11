import streamlit as st
from streamlit_option_menu import option_menu
import requests  # For making API calls to Hugging Face

# Set Hugging Face API Key for Authentication
HUGGING_FACE_API_KEY = "..."  # Replace with your API key
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"  # You can replace "gpt2" with other models

# Streamlit Page Configuration
st.set_page_config(
    page_title="LawAssist",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚖️"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .header {
        text-align: center;
        font-size: 40px;
        color: #4CAF50;
    }
    .subheader {
        text-align: center;
        font-size: 24px;
        color: #333;
    }
    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }
    .input-container select,
    .input-container input {
        padding: 10px;
        margin: 10px;
        width: 70%;
        border-radius: 10px;
        border: 1px solid #ddd;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to generate a response using Hugging Face's API
def generate_response(query, offense=None, section=None):
    try:
        # Customize the prompt to ensure it focuses on legal sections and offenses
        if offense and section:
            prompt = f"Legal Query: {query}\nPlease provide detailed information regarding the offense '{offense}' and legal section '{section}' based on the legal framework."
        else:
            prompt = f"Legal Query: {query}\nPlease provide a response based on legal principles and sections related to the query."

        # Debugging: Print the query being sent to Hugging Face
        st.write(f"Debug: Sending query to Hugging Face - {prompt}")
        
        # Prepare the payload for the API request
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 250,  # Limit response length
                "temperature": 0.7,  # Control creativity (0 = strict, 1 = creative)
                "num_return_sequences": 1  # Number of responses to generate
            }
        }
        
        # Set the Authorization header with the Hugging Face API key
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        
        # Make a POST request to Hugging Face's API
        response = requests.post(HUGGING_FACE_API_URL, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the generated text from the response
            generated_text = response.json()[0]['generated_text']
            return generated_text.strip()
        else:
            # Handle API errors
            st.error(f"Error: Unable to generate response. Status code: {response.status_code}")
            return "Sorry, I couldn't generate a response. Please try again later."
    except Exception as e:
        st.error(f"Error occurred while generating response: {e}")
        return "Sorry, an error occurred. Please try again."

# Main_door Page
def render_Main_door():
    st.markdown("<h1 class='header'>LawAssist</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subheader'>A Legal Offense Query System</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        Welcome to **LawAssist**, your go-to platform for exploring legal offenses, understanding their relevant sections, 
        and receiving personalized legal insights. Whether you are a legal professional, a student, or simply a curious 
        individual, this system empowers you to navigate the intricacies of the legal framework with confidence and clarity.
        """
    )

# Lawing Page
def render_Lawing():
    st.markdown("<h1 class='header'>Lawing</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subheader'>Enter your legal query</h3>", unsafe_allow_html=True)

    query = st.text_area("Enter your legal query:", height=150)

    if st.button("Submit Query"):
        if query.strip():
            st.success("Query submitted successfully!")
            st.write(f"**Query:** {query}")
            
            # Generate response using Hugging Face's API
            response = generate_response(query)
            
            # Display the response
            st.write("**Response:**")
            st.write(response)
        else:
            st.warning("Please enter a legal query.")

# Information Page
def render_information():
    st.markdown("<h1 class='header'>Information</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subheader'>Select an offense and legal section</h3>", unsafe_allow_html=True)

    offenses = ["Choose an offense", "Murder", "Theft", "Fraud", "Assault"]
    sections = ["Choose a legal section", "Section 302", "Section 379", "Section 420", "Section 351"]

    selected_offense = st.selectbox("Select an offense:", offenses)
    selected_section = st.selectbox("Select a legal section:", sections)

    if st.button("Submit Query"):
        if selected_offense == "Choose an offense" or selected_section == "Choose a legal section":
            st.error("Please select both an offense and a legal section.")
        else:
            st.success("Query submitted successfully!")
            st.write(f"**Offense:** {selected_offense}")
            st.write(f"**Legal Section:** {selected_section}")
            
            # Get the legal information based on the selected offense and section
            legal_info = generate_response("Provide a legal explanation", selected_offense, selected_section)
            
            # Display the legal information
            st.write("**Response:**")
            st.write(legal_info)

# Horizontal menu for navigation
selected = option_menu(
    None,
    ["Main_door", "Information", "Lawing"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#4CAF50"},
    }
)

# Route to the selected page
if selected == "Main_door":
    render_Main_door()
elif selected == "Information":
    render_information()
elif selected == "Lawing":
    render_Lawing()
