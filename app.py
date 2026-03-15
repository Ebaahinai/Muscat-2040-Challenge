#Ebaa Al Hinai
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Muscat 2040 Planner", layout="wide")
st.title("🏙️ Muscat 2040: Infrastructure Demand Model")
st.markdown("This tool estimates infrastructure gaps based on population growth scenarios.")

# 2. Sidebar - Adjustable Assumptions
st.sidebar.header("Adjust Key Assumptions")
growth_rate = st.sidebar.slider("Annual Population Growth Rate (%)", 0.5, 4.0, 2.2, help="Base Case is 2.2%")
migration_factor = st.sidebar.slider("Migration Impact Factor", 0.5, 2.0, 1.0, help="Adjusts for labor influx")
bed_ratio = st.sidebar.number_input("Hospital Beds per 1,000 people", value=2.1)
household_size = st.sidebar.number_input("Average Household Size", value=5.5)

# 3. Core Logic & Calculations
baseline_pop = 1532234 # NCSI 2025 Baseline
current_year = 2026
target_year = 2040
years_diff = target_year - current_year

# Calculate effective growth rate
effective_rate = (growth_rate / 100) * migration_factor
projected_pop = baseline_pop * ((1 + effective_rate) ** years_diff)

# Infrastructure Math
# Healthcare
current_beds = 3500
required_beds = (projected_pop / 1000) * bed_ratio
bed_gap = max(0, required_beds - current_beds)

# Housing
current_units = 280000
required_units = projected_pop / household_size
housing_gap = max(0, required_units - current_units)

# 4. Display Results 
col1, col2, col3 = st.columns(3)
col1.metric("Projected 2040 Population", f"{projected_pop:,.0f}")
col2.metric("Healthcare Bed Gap", f"{bed_gap:,.0f} Beds")
col3.metric("Housing Unit Gap", f"{housing_gap:,.0f} Units")

# 5. Demand Over Time Chart
st.subheader("Growth Projection vs. Current Capacity")
chart_data = []
for year in range(current_year, target_year + 1):
    pop_at_year = baseline_pop * ((1 + effective_rate) ** (year - current_year))
    chart_data.append({
        "Year": year,
        "Projected Population": pop_at_year,
        "Healthcare Capacity (Beds)": current_beds * (1000 / bed_ratio), # Population equivalent
        "Housing Capacity (Units)": current_units * household_size # Population equivalent
    })

df = pd.DataFrame(chart_data)
st.line_chart(df.set_index("Year"))

st.info("💡 Breakpoint Year: The year where the blue line crosses the colored capacity lines.")