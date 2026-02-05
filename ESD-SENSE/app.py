import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gap_detector import LearningGapDetector
from data_generator import generate_synthetic_data
from recommendation_engine import RecommendationEngine

# Page config
st.set_page_config(
    page_title="EDU-SENSE: Learning Gap Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title animations */
    .title-main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 800;
        animation: title-glow 3s ease-in-out infinite;
        margin-bottom: 10px;
    }
    
    @keyframes title-glow {
        0%, 100% { text-shadow: 0 0 20px rgba(102, 126, 234, 0.4); }
        50% { text-shadow: 0 0 40px rgba(118, 75, 162, 0.6); }
    }
    
    .subtitle-main {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.3em;
        font-weight: 600;
        animation: fade-in-up 1s ease-out;
    }
    
    /* Gap severity boxes with animations */
    .gap-alert {
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff6b6b;
        background: linear-gradient(135deg, #ffe0e0 0%, #ffcccc 100%);
        margin: 15px 0;
        animation: slide-in-left 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
        transition: all 0.3s ease;
    }
    
    .gap-alert:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
    }
    
    .gap-warning {
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ffa500;
        background: linear-gradient(135deg, #fff3e0 0%, #ffe6cc 100%);
        margin: 15px 0;
        animation: slide-in-left 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(255, 165, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .gap-warning:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(255, 165, 0, 0.3);
    }
    
    .gap-safe {
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #51cf66;
        background: linear-gradient(135deg, #e6ffed 0%, #d4f7e6 100%);
        margin: 15px 0;
        animation: slide-in-left 0.7s ease-out;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.2);
        transition: all 0.3s ease;
    }
    
    .gap-safe:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(81, 207, 102, 0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid #667eea;
        animation: fade-in-up 0.7s ease-out;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        border-color: #764ba2;
    }
    
    /* Button animations */
    button {
        transition: all 0.3s ease !important;
    }
    
    button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    button:active {
        transform: scale(0.98) !important;
    }
    
    /* Keyframe animations */
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slide-in-left {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce-in {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Status indicators */
    .status-high-risk {
        color: #ff6b6b;
        font-weight: 700;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-medium-risk {
        color: #ffa500;
        font-weight: 700;
    }
    
    .status-on-track {
        color: #51cf66;
        font-weight: 700;
    }
    
    /* Divider enhancement */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    h1, h2, h3 {
        animation: fade-in-up 0.6s ease-out;
    }
    
    /* Info box enhancement */
    .stAlert {
        border-radius: 12px;
        animation: fade-in-up 0.5s ease-out;
    }
    
    /* Container for better spacing */
    .container {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.95);
        margin: 15px 0;
        animation: fade-in-up 0.6s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detector' not in st.session_state:
    st.session_state.detector = LearningGapDetector()
    st.session_state.recommendation_engine = RecommendationEngine()
    st.session_state.student_data = None
    st.session_state.analysis_results = None

# Header
# Header with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <div class='title-main'>🧠 EDU-SENSE</div>
        <div class='subtitle-main'>AI-Powered Early Learning Gap Detection System</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    page = st.radio("Select Module", 
        ["Dashboard", "Student Analysis", "Pattern Report", "Recommendations", "About"])
    
    st.divider()
    st.info("💡 EDU-SENSE analyzes student learning patterns to detect gaps early and suggest interventions before failure occurs.")

# ================== PAGE: DASHBOARD ==================
if page == "Dashboard":
    st.markdown("<h2 style='text-align: center; animation: fade-in-up 0.6s ease-out;'>📊 System Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>👥</div>
            <div style='font-size: 1.5em; font-weight: 700;'>12</div>
            <div style='font-size: 0.9em; opacity: 0.9;'>Total Students</div>
            <div style='font-size: 0.8em; margin-top: 5px; opacity: 0.8;'>↑ 2 new this week</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>⚠️</div>
            <div style='font-size: 1.5em; font-weight: 700;'>8</div>
            <div style='font-size: 0.9em; opacity: 0.9;'>Gaps Detected</div>
            <div style='font-size: 0.8em; margin-top: 5px; opacity: 0.8;'>↑ 3 this week</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <div style='font-size: 2.5em; margin-bottom: 10px;'>📈</div>
            <div style='font-size: 1.5em; font-weight: 700;'>75%</div>
            <div style='font-size: 0.9em; opacity: 0.9;'>Intervention Rate</div>
            <div style='font-size: 0.8em; margin-top: 5px; opacity: 0.8;'>↑ 5% improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Load or generate sample data
    if st.button("🔄 Load Sample Student Data", key="load_data"):
        st.session_state.student_data = generate_synthetic_data()
        st.success("Sample data loaded successfully!")
    
    if st.session_state.student_data is not None:
        st.markdown("<h3 style='text-align: center; margin-top: 30px;'>📈 Recent Student Activity</h3>", unsafe_allow_html=True)
        st.dataframe(st.session_state.student_data.head(10), use_container_width=True)
        
        st.markdown("<h3 style='text-align: center; margin-top: 30px;'>Student Status Overview</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%); text-align: center;'>
                <div style='font-size: 3em;'>🔴</div>
                <div style='font-size: 1.8em; font-weight: 700;'>3</div>
                <div style='font-size: 1em;'>High Risk Students</div>
                <div style='font-size: 0.85em; margin-top: 5px; opacity: 0.9;'>Needs immediate intervention</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #ffa500 0%, #ffb74d 100%); text-align: center;'>
                <div style='font-size: 3em;'>🟡</div>
                <div style='font-size: 1.8em; font-weight: 700;'>4</div>
                <div style='font-size: 1em;'>Medium Risk Students</div>
                <div style='font-size: 0.85em; margin-top: 5px; opacity: 0.9;'>Monitor closely</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='metric-card' style='background: linear-gradient(135deg, #51cf66 0%, #69db7c 100%); text-align: center;'>
                <div style='font-size: 3em;'>🟢</div>
                <div style='font-size: 1.8em; font-weight: 700;'>5</div>
                <div style='font-size: 1em;'>On Track Students</div>
                <div style='font-size: 0.85em; margin-top: 5px; opacity: 0.9;'>Progressing well</div>
            </div>
            """, unsafe_allow_html=True)

# ================== PAGE: STUDENT ANALYSIS ==================
elif page == "Student Analysis":
    st.header("🔍 Analyze Student Learning Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Load Sample Data First", key="load_sample"):
            st.session_state.student_data = generate_synthetic_data()
            st.success("Sample data loaded!")
    
    if st.session_state.student_data is not None:
        # Student selection
        students = st.session_state.student_data['Student_ID'].unique()
        selected_student = st.selectbox("Select Student", students, key="student_select")
        
        if st.button("🔬 Analyze Selected Student", key="analyze_btn"):
            # Get student data
            student_df = st.session_state.student_data[
                st.session_state.student_data['Student_ID'] == selected_student
            ]
            
            # Run analysis
            analysis = st.session_state.detector.analyze_student(student_df)
            st.session_state.analysis_results = analysis
            st.success(f"Analysis complete for {selected_student}!")
        
        # Display results
        if st.session_state.analysis_results is not None:
            st.divider()
            st.subheader("📊 Analysis Results")
            
            results = st.session_state.analysis_results
            
            # Display detected gaps
            st.subheader("Detected Learning Gaps")
            for gap_type, details in results['gaps'].items():
                if details['severity'] == 'high':
                    st.markdown(f"""
                    <div class="gap-alert">
                        <strong>🔴 {gap_type.upper()}</strong><br>
                        Severity: {details['severity']}<br>
                        Confidence: {details['confidence']:.1%}
                    </div>
                    """, unsafe_allow_html=True)
                elif details['severity'] == 'medium':
                    st.markdown(f"""
                    <div class="gap-warning">
                        <strong>🟡 {gap_type.upper()}</strong><br>
                        Severity: {details['severity']}<br>
                        Confidence: {details['confidence']:.1%}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="gap-safe">
                        <strong>🟢 {gap_type.upper()}</strong><br>
                        Severity: {details['severity']}<br>
                        Confidence: {details['confidence']:.1%}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Overall score
            st.metric("Overall Performance Score", 
                     f"{results['overall_score']:.1%}", 
                     delta=None)
    else:
        st.warning("Please load sample data first from the Dashboard page")

# ================== PAGE: PATTERN REPORT ==================
elif page == "Pattern Report":
    st.header("📋 Learning Pattern Analysis Report")
    
    if st.session_state.student_data is not None and st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results
        
        st.subheader("Pattern Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Attempts", results['total_attempts'])
        with col2:
            st.metric("Correct Answers", f"{results['correct_answers']}/{results['total_attempts']}")
        with col3:
            st.metric("Avg Time (sec)", f"{results['avg_time']:.1f}")
        with col4:
            st.metric("Accuracy", f"{results['accuracy']:.1%}")
        
        st.divider()
        
        st.subheader("Detailed Gap Analysis")
        
        # Create detailed report
        report_data = {
            'Gap Type': list(results['gaps'].keys()),
            'Severity': [results['gaps'][g]['severity'] for g in results['gaps'].keys()],
            'Confidence': [f"{results['gaps'][g]['confidence']:.1%}" for g in results['gaps'].keys()],
            'Affected Questions': [results['gaps'][g].get('affected_questions', 0) for g in results['gaps'].keys()]
        }
        
        report_df = pd.DataFrame(report_data)
        st.dataframe(report_df, use_container_width=True)
        
        # Export option
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Report as CSV"):
                csv = report_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    else:
        st.warning("Please complete student analysis first")

# ================== PAGE: RECOMMENDATIONS ==================
elif page == "Recommendations":
    st.header("💡 Personalized Intervention Recommendations")
    
    if st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results
        
        # Generate recommendations
        recommendations = st.session_state.recommendation_engine.generate_recommendations(results)
        
        st.subheader("Recommended Actions")
        
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"🎯 Recommendation {i}: {rec['title']}", expanded=(i==1)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {rec['description']}")
                    st.write(f"**Practice Type:** {rec['practice_type']}")
                    st.write(f"**Suggested Duration:** {rec['duration']}")
                    st.write(f"**Target Topics:** {', '.join(rec['target_topics'])}")
                
                with col2:
                    st.metric("Priority", rec['priority'])
                    st.metric("Expected Impact", f"{rec['expected_impact']:.0%}")
        
        st.divider()
        st.subheader("Implementation Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**For Teachers:**")
            st.write("""
            1. Review recommended interventions above
            2. Select 2-3 high-priority recommendations
            3. Schedule focused practice sessions
            4. Monitor student progress
            5. Re-assess after 1-2 weeks
            """)
        
        with col2:
            st.write("**For Students:**")
            st.write("""
            1. Attempt recommended practice problems
            2. Focus on target topics first
            3. Spend time on weak areas
            4. Track your improvement
            5. Ask for help when stuck
            """)
    else:
        st.warning("Please complete student analysis first")

# ================== PAGE: ABOUT ==================
elif page == "About":
    st.markdown("<h2 style='text-align: center;'>ℹ️ About EDU-SENSE</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🎯 Mission</h3>
            <p>EDU-SENSE is an AI-powered learning gap detection system designed to:</p>
            <ul>
                <li><strong>Detect</strong> learning gaps early before students fail</li>
                <li><strong>Analyze</strong> student mistake patterns and behavior</li>
                <li><strong>Recommend</strong> timely micro-interventions</li>
                <li><strong>Support</strong> teachers with actionable insights</li>
                <li><strong>Respect</strong> student privacy and maintain transparency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>🛠️ Technology Stack</h3>
            <ul style='list-style: none; padding: 0;'>
                <li>🐍 <strong>Backend:</strong> Python, Pandas, Scikit-learn</li>
                <li>🎨 <strong>Frontend:</strong> Streamlit</li>
                <li>📊 <strong>Data:</strong> Synthetic datasets based on real patterns</li>
                <li>🤖 <strong>ML Approach:</strong> Rule-based + Lightweight ML</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class='feature-card'>
        <h3 style='text-align: center;'>📊 How It Works</h3>
        <table style='width: 100%;'>
            <tr>
                <td style='text-align: center; padding: 10px;'><strong style='font-size: 1.5em;'>1️⃣</strong><br>Input</td>
                <td style='text-align: center; padding: 10px;'>→</td>
                <td style='text-align: center; padding: 10px;'><strong style='font-size: 1.5em;'>2️⃣</strong><br>Analysis</td>
                <td style='text-align: center; padding: 10px;'>→</td>
                <td style='text-align: center; padding: 10px;'><strong style='font-size: 1.5em;'>3️⃣</strong><br>Classification</td>
                <td style='text-align: center; padding: 10px;'>→</td>
                <td style='text-align: center; padding: 10px;'><strong style='font-size: 1.5em;'>4️⃣</strong><br>Recommendation</td>
                <td style='text-align: center; padding: 10px;'>→</td>
                <td style='text-align: center; padding: 10px;'><strong style='font-size: 1.5em;'>5️⃣</strong><br>Action</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<h3 style='text-align: center;'>✨ Key Features</h3>", unsafe_allow_html=True)
    
    features = {
        "🔍 Pattern Detection": "Identifies repeated mistakes and confusion patterns",
        "⚡ Real-time Analysis": "Instant gap detection from student behavior",
        "🎯 Targeted Recommendations": "Specific, actionable interventions",
        "📊 Visual Reports": "Easy-to-understand dashboards for teachers",
        "🔐 Privacy-First": "Works with synthetic data, respects anonymity",
        "📈 Teacher-Friendly": "Designed with teachers' needs in mind"
    }
    
    feature_cols = st.columns(2)
    for idx, (feature, description) in enumerate(features.items()):
        with feature_cols[idx % 2]:
            st.markdown(f"""
            <div class='feature-card'>
                <h4>{feature}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>👥 Team</h3>
            <p>EDU-SENSE - Developed for early learning intervention and student support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📞 Contact & Support</h3>
            <p>For questions or feedback, please contact the development team.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 12px; color: white;'>
        <strong>Version 1.0.0</strong> | Demo | Last Updated: 2025
    </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%); 
            border-radius: 12px; color: white; animation: fade-in-up 1s ease-out;'>
    <h3 style='margin: 0; margin-bottom: 10px;'>🧠 EDU-SENSE</h3>
    <p style='margin: 5px 0; font-size: 1.1em;'>An AI Second-Teacher for Early Learning Gap Detection</p>
    <p style='margin: 10px 0; opacity: 0.9;'>© 2025 | Ethical AI for Education</p>
    <p style='margin: 5px 0; font-size: 0.9em; opacity: 0.8;'>✨ Making Education Smarter, One Gap at a Time ✨</p>
</div>
""", unsafe_allow_html=True)
