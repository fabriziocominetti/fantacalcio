import streamlit as st
import pandas as pd
import plotly.express as px

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

# Main histogram
fig = px.histogram(
    df,
    x="rank",
    color="team",
    facet_col="team",
    facet_col_wrap=5,
    opacity=0.6,
    nbins=10,
    category_orders={"team": sorted(df['team'].unique())},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

# Update layout
fig.update_layout(
    title="Frequency of Final Ranking by Team (10000 permutations)",
    height=700,
    showlegend=False,
    margin=dict(t=100, b=100),
    bargap=0.2,  # Adds spacing between bars
)

# More space between facets
fig.update_layout(
    grid=dict(rows=2, columns=5, pattern="independent"),
    annotations=[]
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig.update_xaxes(dtick=1)
fig.update_xaxes(tickangle=0)

# Remove all x-axis titles
fig.for_each_xaxis(lambda axis: axis.update(title=None))
# Restore "Rank" title only for x-axes in second row (1–5)
for i in range(1, 6):
    fig['layout'][f'xaxis{i}'].title.text = "Rank"

# Remove all y-axis titles
fig.for_each_yaxis(lambda axis: axis.update(title=None))
# Add title only for leftmost plots in each row (e.g., yaxis1 and yaxis6)
fig['layout']['yaxis1'].title.text = "Simulations"
fig['layout']['yaxis6'].title.text = "Simulations"

st.plotly_chart(fig, use_container_width=True)

# Download plot
st.download_button(
    label="Download as HTML",
    data=fig.to_html(full_html=True, include_plotlyjs='cdn'),
    file_name="simulation_results.html",
    mime="text/html"
)
