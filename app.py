import streamlit as st
from src.resume_parser import parse_resume
from src.semantic_baseline import compute_similarity, extract_keywords, load_model, load_spacy
from src.adzuna_api import AdzunaAPI
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize models and APIs
@st.cache_resource
def init_resources():
    return {
        'adzuna': AdzunaAPI(),
        'transformer_model': load_model(),
        'spacy_model': load_spacy()
    }

resources = init_resources()

st.title("Resume Coach - Job Market Analysis")
st.write("Upload your resume to get insights about your skills and the job market.")

# File upload
uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner('Parsing your resume...'):
        resume_text = parse_resume(uploaded_file)
        st.write("### Your Resume Text")
        st.write(resume_text)

        # Extract keywords from resume
        keywords_data = extract_keywords(resume_text)
        
        st.write("### Skills Found in Your Resume")
        
        # Create separate DataFrames for technical and soft skills
        technical_skills = keywords_data["categories"]["technical_skills"]
        soft_skills = keywords_data["categories"]["soft_skills"]
        
        # Display both skill categories
        st.write("#### Technical Skills")
        tech_df = pd.DataFrame({"Skill": technical_skills})
        st.dataframe(tech_df)
        
        st.write("#### Soft Skills")
        soft_df = pd.DataFrame({"Skill": soft_skills})
        st.dataframe(soft_df)

        # Market Analysis
        st.write("### Job Market Analysis")
        cities = ["New York", "San Francisco", "Chicago", "Austin", "Seattle"]
        skills_list = technical_skills + soft_skills  # Use both technical and soft skills for analysis

        with st.spinner('Analyzing job market data...'):
            market_data = resources['adzuna'].analyze_market_demand(skills_list, cities)

            # Create market insights visualization
            market_insights = []
            for skill, data in market_data.items():
                for city, city_data in data['by_location'].items():
                    market_insights.append({
                        'Skill': skill,
                        'City': city,
                        'Job Count': city_data['job_count']
                    })

            df_market = pd.DataFrame(market_insights)
            
            # Plot job distribution
            fig = px.bar(df_market, 
                        x='Skill', 
                        y='Job Count',
                        color='City',
                        title='Job Distribution by Skill and City',
                        barmode='group')
            st.plotly_chart(fig)

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

            # Get top companies
            st.write("### Top Companies Hiring")
            with st.spinner('Finding top companies...'):
                selected_city = st.selectbox("Select a city", cities)
                top_companies = []
                
                for skill in skills_list[:3]:  # Analyze top 3 skills
                    companies = resources['adzuna'].get_top_companies(skill, selected_city)
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

            # Salary insights
            st.write("### Salary Insights")
            salary_data = []
            for skill, data in market_data.items():
                if 'salary_insights' in data and data['salary_insights']:
                    salary_data.append({
                        'Skill': skill,
                        'Median Salary': data['salary_insights']['median'],
                        'P25': data['salary_insights']['p25'],
                        'P75': data['salary_insights']['p75']
                    })

            if salary_data:
                salary_df = pd.DataFrame(salary_data)
                fig = go.Figure()
                for skill in salary_df['Skill']:
                    skill_data = salary_df[salary_df['Skill'] == skill]
                    fig.add_trace(go.Box(
                        name=skill,
                        y=[skill_data['P25'].iloc[0], 
                           skill_data['Median Salary'].iloc[0], 
                           skill_data['P75'].iloc[0]],
                        boxpoints=False
                    ))
                fig.update_layout(title='Salary Distribution by Skill',
                                yaxis_title='Annual Salary ($)')
                st.plotly_chart(fig)
else:
    st.info("Please upload a resume file to get started.")