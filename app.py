import streamlit as st

# Sample data: list of grants with eligibility criteria
grants = [
    {
        "name": "Small Business Innovation Grant",
        "description": "For small businesses with less than $500K annual revenue in innovative fields.",
        "min_revenue": 0,
        "max_revenue": 500000,
        "required_business_type": "small_business"
    },
    {
        "name": "Nonprofit Development Grant",
        "description": "For registered nonprofit organizations aiming to expand their community services.",
        "required_status": "nonprofit"
    },
    {
        "name": "Education Advancement Grant",
        "description": "For individuals or institutions seeking to improve educational opportunities.",
        "required_status": "education"
    },
    {
        "name": "Startup Seed Grant",
        "description": "For startups in early stages looking to scale up their operations.",
        "min_revenue": 0,
        "max_revenue": 100000,
        "required_business_type": "startup"
    },
    {
        "name": "Local Community Grant",
        "description": "For local businesses and community organizations in select states.",
        "states": ["NC", "VA", "SC"],
        "required_status": "small_business"
    },
    {
        "name": "State Arts Grant",
        "description": "For local artists and cultural organizations seeking to promote arts in their community.",
        "states": ["NY", "CA", "TX"],
        "required_status": "education"  # Using education here for demo; adjust as needed.
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

        # Check for local state requirements if applicable
        if "states" in grant:
            if user_info.get("state") not in grant["states"]:
                continue

        eligible.append(grant)
    return eligible

# Main Streamlit app
def main():
    st.title("Grant Finder Bot")
    st.write("Welcome to the Grant Finder Bot! Answer a few questions below to see which grants you might be eligible for.")

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
    
    # Ask for state for local grant opportunities
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
                # Optionally, you could list detailed requirements here
        else:
            st.write("Sorry, we couldn't find any grants that match your current profile. Please try adjusting your inputs or contact us for further consulting.")

    st.markdown("---")
    
    # Consulting & Pricing Section
    st.header("Consulting & Pricing")
    st.write("This Grant Finder feature is provided as part of our consulting services. Our pricing is designed to be flexible:")
    st.markdown("""
    - **Basic Grant Search:** \$29.99 per search session  
    - **Monthly Subscription:** \$99.99/month for unlimited searches and personalized consulting  
    - **Annual Package:** \$999.99/year for full-service grant consulting, including application support  
    """)
    st.write("Contact us for custom packages and enterprise solutions!")
    
if __name__ == '__main__':
    main()
