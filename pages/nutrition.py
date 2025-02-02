import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="Nutrition Calculator", layout="wide")

# Custom CSS for gradient background and styling
st.markdown("""
<style>
    
    .stApp {
        background-color: #4a90e2;
    }
    
    
    
    /* Title styling */
    .main-title {
        color: #4B0082;
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Section headers */
    .section-header {
        color: rgba(255, 255, 255,0);
        font-size: 2em;
        margin-bottom: 15px;
        font-weight: bold;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #333;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #333;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #ADD8E6, #D8B0FF);
        color: #4B0082;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    /* Metrics styling */
    .nutrition-metric {
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Error message styling */
    .success-msg {
        color: #4CAF50;
        font-weight: bold;
    }
    
    .error-msg {
        color: #FF5252;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Configure Google Gemini API key
genai.configure(api_key="AIzaSyDhge203wnvNPMrkCaf76Miy8l4xraXv5E")

# Main title with custom styling
st.markdown('<h1 class="main-title">Nutrition Calculator & Meal Suggestions</h1>', unsafe_allow_html=True)

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<p class="section-header">Daily Calorie Target</p>', unsafe_allow_html=True)
    target_calories = st.number_input("Set your daily calorie goal:", min_value=1, value=2000)
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'dish_entries' not in st.session_state:
    st.session_state.dish_entries = []

def get_nutrition_from_gemini(dish_name):
    """Fetch nutrition data using Google Gemini API and handle errors."""
    prompt = f"Analyze the nutritional content of: {dish_name}\n" \
             "Provide only the following values in this exact format:\n" \
             "calories: [number]\nprotein: [number]\ncarbs: [number]\nfat: [number]"

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip().split("\n")
        
        expected_keys = ["calories", "protein", "carbs", "fat"]
        nutrition = {}

        for line in response_text:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                if key in expected_keys:
                    try:
                        nutrition[key] = float(value)
                    except ValueError:
                        st.error(f"Invalid value for {key}: {value}")

        for key in expected_keys:
            nutrition.setdefault(key, 0.0)

        return nutrition

    except Exception as e:
        st.error(f"Error fetching nutrition data: {e}")
        return None

# Dish Input Form in a single white box
# Dish Input Form in a single white box
st.markdown('<div class="custom-box">', unsafe_allow_html=True)
st.markdown('<p class="section-header">🍽️ Add New Dish</p>', unsafe_allow_html=True)

with st.form("dish_form"):
    dish_name = st.text_input("Dish Name:", placeholder="Enter dish name...")
    quantity = st.number_input("Quantity (servings):", min_value=1, value=1)
    submit_button = st.form_submit_button("➕ Add Dish")

st.markdown('</div>', unsafe_allow_html=True)

if submit_button and dish_name:
    nutrition = get_nutrition_from_gemini(dish_name)
    if nutrition:
        st.session_state.dish_entries.append({'name': dish_name, 'quantity': quantity, 'nutrition': nutrition})
        st.markdown('<p class="success-msg">✅ Dish added successfully!</p>', unsafe_allow_html=True)


# Display added dishes in a custom box
st.markdown('<p class="section-header">Your Meal Plan</p>', unsafe_allow_html=True)
if not st.session_state.dish_entries:
    st.write("No dishes added yet. Start by adding your first dish above!")
else:
    for i, entry in enumerate(st.session_state.dish_entries):
        with st.container():
            st.markdown(f"""
            <div class="nutrition-metric">
                <h3>{entry['name']} × {entry['quantity']}</h3>
                <p>Calories: {entry['nutrition']['calories']} | 
                   Protein: {entry['nutrition']['protein']}g | 
                   Carbs: {entry['nutrition']['carbs']}g | 
                   Fat: {entry['nutrition']['fat']}g</p>
            </div>
            """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Calculate and display total nutrition
def calculate_total_nutrition(dishes):
    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for dish in dishes:
        for nutrient in totals:
            totals[nutrient] += dish['nutrition'][nutrient] * dish['quantity']
    return totals

if st.session_state.dish_entries:
    total_nutrition = calculate_total_nutrition(st.session_state.dish_entries)
    
    st.markdown('<p class="section-header">Total Nutrition Summary</p>', unsafe_allow_html=True)
    
    # Create columns for nutrition metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="nutrition-metric">
            <h4>Calories</h4>
            <p>{total_nutrition['calories']:.1f} kcal</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="nutrition-metric">
            <h4>Protein</h4>
            <p>{total_nutrition['protein']:.1f}g</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="nutrition-metric">
            <h4>Carbs</h4>
            <p>{total_nutrition['carbs']:.1f}g</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="nutrition-metric">
            <h4>Fat</h4>
            <p>{total_nutrition['fat']:.1f}g</p>
        </div>
        """, unsafe_allow_html=True)

    # Calorie target comparison
    calorie_diff = target_calories - total_nutrition['calories']
    if calorie_diff < 0:
        st.markdown(f'<p class="error-msg">⚠️ You are {abs(calorie_diff):.1f} calories over your target!</p>', unsafe_allow_html=True)
    elif calorie_diff > 0:
        st.markdown(f'<p class="success-msg">🎯 You have {calorie_diff:.1f} calories remaining</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="success-msg">✨ Perfect! You\'ve met your calorie target!</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")  # Adds a horizontal separator

st.subheader("AI Assisstant")


if st.button("Back to AI Assisstant"):
    st.switch_page("app.py")
