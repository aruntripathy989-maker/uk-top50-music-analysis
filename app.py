import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import (
    load_data, artist_dominance, collaboration_analysis,
    explicit_analysis, album_analysis, duration_analysis,
    unique_artist_count
)

st.set_page_config(page_title="UK Top 50 Music Analysis", page_icon="🎵", layout="wide")

df = load_data("Atlantic_United_Kingdom.csv")

st.title("UK Top 50 Playlist Analysis")
st.markdown("**Atlantic Recording Corporation** | Market Structure and Artist Diversity")
st.divider()

st.sidebar.header("Filters")
show_explicit = st.sidebar.selectbox("Content Type", ["All", "Explicit Only", "Clean Only"])
collab_filter = st.sidebar.selectbox("Track Type", ["All", "Collaborations", "Solo"])

filtered_df = df.copy()
if show_explicit == "Explicit Only":
    filtered_df = filtered_df[filtered_df["is_explicit"] == True]
elif show_explicit == "Clean Only":
    filtered_df = filtered_df[filtered_df["is_explicit"] == False]
if collab_filter == "Collaborations":
    filtered_df = filtered_df[filtered_df["is_collab"] == True]
elif collab_filter == "Solo":
    filtered_df = filtered_df[filtered_df["is_collab"] == False]

appearances, aci = artist_dominance(filtered_df)
collab_count, solo_count, collab_ratio, top10_collab = collaboration_analysis(filtered_df)
explicit_share, explicit_by_rank = explicit_analysis(filtered_df)
avg_duration, top10_avg, bottom40_avg = duration_analysis(filtered_df)
unique_artists = unique_artist_count(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Unique Artists", unique_artists)
col2.metric("Collaboration %", f"{collab_ratio}%")
col3.metric("Explicit Content %", f"{explicit_share}%")
col4.metric("Avg Duration (min)", avg_duration)
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Dominant Artists")
    top10_artists = appearances.head(10)
    fig1 = px.bar(top10_artists, x="appearances", y="artist", orientation="h",
                  color="appearances", color_continuous_scale="Blues")
    fig1.update_layout(yaxis={"categoryorder": "total ascending"}, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Solo vs Collaboration")
    fig2 = px.pie(names=["Solo", "Collaboration"], values=[solo_count, collab_count],
                  color_discrete_sequence=["#636EFA", "#EF553B"], hole=0.4)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Explicit vs Clean Content")
    explicit_count = filtered_df["is_explicit"].sum()
    clean_count = len(filtered_df) - explicit_count
    fig3 = px.pie(names=["Explicit", "Clean"], values=[explicit_count, clean_count],
                  color_discrete_sequence=["#FF6B6B", "#51CF66"], hole=0.4)
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Album Type Distribution")
    album_dist = album_analysis(filtered_df)
    fig4 = px.bar(album_dist, x="album_type", y="count", color="album_type",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.subheader("Track Duration by Chart Position")
fig5 = px.scatter(filtered_df, x="position", y="duration_min",
                  color="is_explicit", hover_data=["song", "artist"],
                  color_discrete_map={True: "#FF6B6B", False: "#51CF66"})
fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.subheader("Raw Dataset")
st.dataframe(
    filtered_df[["date", "position", "song", "artist", "popularity",
                 "is_explicit", "is_collab", "album_type", "duration_min"]].reset_index(drop=True),
    use_container_width=True
)