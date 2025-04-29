import streamlit as st
from src.resume_parser import parse_resume
from src.semantic_baseline import compute_similarity, extract_keywords, baseline_scores
from src.adzuna_api import AdzunaAPI
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Initialize models and APIs
@st.cache_resource
def init_resources():
    return {
        'adzuna': AdzunaAPI()
    }

resources = init_resources()

st.title("Resume Coach - Job Market Analysis")
st.write("Get insights about your skills and the job market by uploading your resume.")

# Define cities at the top level
cities = ["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Denver"]
selected_city = st.selectbox("Select a city for job market analysis", cities)

# File upload
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner('Analyzing your resume...'):
        # Parse resume
        resume_text = parse_resume(uploaded_file)
        
        # Create an expander for resume text
        with st.expander("View Parsed Resume Text"):
            st.write(resume_text)

        # Language Analysis Section
        st.write("### Resume Language Analysis")
        scores = baseline_scores(resume_text)
        
        st.write("#### Gender Baseline Scores")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fem_score = round(scores["femininity_score"] * 100, 2)
            st.metric("Feminine Language", f"{fem_score}%", help="Words associated with empathy, collaboration, and support")
            
        with col2:
            masc_score = round(scores["masculinity_score"] * 100, 2)
            st.metric("Masculine Language", f"{masc_score}%", help="Words associated with assertiveness, independence, and leadership")
            
        with col3:
            neutral_score = round(100 - fem_score - masc_score, 2)
            st.metric("Neutral Language", f"{neutral_score}%", help="Balanced or gender-neutral language")

        # Visualization of gender baseline distribution
        fig = go.Figure(data=[
            go.Bar(name='Gender Language Distribution',
                  x=['Feminine', 'Masculine', 'Neutral'],
                  y=[fem_score, masc_score, neutral_score],
                  marker_color=['pink', 'blue', 'gray'])
        ])
        fig.update_layout(title='Gender Language Distribution in Resume')
        st.plotly_chart(fig)

        st.write("#### Professional Style Analysis")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            collab_score = round(scores["femininity_score"] * 100, 2)
            st.metric("Collaborative/Supportive", f"{collab_score}%", help="Language emphasizing teamwork and support")
            
        with col5:
            assert_score = round(scores["masculinity_score"] * 100, 2)
            st.metric("Assertive/Independent", f"{assert_score}%", help="Language emphasizing leadership and initiative")
            
        with col6:
            balanced_score = round(100 - collab_score - assert_score, 2)
            st.metric("Balanced/Neutral", f"{balanced_score}%", help="Professional, balanced language")

        # Visualization of professional style distribution
        fig2 = go.Figure(data=[
            go.Bar(name='Professional Style Distribution',
                  x=['Collaborative', 'Assertive', 'Balanced'],
                  y=[collab_score, assert_score, balanced_score],
                  marker_color=['green', 'orange', 'purple'])
        ])
        fig2.update_layout(title='Professional Language Style Distribution')
        st.plotly_chart(fig2)

        # Add interpretation
        with st.expander("📊 Understanding Your Language Scores"):
            st.write("""
            #### Gender Baseline Analysis
            - **Feminine Language**: Words and phrases traditionally associated with feminine traits (empathy, collaboration, nurturing)
            - **Masculine Language**: Words and phrases traditionally associated with masculine traits (assertiveness, independence, leadership)
            - **Neutral Language**: Gender-neutral or balanced language
            
            #### Professional Style Analysis
            - **Collaborative/Supportive**: Emphasizes team skills, support roles, and interpersonal abilities
            - **Assertive/Independent**: Highlights leadership, initiative, and autonomous achievements
            - **Balanced/Neutral**: Professional language that balances both styles
            
            💡 **Tip**: A well-balanced resume often shows a mix of both collaborative and assertive language, 
            tailored to the specific role you're targeting.
            """)

        # Extract keywords from resume
        keywords_data = extract_keywords(resume_text)
        
        # Create separate DataFrames for technical and soft skills
        technical_skills = keywords_data["categories"]["technical_skills"]
        soft_skills = keywords_data["categories"]["soft_skills"]
        
        # Display skills in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Technical Skills")
            tech_df = pd.DataFrame({"Skill": technical_skills})
            st.dataframe(tech_df, height=300)
        
        with col2:
            st.write("### Soft Skills")
            soft_df = pd.DataFrame({"Skill": soft_skills})
            st.dataframe(soft_df, height=300)

        # Market Analysis
        st.write("## Job Market Analysis")
        st.write(f"Analyzing job market in {selected_city} for your skills")
        
        skills_list = technical_skills + soft_skills

        with st.spinner('Analyzing job market data...'):
            # Get job counts for each skill
            job_counts = []
            for skill in skills_list:
                try:
                    # Search jobs directly for the selected city
                    jobs_data = resources['adzuna'].search_jobs(skill, where=selected_city)
                    count = jobs_data.get('count', 0)
                    job_counts.append({
                        'Skill': skill,
                        'Job Count': count
                    })
                except Exception as e:
                    st.error(f"Error fetching data for {skill}: {str(e)}")
                    continue

            if job_counts:
                df_market = pd.DataFrame(job_counts)
                
                # Sort by job count descending
                df_market = df_market.sort_values('Job Count', ascending=False)
                
                # Plot job distribution
                st.write("### Job Distribution by Skill")
                fig = px.bar(df_market, 
                            x='Skill', 
                            y='Job Count',
                            title=f'Number of Job Postings by Skill in {selected_city}')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig)

                # Show the data in a table
                st.write("#### Detailed Job Counts")
                st.dataframe(df_market)
            else:
                st.warning("No job distribution data available for the selected skills.")

            # Get trending skills
            st.write("### Trending Related Skills")
            with st.spinner('Analyzing trending skills...'):
                all_trending = []
                for skill in skills_list[:3]:  # Analyze top 3 skills
                    trending = resources['adzuna'].get_trending_skills(skill)
                    all_trending.extend(trending)

                # Aggregate and sort trending skills
                trending_df = pd.DataFrame(all_trending)
                if not trending_df.empty:
                    trending_df = trending_df.groupby('skill')['mentions'].sum().reset_index()
                    trending_df = trending_df.sort_values('mentions', ascending=False).head(10)
                    
                    fig = px.bar(trending_df, 
                                x='skill', 
                                y='mentions',
                                title='Top 10 Trending Related Skills')
                    st.plotly_chart(fig)
                else:
                    st.warning("No trending skills data available at the moment.")

            # Get top companies
            st.write("### Top Companies Hiring")
            with st.spinner(f'Finding top companies in {selected_city}...'):
                top_companies = []
                
                for skill in skills_list[:3]:  # Analyze top 3 skills
                    companies = resources['adzuna'].get_top_companies(skill, where=selected_city)
                    for company in companies:
                        company['skill'] = skill
                        top_companies.append(company)

                if top_companies:
                    companies_df = pd.DataFrame(top_companies)
                    companies_df = companies_df.sort_values('job_count', ascending=False).head(10)
                    
                    fig = px.bar(companies_df, 
                                x='name', 
                                y='job_count',
                                color='skill',
                                title=f'Top Companies Hiring in {selected_city}')
                    fig.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig)
                else:
                    st.warning(f"No company data available for {selected_city} at the moment.")

            # Salary insights
            st.write("### Salary Insights")
            with st.spinner('Analyzing salary data...'):
                salary_data = []
                for skill in skills_list[:3]:  # Analyze top 3 skills
                    try:
                        salary_info = resources['adzuna'].get_salary_insights(skill)  # Removed where parameter
                        if salary_info:
                            salary_data.append({
                                'Skill': skill,
                                'Median': salary_info.get('avg', 0),  # Changed to use 'avg' instead of 'median'
                                'Min': salary_info.get('min', 0),
                                'Max': salary_info.get('max', 0)
                            })
                    except Exception as e:
                        st.warning(f"Could not fetch salary data for {skill}")
                        continue

                if salary_data:
                    salary_df = pd.DataFrame(salary_data)
                    fig = go.Figure()
                    for skill in salary_df['Skill']:
                        skill_data = salary_df[salary_df['Skill'] == skill]
                        fig.add_trace(go.Box(
                            name=skill,
                            y=[skill_data['Min'].iloc[0], 
                               skill_data['Median'].iloc[0], 
                               skill_data['Max'].iloc[0]],
                            boxpoints=False
                        ))
                    fig.update_layout(title=f'Salary Distribution by Skill',
                                    yaxis_title='Annual Salary ($)')
                    st.plotly_chart(fig)

                    # Add a table view of salary data
                    st.write("#### Detailed Salary Information")
                    st.dataframe(salary_df)
                else:
                    st.warning("No salary data available for the selected skills.")
else:
    st.info("👆 Please upload your resume to get started with the analysis.")