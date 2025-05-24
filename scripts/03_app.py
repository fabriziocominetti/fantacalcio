import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.title("Fantacalcio | Simulation Results")

# Load CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Sort teams alphabetically
df['team'] = pd.Categorical(df['team'], categories=sorted(df['team'].unique()), ordered=True)

# Dynamic layout: 2 rows, columns = half the number of teams
num_teams = df['team'].nunique()
if num_teams % 2 != 0:
    st.error("Number of teams must be even for a 2-row layout.")
    st.stop()

facet_wrap = num_teams // 2
rows = 2

# Create histogram
fig = px.histogram(
    df,
    x="rank",
    color="team",
    facet_col="team",
    facet_col_wrap=facet_wrap,
    opacity=0.6,
    nbins=10,
    category_orders={"team": sorted(df['team'].unique())},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

# Update layout
fig.update_layout(
    title="Frequency of Final Ranking by Team (10000 permutations)",
    height=350 * rows,
    showlegend=False,
    margin=dict(t=100, b=100),
    bargap=0.2,
    grid=dict(rows=rows, columns=facet_wrap, pattern="independent"),
    annotations=[]
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig.update_xaxes(dtick=1)
fig.update_xaxes(tickangle=0)

# Remove all x-axis titles
fig.for_each_xaxis(lambda axis: axis.update(title=None))
# Restore "Rank" title only for bottom row
for i in range(1, facet_wrap + 1):
    fig['layout'][f'xaxis{i}'].title.text = "Rank"



# Remove all y-axis titles
fig.for_each_yaxis(lambda axis: axis.update(title=None))
# Add title only for leftmost plots in each row
for i in [1, facet_wrap + 1]:
    fig['layout'][f'yaxis{i}'].title.text = "Simulations"

# Show plot
st.plotly_chart(fig, use_container_width=True)

# Download button
st.download_button(
    label="Download as HTML",
    data=fig.to_html(full_html=True, include_plotlyjs='cdn'),
    file_name="simulation_results.html",
    mime="text/html"
)
