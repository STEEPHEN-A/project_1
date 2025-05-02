import streamlit as st

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymysql
from sqlalchemy import create_engine
import numpy as np



# --- DATABASE CONNECTION --- #
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/imdb_2024", echo=False)
connection = engine.connect()


# --- LOAD DATA --- #
df = pd.read_sql("SELECT * FROM movies_2024", con=connection)

# --- DATA CLEANING --- #
df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
df['Voting Counts'] = pd.to_numeric(df['Voting Counts'], errors='coerce')
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
# --- SIDEBAR FILTERS --- #
st.sidebar.header("🔍 Filter Options")
genre_filter = st.sidebar.multiselect("Select Genre", df['Genre'].dropna().unique())
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)

min_votes = int(np.nan_to_num(df['Voting Counts'].min(), nan=0))
max_votes = int(np.nan_to_num(df['Voting Counts'].max(), nan=100000))
vote_range = st.sidebar.slider("Select Voting Count Range", min_value=min_votes, max_value=max_votes, value=(min_votes, max_votes))

duration_filter = st.sidebar.selectbox("Duration Filter (in minutes)", ["All", "< 120 mins", "120–180 mins", "> 180 mins"])

# --- APPLY FILTERS --- #
filtered_df = df.copy()
if genre_filter:
    filtered_df = filtered_df[filtered_df['Genre'].isin(genre_filter)]
    filtered_df = filtered_df[filtered_df['Ratings'] >= min_rating]
    filtered_df = filtered_df[
        (filtered_df['Voting Counts'] >= vote_range[0]) &
        (filtered_df['Voting Counts'] <= vote_range[1])
    ]
    if duration_filter == "< 120 mins":
        filtered_df = filtered_df[filtered_df['Duration'] < 120]
    elif duration_filter == "120–180 mins":
        filtered_df = filtered_df[(filtered_df['Duration'] >= 120) & (filtered_df['Duration'] <= 180)]
    elif duration_filter == "> 180 mins":
        filtered_df = filtered_df[filtered_df['Duration'] > 180]

    # --- DISPLAY FILTERED DATA --- #
    st.subheader("🎬 Filtered Movies")
    st.dataframe(filtered_df)

    # --- VISUALIZATIONS --- #
    st.subheader("📊 Top 10 Movies by Rating and Voting Counts")

    # Get top 10 movies
    top_movies = df.sort_values(['Ratings', 'Voting Counts'], ascending=False).head(11)

    # Set up the plot
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Bar chart for voting counts
    ax1.bar(top_movies['Movie Name'], top_movies['Voting Counts'], color='skyblue', label='Voting Counts')
    ax1.set_ylabel('Voting Counts', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.set_xticklabels(top_movies['Movie Name'], rotation=45, ha='right')

    # Secondary y-axis for ratings
    ax2 = ax1.twinx()
    ax2.plot(top_movies['Movie Name'], top_movies['Ratings'], color='darkblue', marker='o', label='Ratings')
    ax2.set_ylabel('Ratings', color='darkblue')
    ax2.tick_params(axis='y', labelcolor='darkblue')

    # Add a title and show plot
    fig.tight_layout()
    st.pyplot(fig)

    st.subheader("📚 Genre Distribution")
    genre_count = df['Genre'].value_counts()
    st.bar_chart(genre_count)

    st.subheader("⏱ Average Duration by Genre")
    avg_duration = df.groupby('Genre')['Duration'].mean().sort_values()
    st.bar_chart(avg_duration)

    st.subheader("🗳 Voting Trends by Genre")
    avg_votes = df.groupby('Genre')['Voting Counts'].mean()
    st.bar_chart(avg_votes)

    # Rating Distribution (using seaborn for a better histogram)
    st.subheader("⭐ Rating Distribution")
    st.write("Histogram of Ratings")

    # Create a seaborn histogram
    fig, ax = plt.subplots()
    sns.histplot(df['Ratings'], bins=20, kde=False, ax=ax)

    # Set the labels correctly
    ax.set_xlabel("Ratings")
    ax.set_ylabel("Number of Movies")

    # Show the plot
    st.pyplot(fig)


    st.subheader("🎯 Top-Rated Movie Per Genre")
    top_per_genre = df.loc[df.groupby('Genre')['Ratings'].idxmax()]
    st.dataframe(top_per_genre[['Movie Name', 'Genre', 'Ratings']])

    st.subheader("🥧 Most Popular Genres by Voting")

    votes_by_genre = df.groupby('Genre')['Voting Counts'].sum().dropna()
    votes_by_genre = votes_by_genre[votes_by_genre > 0]

    # Plot the pie chart
    fig2, ax = plt.subplots(figsize=(2, 2), dpi=300)
    ax.pie(votes_by_genre, labels=votes_by_genre.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 6})
    ax.set_title('Most Popular Genres by Voting', fontsize=8)
    plt.tight_layout()  # Adjust layout to prevent overlap


    # Remove the axis label that shows up as the weird bar
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display it
    st.pyplot(fig2)


    st.subheader("📏 Duration Extremes")
    st.write("Shortest Movie:")
    st.dataframe(df.nsmallest(1, 'Duration'))
    st.write("Longest Movie:")
    st.dataframe(df.nlargest(1, 'Duration'))

    # --- CORRELATION ANALYSIS --- #
    st.subheader("🔗 Correlation Analysis: Ratings vs Voting Counts")
    st.write("Scatter plot showing the relationship between movie ratings and the number of votes.")

    # Remove missing values for this plot
    scatter_df = df[['Ratings', 'Voting Counts']].dropna()

    # Create the scatter plot
    fig_corr, ax_corr = plt.subplots()
    sns.scatterplot(data=scatter_df, x='Ratings', y='Voting Counts', ax=ax_corr)
    ax_corr.set_title("Ratings vs Voting Counts")
    ax_corr.set_xlabel("Ratings")
    ax_corr.set_ylabel("Voting Counts")

    # Display correlation coefficient
    corr_val = scatter_df['Ratings'].corr(scatter_df['Voting Counts'])
    st.markdown(f"*Correlation Coefficient (r):* {corr_val:.2f}")

    # Show the plot
    st.pyplot(fig_corr)


    st.subheader("🔥 Ratings by Genre (Heatmap)")
    heatmap_data = df.pivot_table(index='Genre', values='Ratings', aggfunc='mean')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", cbar=True, ax=ax3)
    st.pyplot(fig3)    