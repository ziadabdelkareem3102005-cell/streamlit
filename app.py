import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="Netflix Content Analysis")

st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("---")
st.header("📊 Executive Summary & Key Insights")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned_for_streamlit.csv")
    df['Date_added'] = pd.to_datetime(df['Date_added'], errors='coerce')
    df['Year_added'] = df['Date_added'].dt.year
    df.columns = df.columns.str.capitalize()
    return df

df = load_data()

if not df.empty:
    
    total_titles = df.shape[0]
    total_movies = df[df['Type'] == 'Movie'].shape[0]
    total_shows = df[df['Type'] == 'TV Show'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", f"{total_titles:,}")
    col2.metric("Total Movies", f"{total_movies:,}")
    col3.metric("Total TV Shows", f"{total_shows:,}")
    st.markdown("---")


    st.subheader("I. Content Mix and Strategic Trend")
    
    col_pie, col_line = st.columns(2)

    with col_pie:
        st.markdown("##### 1. Distribution of Movies vs. TV Shows")
        
        content_type_counts = df['Type'].value_counts().reset_index()
        content_type_counts.columns = ['Content Type', 'Count']
        fig_pie = px.pie(
            content_type_counts, 
            names='Content Type', 
            values='Count', 
            title='Distribution of Content Types on Netflix',
            color_discrete_sequence=["#26FF00", '#E50914']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("The content library is heavily dominated by Movies, accounting for approximately **69.6%** of the total titles, while TV Shows represent the remaining **30.4%**. This composition suggests a strategic priority on acquiring and producing films to achieve rapid library growth and cater to viewers who prefer single-session content.")


    with col_line:
        st.markdown("##### 2. Netflix Content Additions Over the Years")
        
        yearly_additions = df['Year_added'].value_counts().sort_index().reset_index()
        yearly_additions.columns = ['Year Added', 'Number of Titles Added']

        fig_line = px.line(
            yearly_additions, 
            x='Year Added', 
            y='Number of Titles Added', 
            title='2. Netflix Content Additions Over the Years (Strategy Trend)',
            line_shape='spline'
        )

        fig_line.update_traces(line_color="#000000", mode='lines+markers')
        fig_line.update_xaxes(dtick="M12")
        
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("The trend of content additions shows an aggressive surge starting around **2016**, accelerating rapidly to reach its highest volume in **2019**. This growth signifies a major strategic shift by Netflix, moving away from being solely a distributor to becoming a primary Original Content Producer to secure its market position and competitive edge.")

    st.markdown("---")

    st.subheader("II. Geographical Production and Key Contributors")
    
    col_country, col_director = st.columns(2)

    with col_country:
        st.markdown("##### 3. Top 10 Countries by Content Volume")
        
        country_counts = df.groupby('Countries')['Show_id'].count().sort_values(ascending=False).head(10).reset_index()
        country_counts.columns = ['Country', 'Content Count']

        fig_countries = px.bar(
            country_counts,
            x='Country',
            y='Content Count',
            title='3. Top 10 Countries by Content Volume on Netflix',
            color='Country',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_countries.update_layout(xaxis={'categoryorder':'total descending'}, yaxis={'title': 'Number of Titles'})
        st.plotly_chart(fig_countries, use_container_width=True)
        st.markdown("The data confirms the overwhelming dominance of the **United States** in the content library, accounting for over **3646** of the total titles, primarily due to licensing and the imputation method used. Excluding the US, the top international contributors are **India**, **United Kingdom**, and **Japan**.")


    with col_director:
        st.markdown("##### 4. Top 10 Directors (Excluding Unknown)")
        
        director_counts = df[df['Directors'] != 'Unknown'].groupby('Directors')['Show_id'].count().sort_values(ascending=False).head(10).reset_index()
        director_counts.columns = ['Director', 'Content Count']

        fig_directors = px.bar(
            director_counts,
            x='Director',
            y='Content Count',
            title='4. Top 10 Directors by Content Volume (Excluding Unknown)',
            color='Director',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_directors.update_layout(xaxis={'categoryorder':'total descending'}, yaxis={'title': 'Number of Titles'})
        st.plotly_chart(fig_directors, use_container_width=True)
        st.markdown("The analysis of directors reveals a reliance on a small, core group of individuals. Director **e.g., Rajiv Chilaka** is the most prolific, followed closely by **Raul Campos, Jan Suter** and **Suhas Kadav**. This indicates a strategy of building relationships with specific creators who consistently deliver content, rather than working with a vastly diverse pool of directors.")

    st.markdown("---")

    st.subheader("III. Genre Focus and Actionable Recommendation")
    
    st.markdown("##### 5. Top 10 Genres in the Netflix Library")
    
    genre_df = df.assign(Listed_in=df['Listed_in'].str.split(', ')).explode('Listed_in')
    genre_df['Listed_in'] = genre_df['Listed_in'].str.strip()
    
    top_genres = genre_df['Listed_in'].value_counts().head(10).reset_index()
    top_genres.columns = ['Genre', 'Count']
    
    fig_genres = px.bar(top_genres, x='Genre', y='Count', title='5. Top 10 Genres in the Netflix Library', color='Genre', color_discrete_sequence=px.colors.sequential.Sunset)
    fig_genres.update_layout(xaxis={'categoryorder':'total descending'}, yaxis={'title': 'Number of Titles'})
    st.plotly_chart(fig_genres, use_container_width=True)

    
    st.markdown("---")
    st.header("🔑 Final Recommendation")
    st.info("The analysis of content genres reveals that **International Movies** (as the top genre) and **Dramas** (as the second) form the backbone of the Netflix library. This confirms the platform's strategy to heavily invest in universally appealing narrative content and non-US global cinema.")