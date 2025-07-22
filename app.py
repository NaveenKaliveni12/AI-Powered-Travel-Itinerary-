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
        "itinerary": "",
        "total_cost": calculate_budget(days, budget),
    }

    response = llm.invoke(itinerary_prompt.format_messages(city=state['city'], interests=','.join(state['interests']), days=state["days"], budget=state["budget"]))
    state["itinerary"] = response.content

    itinerary_text = f"""📍 **Destination:** {state['city']}
📆 **Duration:** {state['days']} days
💰 **Estimated Cost:** ${state['total_cost']}

📝 **Futuristic AI Itinerary:**
{state['itinerary']}"""

    return itinerary_text

# Streamlit UI
st.set_page_config(page_title="🚀 AI Travel Planner", page_icon="🌍", layout="wide")

# Custom CSS for futuristic styling
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #f1f1f1;
        font-family: 'Poppins', sans-serif;
    }
    .stButton button {
        background: linear-gradient(135deg, #ff7eb3, #ff758c);
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stSlider {
        color: #ff758c !important;
    }
    .stRadio label {
        font-size: 16px;
        color: #ff7eb3;
    }
    .full-image {
        width: 100%;
        height: auto;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# 🌍 Alpha GenAI Travel Planner")
st.markdown("### 🚀 Plan your dream trip with AI-generated recommendations!")

# Display futuristic image with updated parameter
st.image("An_ultra-futuristic_AI-powered_travel_planner_inte.png", use_container_width=True, caption="🔮 Welcome to the Future of Travel Planning!")

# Input Section
st.markdown("## 🎯 Select Your Travel Preferences")

col1, col2 = st.columns([1, 1])

with col1:
    city = st.text_input("🏙️ Destination", placeholder="Enter a city (e.g., Paris)")
    interests = st.text_input("🎨 Interests", placeholder="E.g., Museums, Food, Beaches")

with col2:
    days = st.slider("📆 Duration (Days)", 1, 14, 5)
    budget = st.radio("💰 Budget Category", ["Budget", "Mid-Range", "Luxury"], index=1, horizontal=True)

st.markdown("---")

# Generate Itinerary
if st.button("🚀 Generate Itinerary"):
    with st.spinner("🔮 Generating your futuristic itinerary..."):
        itinerary_text = travel_planner(city, interests, days, budget)
        st.success("✅ Itinerary Ready!")
        st.markdown(itinerary_text)

# AI Travel Chatbot Section
st.markdown("## 🤖 Ask Alpha GenAI Travel Assistant")

query = st.text_input("💬 Ask any travel-related question", placeholder="E.g., What are the best places to visit in Japan?")

if st.button("🔍 Ask AI"):
    with st.spinner("🤖 Thinking..."):
        chat_response = llm.invoke(query)
        st.success("✅ Answer Ready!")
        st.markdown(f"**AI Travel Assistant:** {chat_response.content}")

# Footer
st.markdown("---")
st.markdown("👾 **Powered by AI | Designed for the Future!**")
