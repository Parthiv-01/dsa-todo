import streamlit as st
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="DSA Mastery Tracker - All Questions",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .day-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        background-color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .completed {
        border-left-color: #00cc96;
    }
    .in-progress {
        border-left-color: #ffa15c;
    }
    .planned {
        border-left-color: #636efa;
    }
    .topic-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        background-color: #e0e0e0;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .progress-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .topic-progress-bar {
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 4px;
        margin: 5px 0;
    }
    .topic-progress-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
</style>
""", unsafe_allow_html=True)

class DataLoader:
    @staticmethod
    def load_dsa_plan():
        """Load the DSA plan from JSON file"""
        try:
            with open('data/dsa_plan.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("❌ dsa_plan.json file not found. Please make sure it exists in the data folder.")
            return []
    
    @staticmethod
    def load_topic_totals():
        """Load topic totals from JSON file"""
        try:
            with open('data/topic_totals.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("❌ topic_totals.json file not found.")
            return {}
    
    @staticmethod
    def load_resources():
        """Load study resources from JSON file"""
        try:
            with open('data/resources.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("❌ resources.json file not found.")
            return {}

class DSATracker:
    def __init__(self):
        self.dsa_plan = DataLoader.load_dsa_plan()
        self.topic_totals = DataLoader.load_topic_totals()
        self.resources = DataLoader.load_resources()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        if 'progress' not in st.session_state:
            st.session_state.progress = {}
        if 'start_date' not in st.session_state:
            st.session_state.start_date = datetime.now().date()
        if 'notes' not in st.session_state:
            st.session_state.notes = {}
        if 'question_progress' not in st.session_state:
            st.session_state.question_progress = {}
    
    def calculate_metrics(self):
        total_days = len(self.dsa_plan)
        completed_days = len([day for day in st.session_state.progress.values() if day == 'completed'])
        in_progress_days = len([day for day in st.session_state.progress.values() if day == 'in-progress'])
        
        # Calculate total and completed questions
        total_questions = self.get_total_questions_count()
        completed_questions = self.get_completed_questions_count()
        
        return {
            'total_days': total_days,
            'completed_days': completed_days,
            'in_progress_days': in_progress_days,
            'completion_rate': (completed_days / total_days) * 100 if total_days > 0 else 0,
            'current_streak': self.calculate_streak(),
            'total_questions': total_questions,
            'completed_questions': completed_questions,
            'question_completion_rate': (completed_questions / total_questions) * 100 if total_questions > 0 else 0
        }
    
    def get_total_questions_count(self):
        total = 0
        for topic_data in self.topic_totals.values():
            total += topic_data['easy'] + topic_data['medium'] + topic_data['hard']
        return total
    
    def get_completed_questions_count(self):
        completed = 0
        for day, day_data in enumerate(self.dsa_plan, 1):
            day_key = f"day_{day}"
            if day_key in st.session_state.question_progress:
                progress = st.session_state.question_progress[day_key]
                completed += progress.get('easy', 0) + progress.get('medium', 0) + progress.get('hard', 0)
        return completed
    
    def calculate_streak(self):
        streak = 0
        today = datetime.now().date()
        start_date = st.session_state.start_date
        
        for day in range(1, len(self.dsa_plan) + 1):
            day_date = start_date + timedelta(days=day-1)
            if day_date > today:
                break
            if st.session_state.progress.get(day) == 'completed':
                streak += 1
            else:
                streak = 0
        return streak
    
    def get_day_status(self, day):
        return st.session_state.progress.get(day, 'planned')
    
    def update_progress(self, day, status):
        st.session_state.progress[day] = status
    
    def get_question_status(self, day, difficulty):
        day_key = f"day_{day}"
        if day_key not in st.session_state.question_progress:
            st.session_state.question_progress[day_key] = {'easy': 0, 'medium': 0, 'hard': 0}
        return st.session_state.question_progress[day_key].get(difficulty, 0)
    
    def update_question_progress(self, day, difficulty, count):
        day_key = f"day_{day}"
        if day_key not in st.session_state.question_progress:
            st.session_state.question_progress[day_key] = {'easy': 0, 'medium': 0, 'hard': 0}
        st.session_state.question_progress[day_key][difficulty] = count
    
    def get_topic_resources(self, topics):
        """Get study resources for given topics"""
        resources = []
        for topic in topics:
            if topic in self.resources:
                resources.extend(self.resources[topic])
        return resources if resources else ["Practice fundamental problems", "Review basic concepts"]

def main():
    st.markdown('<h1 class="main-header">🚀 DSA Mastery Tracker - All Questions Covered</h1>', unsafe_allow_html=True)
    
    # Initialize tracker
    tracker = DSATracker()
    
    if not tracker.dsa_plan:
        st.error("Failed to load DSA plan data. Please check the data files.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Progress Overview")
        metrics = tracker.calculate_metrics()
        
        # Metrics in cards
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 Days</h3>
            <h2>{metrics['completed_days']}/{metrics['total_days']}</h2>
            <p>{metrics['completion_rate']:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>❓ Questions</h3>
            <h2>{metrics['completed_questions']}/{metrics['total_questions']}</h2>
            <p>{metrics['question_completion_rate']:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Streak</h3>
            <h2>{metrics['current_streak']} days</h2>
            <p>Keep going!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Start date picker
        start_date = st.date_input(
            "🎯 Start Date",
            value=st.session_state.start_date,
            help="Set your start date for the DSA challenge"
        )
        st.session_state.start_date = start_date
        
        # Filters
        st.markdown("---")
        st.header("🔍 Filters")
        phases = ["All"] + list(set(day['phase'] for day in tracker.dsa_plan))
        selected_phase = st.selectbox("Filter by Phase", phases)
        
        statuses = ["All", "Completed", "In Progress", "Planned"]
        selected_status = st.selectbox("Filter by Status", statuses)
        
        # Quick actions
        st.markdown("---")
        st.header("⚡ Quick Actions")
        if st.button("✅ Mark Today as Completed", use_container_width=True):
            today_day = (datetime.now().date() - start_date).days + 1
            if 1 <= today_day <= len(tracker.dsa_plan):
                tracker.update_progress(today_day, 'completed')
                st.success(f"🎉 Marked Day {today_day} as completed!")
                st.rerun()
        
        if st.button("🔄 Reset All Progress", use_container_width=True):
            st.session_state.progress = {}
            st.session_state.question_progress = {}
            st.session_state.notes = {}
            st.success("🔄 All progress reset!")
            st.rerun()

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Study Plan", "📈 Progress Analytics", "🎯 Today's Focus", "📊 Topic Mastery"])

    with tab1:
        display_daywise_plan(tracker, selected_phase, selected_status)
    
    with tab2:
        display_analytics(tracker)
    
    with tab3:
        display_todays_focus(tracker)
        
    with tab4:
        display_topic_mastery(tracker)

def display_daywise_plan(tracker, selected_phase, selected_status):
    st.header("📅 30-Day DSA Study Plan")
    
    # Filter data
    filtered_data = [day for day in tracker.dsa_plan if selected_phase == "All" or day['phase'] == selected_phase]
    
    if selected_status != "All":
        status_map = {"Completed": "completed", "In Progress": "in-progress", "Planned": "planned"}
        filtered_data = [day for day in filtered_data if tracker.get_day_status(day['day']) == status_map[selected_status]]
    
    # Display days in a grid
    cols = st.columns(2)
    for idx, day_data in enumerate(filtered_data):
        with cols[idx % 2]:
            display_day_card(day_data, tracker)

def display_day_card(day_data, tracker):
    day = day_data['day']
    topics = day_data['topics']
    questions = day_data['questions']
    phase = day_data['phase']
    status = tracker.get_day_status(day)
    
    # Calculate actual date
    start_date = st.session_state.start_date
    day_date = start_date + timedelta(days=day-1)
    is_today = day_date == datetime.now().date()
    
    # Status colors and emojis
    status_config = {
        'completed': {'color': '#00cc96', 'emoji': '✅'},
        'in-progress': {'color': '#ffa15c', 'emoji': '🔄'}, 
        'planned': {'color': '#636efa', 'emoji': '📋'}
    }
    
    status_info = status_config.get(status, status_config['planned'])
    
    # Card styling
    card_style = f"""
    border-left: 5px solid {status_info['color']}; 
    background-color: white; 
    padding: 1.5rem; 
    border-radius: 10px; 
    margin: 0.5rem 0; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    """
    
    if is_today:
        card_style += " border: 3px solid #ff4b4b;"
    
    with st.container():
        st.markdown(f'<div style="{card_style}">', unsafe_allow_html=True)
        
        # Header
        st.subheader(f"{status_info['emoji']} Day {day}")
        if is_today:
            st.markdown("**🎯 TODAY**")
        
        # Phase and date
        st.caption(f"**{phase}** • {day_date.strftime('%b %d, %Y')}")
        
        # Topics with badges
        st.write("**Topics:**")
        for topic in topics:
            st.markdown(f'<span class="topic-badge">{topic}</span>', unsafe_allow_html=True)
        
        # Questions breakdown
        st.write("**Questions Breakdown:**")
        for q in questions:
            topic = q['topic']
            easy = q['easy']
            medium = q['medium'] 
            hard = q['hard']
            if easy + medium + hard > 0:
                st.write(f"• **{topic}:** {easy}E + {medium}M + {hard}H")
        
        # Progress bars
        total_easy = day_data['total_easy']
        total_medium = day_data['total_medium'] 
        total_hard = day_data['total_hard']
        
        completed_easy = tracker.get_question_status(day, 'easy')
        completed_medium = tracker.get