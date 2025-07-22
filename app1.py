import streamlit as st
import requests
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

# Estimated cost per day based on budget category
COST_DATA = {
    "Budget": {"Hotel": 30, "Food": 10, "Transport": 5, "Attractions": 10, "Misc": 5},
    "Mid-Range": {"Hotel": 80, "Food": 25, "Transport": 15, "Attractions": 25, "Misc": 15},
    "Luxury": {"Hotel": 200, "Food": 50, "Transport": 50, "Attractions": 50, "Misc": 50},
}

# Function to estimate trip cost
def calculate_budget(days, budget):
    if budget in COST_DATA:
        return sum(COST_DATA[budget].values()) * days
    return "Invalid budget category"

# Prompt template for itinerary generation
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a futuristic AI travel assistant. Create a {days}-day itinerary for {city} based on {interests} with a {budget} budget. Provide a concise, futuristic-styled itinerary."),
    ("human", "Plan my trip")
])

# Function to generate travel itinerary
def travel_planner(city, interests, days, budget):
    state = {
        "city": city,
        "interests": [interest.strip() for interest in interests.split(',')],
        "days": days,
        "budget": budget,
        "total_cost": calculate_budget(days, budget),
    }

    response = llm.invoke(itinerary_prompt.format_messages(
        city=state['city'], 
        interests=','.join(state['interests']), 
        days=state["days"], 
        budget=state["budget"]
    ))
    
    state["itinerary"] = response.content if hasattr(response, 'content') else str(response)
    
    itinerary_text = f"""
    <div class='itinerary-box'>
        <h2>📍 {state['city']}</h2>
        <h3>📆 {state['days']} Days | 💰 Estimated Cost: ${state['total_cost']}</h3>
        <div class='itinerary-text'>
            {state['itinerary']}
        </div>
    </div>
    """
    return itinerary_text

# Streamlit UI
st.set_page_config(page_title="🚀 AI Travel Planner", page_icon="🌍", layout="wide")

# Custom CSS for futuristic styling & glowing effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f1f1f1;
        font-family: 'Orbitron', sans-serif;
    }
    .stButton button {
        background: linear-gradient(135deg, #ff7eb3, #ff758c);
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease-in-out;
        animation: pulse 1.5s infinite;
    }
    .stButton button:hover {
        transform: scale(1.1);
        box-shadow: 0px 0px 20px #ff758c;
    }
    @keyframes pulse {
        0% { box-shadow: 0px 0px 5px #ff758c; }
        50% { box-shadow: 0px 0px 15px #ff758c; }
        100% { box-shadow: 0px 0px 5px #ff758c; }
    }
    .glowing-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        text-shadow: 0px 0px 10px #ff7eb3;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        0% {text-shadow: 0 0 5px #fff, 0 0 10px #ff7eb3, 0 0 15px #ff758c;}
        100% {text-shadow: 0 0 10px #fff, 0 0 20px #ff7eb3, 0 0 30px #ff758c;}
    }
    .itinerary-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 15px #ff758c;
        margin: 20px 0;
    }
    .itinerary-text {
        font-size: 18px;
        color: #fff;
        padding: 10px;
        line-height: 1.5;
    }
    /* Glowing Input Fields */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #ff7eb3;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        color: #fff;
        text-shadow: 0px 0px 10px #ff7eb3;
        animation: glowInput 1.5s infinite alternate;
    }
    @keyframes glowInput {
        0% { box-shadow: 0px 0px 5px #ff7eb3; }
        100% { box-shadow: 0px 0px 15px #ff758c; }
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="glowing-title">🌍 Alpha GenAI Travel Planner</p>', unsafe_allow_html=True)
st.image("An_ultra-futuristic_AI-powered_travel_planner_inte.png", use_container_width=True, caption="🔮 Welcome to the Future of Travel Planning!")

# Input Section
st.markdown("## 🎯 Select Your Travel Preferences")

col1, col2 = st.columns([1, 1])

with col1:
    city = st.text_input("🏙️ Destination", placeholder="Enter a city (e.g., Paris)", key="glow_dest")
    interests = st.text_input("🎨 Interests", placeholder="E.g., Museums, Food, Beaches", key="glow_interests")

with col2:
    days = st.slider("📆 Duration (Days)", 1, 14, 5)
    budget = st.radio("💰 Budget Category", ["Budget", "Mid-Range", "Luxury"], index=1, horizontal=True)

st.markdown("---")

# Generate Itinerary
if st.button("🚀 Generate Itinerary"):
    with st.spinner("🔮 Generating your futuristic itinerary..."):
        itinerary_text = travel_planner(city, interests, days, budget)
        st.success("✅ Itinerary Ready!")
        st.markdown(itinerary_text, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("👾 **Powered by AI | Designed for the Future!**")
