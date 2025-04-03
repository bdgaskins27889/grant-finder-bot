import streamlit as st
import pandas as pd

# Expanded grant dataset with eligibility criteria, levels, due dates, and requirements
grants = [
    # Federal Grants (National)
    {
        "name": "Federal Innovation Grant",
        "description": "A federal grant designed to support innovative small businesses across the nation.",
        "min_revenue": 0,
        "max_revenue": 1000000,
        "required_business_type": "small_business",
        "level": "Federal",
        "due_date": "2025-06-30",
        "requirements": "Submit business plan, revenue details, and innovation summary."
    },
    {
        "name": "Federal Research Grant",
        "description": "Supports academic research and innovation in educational institutions.",
        "required_status": "education",
        "level": "Federal",
        "due_date": "2025-05-15",
        "requirements": "Submit a detailed proposal and institutional affiliation."
    },
    {
        "name": "Federal Disaster Relief Grant",
        "description": "Provides funds for businesses and communities impacted by natural disasters.",
        "required_status": "small_business",
        "level": "Federal",
        "due_date": "2025-07-10",
        "requirements": "Documentation of disaster impact and recovery plan."
    },
    
    # State Grants
    {
        "name": "State Arts Grant",
        "description": "For local artists and cultural organizations seeking to promote arts in their community.",
        "states": ["NY", "CA", "TX"],
        "required_status": "education",  # Adjust as needed.
        "level": "State",
        "due_date": "2025-04-30",
        "requirements": "Portfolio, project summary, and budget."
    },
    {
        "name": "State Business Expansion Grant",
        "description": "Supports state-level small business expansion initiatives in targeted industries.",
        "min_revenue": 50000,
        "max_revenue": 500000,
        "states": ["FL", "TX", "CA", "NC"],
        "required_business_type": "small_business",
        "level": "State",
        "due_date": "2025-08-15",
        "requirements": "Financial statements, expansion plan, and business strategy."
    },
    {
        "name": "State Nonprofit Sustainability Grant",
        "description": "Assists nonprofit organizations with sustaining and growing community services.",
        "states": ["NC", "VA", "MI"],
        "required_status": "nonprofit",
        "level": "State",
        "due_date": "2025-09-01",
        "requirements": "Proof of nonprofit status, budget, and program overview."
    },
    
    # Local Grants
    {
        "name": "Local Community Grant",
        "description": "For local businesses and community organizations in select states.",
        "states": ["NC", "VA", "SC"],
        "required_status": "small_business",
        "level": "Local",
        "due_date": "2025-03-31",
        "requirements": "Local business verification and community development plan."
    },
    {
        "name": "Local Arts & Culture Grant",
        "description": "Provides funding for local arts and cultural projects in select cities.",
        "states": ["NY", "CA", "TX", "NC"],
        "required_status": "nonprofit",
        "level": "Local",
        "due_date": "2025-05-31",
        "requirements": "Project description, budget, and artistic portfolio."
    },
    
    # Other Specialized Grants
    {
        "name": "Nonprofit Development Grant",
        "description": "For registered nonprofit organizations aiming to expand their community services.",
        "required_status": "nonprofit",
        "level": "Specialized",
        "due_date": "2025-07-20",
        "requirements": "501(c)(3) verification and detailed program plan."
    },
    {
        "name": "Education Advancement Grant",
        "description": "For individuals or institutions seeking to improve educational opportunities.",
        "required_status": "education",
        "level": "Specialized",
        "due_date": "2025-06-15",
        "requirements": "Educational improvement plan and relevant credentials."
    },
    {
        "name": "Startup Seed Grant",
        "description": "For startups in early stages looking to scale up their operations.",
        "min_revenue": 0,
        "max_revenue": 100000,
        "required_business_type": "startup",
        "level": "Specialized",
        "due_date": "2025-04-15",
        "requirements": "Startup pitch, financial projections, and team background."
    },
    {
        "name": "Special Needs Grant",
        "description": "Tailored to support individuals and organizations addressing unique community needs.",
        "required_status": "other",
        "level": "Federal",
        "due_date": "2025-08-01",
        "requirements": "Special needs project proposal and impact assessment."
    }
]

def find_eligible_grants(user_info, level_filter=None):
    eligible = []
    for grant in grants:
        # Check revenue requirements if applicable
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

        # Apply level filter if selected
        if level_filter and grant.get("level", "").lower() != level_filter.lower():
            continue

        eligible.append(grant)
    return eligible

def main():
    st.set_page_config(page_title="Grant Guru", layout="wide")
    st.title("Grant Guru")
    st.write("Your smart, interactive grant search tool inspired by Instrumentl. Let our intelligent matching eliminate the guesswork and instantly discover your best-fit grant opportunities.")

    # Sidebar for user inputs and advanced filtering
    st.sidebar.header("Filter Your Grants")
    
    user_status = st.sidebar.selectbox(
        "Select your status:",
        ("small_business", "startup", "nonprofit", "education", "other")
    )
    
    annual_revenue = None
    if user_status in ["small_business", "startup"]:
        annual_revenue = st.sidebar.number_input("Enter your annual revenue (in USD)", min_value=0, step=1000)
    
    state = st.sidebar.text_input("Enter your state (2-letter code)", max_chars=2)
    state = state.upper().strip() if state else ""

    # Advanced filter: choose grant level
    level_filter = st.sidebar.selectbox(
        "Select Grant Level (optional):",
        ("All", "Federal", "State", "Local", "Specialized")
    )
    if level_filter == "All":
        level_filter = None

    # Sidebar button to search
    if st.sidebar.button("Search Grants"):
        user_info = {"status": user_status, "business_type": user_status, "state": state}
        if annual_revenue is not None and annual_revenue != 0:
            user_info["annual_revenue"] = annual_revenue

        eligible_grants = find_eligible_grants(user_info, level_filter)
        
        st.subheader("Eligible Grants")
        if eligible_grants:
            # Create a dataframe for a clean tabular view
            df = pd.DataFrame(eligible_grants)
            columns_order = ["name", "description", "due_date", "requirements", "level"]
            df = df[[col for col in columns_order if col in df.columns]]
            st.dataframe(df)
        else:
            st.write("No grants found matching your criteria. Try adjusting your filters or contact us for personalized support.")
    
    st.markdown("---")
    
    # Section: Powerful Features
    st.header("Our Powerful Features")
    st.markdown("""
    **Intelligent Matching:**  
    Eliminate the guesswork. Instantly discover your best-fit grant opportunities using our advanced matching engine.

    **Active RFP Database:**  
    Access 22k+ active RFPs. Over 250 new opportunities are added weekly by our in-house experts.

    **Active Funders Directory:**  
    Discover new good-fit funders within our database of 400k active grant makers.
    """)

    st.markdown("---")
    
    # Consulting & Pricing Section
    st.header("Consulting & Pricing")
    st.write("Grant Guru is part of our comprehensive consulting services. Choose a plan that works for you:")
    st.markdown("""
    - **Basic Grant Search:** \$29.99 per search session  
    - **Monthly Subscription:** \$99.99/month for unlimited searches and personalized consulting  
    - **Annual Package:** \$999.99/year for full-service grant consulting, including application support  
    """)
    st.write("Contact us for custom packages and enterprise solutions!")

if __name__ == '__main__':
    main()
