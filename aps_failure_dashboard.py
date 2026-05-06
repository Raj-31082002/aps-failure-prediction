import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Markov APS Failure Model
# ----------------------------

def aps_failure_model(fragment_count, component_area, system_health, total_area=80):
    if component_area >= total_area:
        component_area = total_area - 0.001

    survival_probability = (1 - component_area / total_area) ** fragment_count
    survival_probability = survival_probability * system_health

    failure_probability = 1 - survival_probability

    if failure_probability <= 0:
        expected_encounters = np.inf
    else:
        expected_encounters = 1 / failure_probability

    return survival_probability, failure_probability, expected_encounters


# ----------------------------
# Streamlit Page Setup
# ----------------------------

st.set_page_config(
    page_title="APS Failure Prediction System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ APS Failure Prediction System")
st.subheader("Markov-Based Survivability Prediction for Active Protection Systems")

st.write("""
This tool predicts the survivability of an Active Protection System (APS) based on 
fragment count, exposed component area, and current system health.
""")

# ----------------------------
# Sidebar Inputs
# ----------------------------

st.sidebar.header("Input Parameters")

fragment_count = st.sidebar.slider(
    "Number of Fragments",
    min_value=1,
    max_value=50,
    value=35
)

component_area = st.sidebar.slider(
    "Critical Component Area (ft²)",
    min_value=0.05,
    max_value=5.0,
    value=2.56,
    step=0.01
)

system_health = st.sidebar.slider(
    "Current System Health",
    min_value=0.1,
    max_value=1.0,
    value=1.0,
    step=0.01
)

total_area = st.sidebar.number_input(
    "Total Mounting Area (ft²)",
    min_value=10.0,
    max_value=200.0,
    value=80.0
)

# ----------------------------
# Prediction
# ----------------------------

survival_prob, failure_prob, expected_life = aps_failure_model(
    fragment_count,
    component_area,
    system_health,
    total_area
)

# ----------------------------
# Output Cards
# ----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Survival Probability", f"{survival_prob*100:.2f}%")

with col2:
    st.metric("Failure Probability", f"{failure_prob*100:.2f}%")

with col3:
    st.metric("Expected Encounters", f"{expected_life:.2f}")

# ----------------------------
# Risk Classification
# ----------------------------

st.markdown("## System Risk Status")

if failure_prob >= 0.60:
    st.error("🔴 HIGH RISK: APS is highly vulnerable under this fragment condition.")
elif failure_prob >= 0.30:
    st.warning("🟡 MEDIUM RISK: APS has moderate survivability risk.")
else:
    st.success("🟢 LOW RISK: APS is relatively safe under this condition.")

# ----------------------------
# Technical Result Table
# ----------------------------

st.markdown("## Technical Output Table")

result_df = pd.DataFrame({
    "Parameter": [
        "Fragment Count",
        "Component Area",
        "System Health",
        "Survival Probability",
        "Failure Probability",
        "Expected Functional Encounters"
    ],
    "Value": [
        fragment_count,
        f"{component_area:.2f} ft²",
        f"{system_health:.2f}",
        f"{survival_prob:.4f}",
        f"{failure_prob:.4f}",
        f"{expected_life:.2f}"
    ]
})

st.table(result_df)

# ----------------------------
# Graph 1: Fragment Count vs Failure Probability
# ----------------------------

st.markdown("## Effect of Fragment Count on Failure Probability")

frag_values = np.arange(1, 51)
failure_values = []

for k in frag_values:
    _, fp, _ = aps_failure_model(k, component_area, system_health, total_area)
    failure_values.append(fp)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(frag_values, failure_values, marker="o")
ax1.set_xlabel("Fragment Count")
ax1.set_ylabel("Failure Probability")
ax1.set_title("Fragment Count vs Failure Probability")
ax1.grid(True)

st.pyplot(fig1)

# ----------------------------
# Graph 2: Component Area vs Failure Probability
# ----------------------------

st.markdown("## Effect of Component Area on Failure Probability")

area_values = np.linspace(0.05, 5.0, 50)
failure_area_values = []

for area in area_values:
    _, fp, _ = aps_failure_model(fragment_count, area, system_health, total_area)
    failure_area_values.append(fp)

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(area_values, failure_area_values, marker="s")
ax2.set_xlabel("Component Area (ft²)")
ax2.set_ylabel("Failure Probability")
ax2.set_title("Component Area vs Failure Probability")
ax2.grid(True)

st.pyplot(fig2)

# ----------------------------
# Design Recommendation
# ----------------------------

st.markdown("## Design Recommendation")

if failure_prob >= 0.60:
    st.write("""
    The APS configuration shows a high probability of failure. To improve survivability,
    the exposed component area should be reduced, launcher and radar units should be hardened,
    and critical modules should be distributed or protected behind partial armor coverage.
    """)
elif failure_prob >= 0.30:
    st.write("""
    The APS configuration has moderate survivability risk. Further improvement can be achieved
    by reducing exposed area, improving component redundancy, and optimizing module placement.
    """)
else:
    st.write("""
    The APS configuration shows acceptable survivability. The current exposed area and system
    health provide a relatively safe operating condition for the selected fragment scenario.
    """)

# ----------------------------
# Thesis Explanation
# ----------------------------

st.markdown("## Thesis Explanation")

st.write("""
The model uses a two-state Markov reliability framework, where the APS is assumed to be either
functional or non-functional. The probability of remaining functional depends on the fragment count
and the exposed area of critical components. This dashboard provides a user-friendly decision-support
tool for evaluating APS survivability under fragment impact conditions.
""")
