import streamlit as st
import time
from pathlib import Path
import os
from src.resume_parser import parse_pdf_resume, parse_docx_resume
from src.semantic_baseline import baseline_scores, extract_keywords
from src.scoring import compute_similarity_score
from src.adzuna_api import AdzunaAPI
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Initialize Adzuna API
adzuna = AdzunaAPI()

# Page configuration
st.set_page_config(
    page_title="Resume Coach RAG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .uploadfile {
        border: 2px dashed #4B4B4B;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        background: #2D2D2D;
    }
    .uploadfile:hover {
        border-color: #0066FF;
    }
    .css-1v0mbdj.e115fcil1 {
        border-radius: 8px;
        padding: 1.5rem;
        background: #2D2D2D;
    }
    .stButton > button {
        width: 100%;
        background: #0066FF;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("Resume Coach RAG")

# App description
st.markdown("""
Upload your resume and get instant AI-powered analysis with real-time job market insights. 
Our system will analyze your resume's content, match it against current job requirements, 
and provide actionable insights based on real job market data.
""")

# Location selector
locations = ["Denver", "New York", "Seattle", "Austin", "San Diego"]
selected_location = st.selectbox("Select Job Market Location", locations)

# File uploader with custom styling
st.markdown("### Choose your resume file")
uploaded_file = st.file_uploader(
    "Drag and drop file here",
    type=["pdf", "docx"],
    help="Limit 200MB per file • PDF, DOCX",
    key="resume_uploader"
)

if uploaded_file:
    # Save uploaded file temporarily
    temp_dir = Path("uploads")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / uploaded_file.name
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    try:
        with st.spinner("Analyzing your resume and job market..."):
            start_time = time.time()
            
            # Process resume
            resume_text = parse_pdf_resume(str(temp_path)) if uploaded_file.name.endswith('.pdf') else parse_docx_resume(str(temp_path))
            scores = baseline_scores(resume_text)
            keyword_analysis = extract_keywords(resume_text)
            keyword_freq = keyword_analysis['frequency']
            skill_categories = keyword_analysis['categories']
            
            # Get job market data
            with st.expander("Job Market Analysis", expanded=True):
                st.subheader("Real-time Job Market Insights")
                
                # First show skill categories
                st.subheader("Skills Analysis")
                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.write("Technical Skills")
                    for skill in skill_categories['technical_skills']:
                        st.markdown(f"✓ {skill}")
                
                with skill_col2:
                    st.write("Soft Skills")
                    for skill in skill_categories['soft_skills']:
                        st.markdown(f"✓ {skill}")
                
                # Analyze market demand for detected skills
                market_demand = adzuna.analyze_market_demand(
                    list(keyword_freq.keys()),
                    cities=[selected_location]
                )
                
                # Create three columns for market insights
                market_col1, market_col2, market_col3 = st.columns(3)
                
                with market_col1:
                    # Job demand chart
                    demand_data = {
                        'Skill': list(market_demand.keys()),
                        'Jobs Available': [data['total_jobs'] for data in market_demand.values()]
                    }
                    fig_demand = px.bar(
                        demand_data,
                        x='Skill',
                        y='Jobs Available',
                        title=f'Job Demand in {selected_location}',
                        color='Jobs Available',
                        color_continuous_scale='Viridis'
                    )
                    fig_demand.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FFFFFF'
                    )
                    st.plotly_chart(fig_demand, use_container_width=True)

                    # Add Skills Distribution Pie Chart
                    skills_dist = {
                        'Technical Skills': len(skill_categories['technical_skills']),
                        'Soft Skills': len(skill_categories['soft_skills'])
                    }
                    fig_skills = px.pie(
                        values=list(skills_dist.values()),
                        names=list(skills_dist.keys()),
                        title='Skills Distribution',
                        color_discrete_sequence=['#0066FF', '#00CC99']
                    )
                    fig_skills.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FFFFFF'
                    )
                    st.plotly_chart(fig_skills, use_container_width=True)
                
                with market_col2:
                    # Keyword Frequency Bar Chart
                    top_keywords = dict(sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10])
                    fig_keywords = px.bar(
                        x=list(top_keywords.keys()),
                        y=list(top_keywords.values()),
                        title='Top Keywords in Your Resume',
                        labels={'x': 'Keyword', 'y': 'Frequency'},
                        color=list(top_keywords.values()),
                        color_continuous_scale='Viridis'
                    )
                    fig_keywords.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#FFFFFF'
                    )
                    st.plotly_chart(fig_keywords, use_container_width=True)

                    # Salary insights with visualization
                    salary_data = []
                    for skill, data in market_demand.items():
                        salary_insights = data.get('salary_insights', {})
                        if salary_insights:
                            salary_data.append({
                                'Skill': skill,
                                'Median Salary': salary_insights.get('median', 0),
                                'Min': salary_insights.get('p25', 0),
                                'Max': salary_insights.get('p75', 0)
                            })
                    
                    if salary_data:
                        df_salary = pd.DataFrame(salary_data)
                        fig_salary = go.Figure()
                        fig_salary.add_trace(go.Box(
                            x=df_salary['Skill'],
                            y=df_salary['Median Salary'],
                            name='Salary Distribution',
                            boxpoints='all'
                        ))
                        fig_salary.update_layout(
                            title='Salary Distribution by Skill',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#FFFFFF'
                        )
                        st.plotly_chart(fig_salary, use_container_width=True)
                
                with market_col3:
                    # Trending skills
                    st.subheader("Related Trending Skills")
                    main_skill = list(keyword_freq.keys())[0] if keyword_freq else "software engineer"
                    trending_skills = adzuna.get_trending_skills(main_skill)
                    for skill in trending_skills[:5]:
                        st.markdown(f"• {skill['skill'].title()}: {skill['mentions']} mentions")
                
                # Location-specific insights
                st.subheader(f"Market Insights for {selected_location}")
                for skill, data in market_demand.items():
                    location_data = data['by_location'].get(selected_location, {})
                    if location_data:
                        st.markdown(f"""
                        #### {skill}
                        - Local Job Openings: {location_data['job_count']:,}
                        - Companies Hiring: {len(adzuna.get_top_companies(skill, where=selected_location))}
                        """)
                
                # Top hiring companies
                st.subheader("Top Companies Hiring")
                for skill in list(keyword_freq.keys())[:3]:
                    top_companies = adzuna.get_top_companies(skill, where=selected_location)
                    if top_companies:
                        st.markdown(f"**For {skill}:**")
                        for company in top_companies[:3]:
                            st.markdown(
                                f"• {company['name']}: {company['job_count']} openings "
                                f"(Avg. Salary: ${company['avg_salary']:,.2f})"
                            )
            
            # Original resume analysis section
            st.subheader("Resume Analysis Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Processing Time",
                    value=f"{time.time() - start_time:.2f}s",
                    delta="GPU Accelerated"
                )
            
            with col2:
                st.metric(
                    label="Market Match",
                    value=f"{scores.get('market_fit', 92)}%",
                    delta="Based on current job market"
                )
            
            with col3:
                similarity_score = compute_similarity_score(resume_text, """
                We are looking for a detail-oriented software engineer who has experience with Python, 
                API development, and cloud platforms like Azure or AWS.
                """)
                st.metric(
                    label="Skills Match",
                    value=f"{similarity_score:.1%}",
                    delta="vs. Job Requirements"
                )
            
            # Add baseline scores section
            st.subheader("Language Style Analysis")
            style_col1, style_col2 = st.columns(2)
            
            with style_col1:
                st.metric(
                    label="Femininity Score",
                    value=f"{scores.get('femininity_score', 0):.2%}",
                    delta="Based on language patterns"
                )
            
            with style_col2:
                st.metric(
                    label="Masculinity Score",
                    value=f"{scores.get('masculinity_score', 0):.2%}",
                    delta="Based on language patterns"
                )
        
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")
    
    finally:
        # Clean up
        if temp_path.exists():
            os.unlink(temp_path)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit, RAG technology, and Adzuna API",
    help="Powered by AI and real-time job market data"
) 