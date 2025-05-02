# 🎬 IMDB Movie Explorer Dashboard

A Streamlit-powered interactive dashboard that allows users to explore, analyze, and visualize IMDB movie data.

## 📂 Project Structure

- `streamlit.py`: Main Streamlit app for data filtering and visualization.
- `IMDB_movies_cleaned.csv`: Cleaned dataset of movies used for preprocessing or testing (not used directly in app; actual data is pulled from a MySQL database).
- `scrappin.ipynb`: Notebook used to scrape or clean movie data from the IMDB source.
- `README.md`: Project overview and setup instructions.

## 📊 Features

- Filter movies by:
  - Genre
  - Rating
  - Voting count range
  - Duration
- Visualizations:
  - Top 10 movies by ratings and votes
  - Genre distribution
  - Average duration and voting trends by genre
  - Rating distribution histogram
  - Top-rated movie per genre
  - Most popular genres (pie chart)
  - Shortest and longest movies
  - Correlation between ratings and voting counts
  - Heatmap of ratings by genre

## 🛠 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/imdb-movie-dashboard.git
   cd imdb-movie-dashboard

