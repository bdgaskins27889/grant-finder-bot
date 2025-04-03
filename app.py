import streamlit as st

# Expanded grant dataset with eligibility criteria and levels
grants = [
    # Federal Grants
    {
        "name": "Federal Innovation Grant",
        "description": "A federal grant designed to support innovative small businesses across the nation.",
        "min_revenue": 0,
        "max_revenue": 1000000,
        "required_business_type": "small_business",
        "level": "federal"
    },
    {
        "name": "Federal Research Grant",
        "description": "Supports academic research and innovation in educational institutions.",
        "required_status": "education",
        "level": "federal"
    },
    {
        "name": "Federal Disaster Relief Grant",
        "description": "Provides funds for businesses and communities impacted by natural disasters.",
        "required_status": "small_business",
        "level": "federal"
    },
    
    # State Grants
    {
        "name": "State Arts Grant",
        "description": "For local artists and cultural organizations seeking to promote arts in their community.",
        "states": ["NY", "CA", "TX"],
        "required_status": "education",  # Demo purpose; adjust as needed.
        "level": "state"
    },
    {
        "name": "State Business Expansion Grant",
        "description": "Supports state-level small business expansion initiatives in targeted industries.",
        "min_revenue": 50000,
        "max_revenue": 500000,
        "states": ["FL", "TX", "CA", "NC"],
        "required_business_type": "small_business",
        "level": "state"
    },
    {
        "name": "State Nonprofit Sustainability Grant",
        "description": "Assists nonprofit organizations with sustaining and growing community services.",
        "states": ["NC", "VA", "MI"],
        "required_status": "nonprofit",
        "level": "state"
    },
    
    # Local Grants
    {
        "name": "Local Community Grant",
        "description": "For local businesses and community organizations in select states.",
        "states": ["NC", "VA", "SC"],
        "required_status": "small_business",
        "level": "local"
    },
    {
        "name": "Local Arts & Culture Grant",
        "description": "Provides funding for local arts and cultural projects in select cities.",
        "states": ["NY", "CA", "TX", "NC"],
        "required_status": "nonprofit",
        "level": "local"
    },
    
    # Other Specialized Grants
    {
        "name": "Nonprofit Development Grant",
        "description": "For registered nonprofit organizations aiming to expand their community services.",
        "required_status": "nonprofit",
        "level": "other"
    },
    {
        "name": "Education Advancement Grant",
        "description": "For individuals or institutions seeking to improve educational opportunities.",
        "required_status": "education",
        "level": "other"
    },
    {
        "name": "Startup Seed Grant",
        "description": "For startups in early stages looking to scale up their operations.",
        "min_revenue": 0,
        "max_revenue": 100000,
        "required_business_type": "startup",
        "level": "other"
    },
    {
        "name": "Special Needs Grant",
        "description": "Tailored to support individuals and organizations addressing unique community needs.",
        "required_status": "other",
        "level": "federal"  # For demo purposes; could be federal or another level.
    }
]

# Function to filter grants based on user responses
def find_eligible_grants(user_info):
    eligible = []
    for grant in grants:
        # Check for revenue requirements if applicable
        if "max_revenue" in grant and "annual_revenue" in user_info:
            if not (grant["min_revenue"] <= user_info["annual_revenue"] <= grant["max_revenue"]):
                continue

        # Check for business type or status if applicable
        if "required_business_type" in grant:
            if user_info.get("business_type") != grant["required_business_type"]:
                continue
        if "required_status" in grant:
            if user_info.get("status") != grant["required_status"]:
                continue

        # Check for state requirements if applicable
        if "states" in grant:
            if user_info.get("state") not in grant["states"]:
                continue

        eligible.append(grant)
    return eligible

# Main Streamlit app
def main():
    st.title("Grant Guru")
    st.write("Welcome to Grant Guru – your friendly, all-knowing grant guide! Answer a few questions below, and we'll match you with local, state, federal, and other specialized grants tailored to your needs.")

    # Qualifying questions
    st.header("Step 1: Qualifying Questions")
    
    user_status = st.radio(
        "What best describes your current status?",
        ("small_business", "startup", "nonprofit", "education", "other")
    )
    
    # Only ask for revenue if they are a business or startup
    annual_revenue = None
    if user_status in ["small_business", "startup"]:
        annual_revenue = st.number_input("Enter your annual revenue (in USD)", min_value=0, step=1000)
    
    # Ask for state for local and state grant opportunities
    state = st.text_input("Enter your state (use the two-letter abbreviation, e.g., NC, NY, CA)", max_chars=2)
    state = state.upper().strip() if state else ""

    st.write("If you are a nonprofit or in education, revenue info is not required.")
    
    if st.button("Find Grants"):
        # Package user info for filtering
        user_info = {"status": user_status, "business_type": user_status, "state": state}
        if annual_revenue is not None and annual_revenue != 0:
            user_info["annual_revenue"] = annual_revenue
        
        eligible_grants = find_eligible_grants(user_info)
        
        st.header("Step 2: Eligible Grants")
        if eligible_grants:
            for grant in eligible_grants:
                st.subheader(grant["name"])
                st.write(grant["description"])
                if "level" in grant:
                    st.caption(f"Grant Level: {grant['level'].capitalize()}")
        else:
            st.write("Sorry, we couldn't find any grants that match your current profile. Please try adjusting your inputs or contact us for further consulting.")

    st.markdown("---")
    
    # Consulting & Pricing Section
    st.header("Consulting & Pricing")
    st.write("Grant Guru is offered as part of our comprehensive consulting services. Our pricing is designed to be flexible:")
    st.markdown("""
    - **Basic Grant Search:** \$29.99 per search session  
    - **Monthly Subscription:** \$99.99/month for unlimited searches and personalized consulting  
    - **Annual Package:** \$999.99/year for full-service grant consulting, including application support  
    """)
    st.write("Contact us for custom packages and enterprise solutions!")

if __name__ == '__main__':
    main()
