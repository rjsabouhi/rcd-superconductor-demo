import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from mpl_toolkits.mplot3d import Axes3D

# --- Symbolic Equations ---
def compute_coherence(theta, mu, entropy_grad):
    return 1 / (1 + theta * entropy_grad)

def compute_transit_time(mu, gamma):
    return mu / gamma

def compute_resistance(gamma):
    return 0.0 if gamma >= 0.6 else 1.0

# --- Real Material Reference ---
def get_known_materials():
    data = [
        {"name": "YBCO", "Tc": 93, "symbolic_gamma": 0.66667},
        {"name": "BSCCO", "Tc": 95, "symbolic_gamma": 0.66667},
        {"name": "HgBa2Ca2Cu3O8", "Tc": 133, "symbolic_gamma": 0.76923},
        {"name": "MgB2", "Tc": 39, "symbolic_gamma": 0.57142},
        {"name": "FeSe", "Tc": 8, "symbolic_gamma": 0.44444},
    ]
    return pd.DataFrame(data)

# --- 3D Plotting ---
def generate_surface_plot():
    theta_vals = np.linspace(0.01, 2.0, 50)
    entropy_vals = np.linspace(0.1, 10.0, 50)
    theta_grid, entropy_grid = np.meshgrid(theta_vals, entropy_vals)
    gamma_grid = 1 / (1 + theta_grid * entropy_grid)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(theta_grid, entropy_grid, gamma_grid, cmap='viridis')
    ax.set_xlabel("Θ (Clinging)")
    ax.set_ylabel("∇S (Entropy Gradient)")
    ax.set_zlabel("γ (Coherence)")
    ax.set_title("Symbolic Coherence Surface γ(Θ, ∇S)")
    return fig

# --- Streamlit App UI ---
st.set_page_config(page_title="Symbolic Superconductors", layout="wide")
st.title("Symbolic Superconductor Prediction Engine")
st.markdown("Use cognitive-symbolic inputs to explore and predict superconductive behavior in known and hypothetical materials.")

col1, col2 = st.columns(2)
with col1:
    theta = st.slider("Θ(T) — Clinging", 0.0, 2.0, 1.0, 0.01)
    mu = st.slider("μ(H, M, R) — Memory Tension", 0.0, 5.0, 1.0, 0.01)
    entropy_grad = st.slider("∇S — Entropy Gradient", 0.1, 10.0, 1.0, 0.1)

gamma = compute_coherence(theta, mu, entropy_grad)
tau_0 = compute_transit_time(mu, gamma)
resistance = compute_resistance(gamma)

with col2:
    st.metric("Coherence γ", f"{gamma:.5f}")
    st.metric("Synthetic Transit Time τ₀", f"{tau_0:.5f}")
    st.metric("Resistance at Tc", f"{resistance:.5f}")
    if gamma >= 0.6:
        st.success("Superconductive coherence likely.")
    else:
        st.warning("No symbolic superconductivity detected.")

# --- Known Comparison ---
st.subheader("Known Superconductor Comparison")
materials_df = get_known_materials()
materials_df["Δγ (vs current)"] = (materials_df["symbolic_gamma"] - gamma).abs().round(5)
st.dataframe(materials_df.style.highlight_min("Δγ (vs current)", color='lightgreen'), use_container_width=True)

# --- Coherence Landscape ---
st.subheader("Symbolic Coherence Landscape")
fig = generate_surface_plot()
st.pyplot(fig)
