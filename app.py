import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(layout="wide", page_title="AQI Predictor")
import warnings

warnings.filterwarnings("ignore")

# Function to load the Random Forest model
@st.cache_resource
def load_model():
    with open('D:\\FP\\AQI\\random_forest_regression_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Load the model once at the beginning
model = load_model()

# Function to predict AQI
def predict_aqi(features):
    prediction = model.predict(features)
    return prediction

# Function to fetch real-time weather data for Meerut
def fetch_weather_data():
    url = "https://the-weather-api.p.rapidapi.com/api/weather/meerut"

    headers = {
        "x-rapidapi-key": "e62bc6ccbfmsh69183f87eadefd4p1d3f67jsn866e91d4ea63",
        "x-rapidapi-host": "the-weather-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data:
                weather_data = data['data']
                return weather_data
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to display the Home page
def home():
    st.title("AQI Predictor for Meerut City")

    # Description text
    description_col, image_col = st.columns([2, 1])

    with description_col:
        st.write("Welcome to our latest update on the Air Quality Index (AQI) of Meerut! "
                 "Stay informed about the current air quality conditions in Meerut with real-time data and analysis on our webpage. "
                 "We provide comprehensive insights into air pollution levels, including PM2.5, PM10, ozone, carbon monoxide,"
                 " sulfur dioxide, and nitrogen dioxide concentrations. Our user-friendly interface ensures easy navigation "
                 "and access to vital information for residents, policymakers, and environmental enthusiasts alike. "
                 "Stay ahead of environmental challenges and make informed decisions to safeguard your health and the well-being of our city. "
                 "Explore the AQI of Meerut on our webpage today!"
                 "Join us in staying ahead of environmental challenges and making informed decisions to safeguard the health and well-being of our community. Explore the AQI of Meerut on our webpage today and take the first step towards a healthier future")

        st.write("Meerut's Air Quality Index (AQI) has witnessed notable fluctuations over the past six years, reflecting the dynamic interplay of industrial activities, vehicular emissions, and seasonal variations. Despite occasional improvements spurred by regulatory measures and public awareness initiatives, AQI levels have predominantly lingered in the moderate to poor range, highlighting persistent challenges in maintaining air quality standards. To mitigate these levels, concerted efforts are imperative, including promoting sustainable practices, enforcing environmental regulations, and raising public awareness about the detrimental effects of air pollution. Additionally, during periods of heightened AQI, individuals should take precautions such as limiting outdoor exposure, using indoor air purifiers, and wearing protective masks to safeguard their health. By addressing these concerns collectively, we can strive towards a cleaner and healthier environment for Meerut.")

    with image_col:
        st.image('D:\\FP\\40059.jpg', caption="Air Quality Index (AQI) for Meerut", width=421, use_column_width=True)

    # Fetch real-time weather data
    st.title("Real-time Weather Data for Meerut")
    st.write("Fetching real-time weather data...")

    # Fetch weather data for Meerut
    weather_data = fetch_weather_data()

    # Display the weather data
    if weather_data:
        aqi = weather_data.get('aqi')
        current_weather = weather_data.get('current_weather')
        temp = weather_data.get('temp')
        aqi_remark = weather_data.get('aqi_remark')

        st.write("AQI (Air Quality Index):", aqi)
        st.write("Current Weather Condition:", current_weather)
        st.write("Temperature:", temp, "°C")
        st.write("AQI Remark:", aqi_remark)
    else:
        st.error("Error fetching weather data. Please try again later.")
def about_us():
    st.title("About Us")
    st.write(
        "We are final-year students of the B.Tech CSE (Data Science) program at Meerut Institute of Engineering and Technology, Meerut. Our passion for technology and environmental science has driven us to develop an AQI Predictor specifically for our city, Meerut.")

    st.write(
        "In this project, we meticulously collected and analyzed air quality data from the Tutiempo website. By applying supervised machine learning algorithms, we have successfully created a model that predicts the Air Quality Index (AQI) for Meerut with an accuracy of 85%. Our model is built on the foundation of six years of historical data, and through rigorous testing and optimization, we have employed various machine learning techniques to enhance our predictions.")

    st.write(
        "Our project is not just a culmination of our academic journey but a step towards contributing to our community by providing real-time air quality insights. We believe that understanding and predicting air quality is crucial for the health and well-being of our residents.")

    st.write(
        "Looking ahead, our goal is to integrate unsupervised machine learning algorithms to further improve the accuracy and reliability of our predictions. We are committed to continuous learning and innovation, and we aspire to set a benchmark in environmental data science.")

    st.write("Join us in our journey towards a cleaner, healthier future for Meerut!")

    st.title("Meet Our Team")

    # Team member details
    #import streamlit as st

    team_members = [
        {
            "name": "Ayush Sharma",
            "position": "Team Leader - Backend Developer",
            "contact": "+91 9084626104",
            "image": "D:\\FP\\TeamImages\\mea.jpg"  # Provide the correct path to Ayush's image
        },
        {
            "name": "Dhariya Rajput",
            "position": "Team Member - Content Writer",
            "contact": "+91 9760666142",
            "image": "D:\\FP\\TeamImages\\dd.jpg"  # Provide the correct path to Dhariya's image
        },
        {
            "name": "Ankit .",
            "position": "Team Member - Content Writer",
            "contact": "+91 8126810022",
            "image": "D:\\FP\\TeamImages\\ankitimg.jpg"  # Provide the correct path to Ankit's image
        },
        {
            "name": "Sandeep Kumar",
            "position": "Team Member - UI Developer",
            "contact": "+91 7906774535",
            "image": "D:\\FP\\TeamImages\\sandeep2.jpg"  # Provide the correct path to Sandeep's image
        }
    ]

    # Create columns for each team member to display their details in a row
    cols = st.columns(4)  # Create 4 equal-width columns

    for idx, member in enumerate(team_members):
        with cols[idx]:
            st.image(member["image"], use_column_width=True, width=150)
            st.write(f"**{member['name']}**")
            st.write(f"*{member['position']}*")
            st.write(f"Contact: {member['contact']}")


# Function to display the Calculate page
def calculate():
    st.title("Calculate AQI of Meerut")
    st.write("Enter the Values")

    # Input features
    st.header('Input Features')

    # Add input features
    temperature = st.slider('Average Temperature (°C)', 0.0, 40.0, 25.0)
    max_temperature = st.slider('Maximum Temperature (°C)', 0.0, 50.0, 30.0)
    min_temperature = st.slider('Minimum Temperature (°C)', 0.0, 30.0, 20.0)
    pressure = st.slider('Atmospheric Pressure (hPa)', 900, 1100, 1000)
    humidity = st.slider('Average Relative Humidity (%)', 0.0, 100.0, 50.0)
    visibility = st.slider('Average Visibility (Km)', 0.0, 20.0, 10.0)
    wind_speed = st.slider('Average Wind Speed (Km/h)', 0.0, 50.0, 10.0)
    pm25 = st.slider('PM2.5 (µg/m³)', 0.0, 500.0, 50.0)

    # Create a dictionary of input features
    features = {'T': temperature,
                'TM': max_temperature,
                'Tm': min_temperature,
                'SLP': pressure,
                'H': humidity,
                'VV': visibility,
                'V': wind_speed,
                'PM2.5': pm25}

    # Convert to DataFrame
    input_df = pd.DataFrame([features])

    # Predict AQI
    if st.button('Predict AQI'):
        prediction = predict_aqi(input_df)
        st.subheader('Predicted AQI')
        st.write(prediction)

    # Display input features
    st.subheader('Input Features')
    st.write(input_df)

# Function to display the Contact Us page
def contact_us():
    st.title("Contact Us")
    st.write("Please fill out the form below to contact us.")

    # Example contact form
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Send form data to FormsFree
            form_data = {
                "Name": name,
                "Email": email,
                "Message": message
            }
            response = requests.post("https://formspree.io/f/moqgznbd", data=form_data)
            if response.ok:
                st.success("Your message has been successfully submitted!")
            else:
                st.error("Failed to submit the form. Please try again later.")
# Dictionary to map page names to functions
pages = {
    "Home": home,
    "About Us": about_us,
    "Calculate": calculate,
    "Contact Us": contact_us,
}

# Function to render the horizontal navigation bar
def render_navbar():
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f8f9fa;
        padding: 10px 20px;
        margin-left: 25px; /* Reducing the left margin */
    }
    .navbar img {
        height: 500px;
    }
    .navbar a {
        padding: 14px 20px;
        text-decoration: none;
        color: #000;
        font-size: 25px;
    }
    .navbar a:hover {
        background-color: #ddd;
        color: black;
    }
    </style>
    <div class="navbar">
        <div>
            <a href="/?page=Home">Home</a>
            <a href="/?page=About%20Us">About Us</a>
            <a href="/?page=Calculate">Calculate</a>
            <a href="/?page=Contact%20Us">Contact Us</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Get the selected page from the URL parameters
params = st.experimental_get_query_params()
page = params.get("page", ["Home"])[0]

# Render the navigation bar
render_navbar()

# Call the function corresponding to the selected page
if page in pages:
    pages[page]()
else:
    home()
