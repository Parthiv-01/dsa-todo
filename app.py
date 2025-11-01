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
        completed_medium = tracker.get_question_status(day, 'medium')
        completed_hard = tracker.get_question_status(day, 'hard')
        
        st.markdown("---")
        st.write("**Progress:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if total_easy > 0:
                progress = completed_easy / total_easy
                st.progress(progress)
                st.caption(f"🟢 Easy: {completed_easy}/{total_easy}")
        with col2:
            if total_medium > 0:
                progress = completed_medium / total_medium
                st.progress(progress)
                st.caption(f"🟡 Medium: {completed_medium}/{total_medium}")
        with col3:
            if total_hard > 0:
                progress = completed_hard / total_hard
                st.progress(progress)
                st.caption(f"🔴 Hard: {completed_hard}/{total_hard}")
        
        # Controls
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            current_status = tracker.get_day_status(day)
            new_status = st.selectbox(
                "Status",
                ["planned", "in-progress", "completed"],
                index=["planned", "in-progress", "completed"].index(current_status),
                key=f"status_{day}",
                label_visibility="collapsed"
            )
            if new_status != current_status:
                tracker.update_progress(day, new_status)
                st.rerun()
        
        with col2:
            st.write("**Update Progress:**")
            subcol1, subcol2, subcol3 = st.columns(3)
            with subcol1:
                if total_easy > 0:
                    easy_done = st.number_input("E", 0, total_easy, 
                                              tracker.get_question_status(day, 'easy'),
                                              key=f"easy_{day}",
                                              label_visibility="collapsed")
                    tracker.update_question_progress(day, 'easy', easy_done)
            with subcol2:
                if total_medium > 0:
                    medium_done = st.number_input("M", 0, total_medium,
                                                tracker.get_question_status(day, 'medium'),
                                                key=f"medium_{day}",
                                                label_visibility="collapsed")
                    tracker.update_question_progress(day, 'medium', medium_done)
            with subcol3:
                if total_hard > 0:
                    hard_done = st.number_input("H", 0, total_hard,
                                              tracker.get_question_status(day, 'hard'),
                                              key=f"hard_{day}",
                                              label_visibility="collapsed")
                    tracker.update_question_progress(day, 'hard', hard_done)
        
        # Notes
        note_key = f"note_{day}"
        current_note = st.session_state.notes.get(day, "")
        with st.expander("📝 Notes"):
            new_note = st.text_area("Add your notes here", value=current_note, key=note_key, height=100,
                                   placeholder="Write your insights, challenges, or resources for this day...")
            if new_note != current_note:
                st.session_state.notes[day] = new_note
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_analytics(tracker):
    st.header("📈 Progress Analytics")
    
    metrics = tracker.calculate_metrics()
    
    # Overall metrics
    st.subheader("🎯 Overall Progress")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Days", metrics['total_days'])
    with col2:
        st.metric("Days Completed", metrics['completed_days'])
    with col3:
        st.metric("Completion Rate", f"{metrics['completion_rate']:.1f}%")
    with col4:
        st.metric("Current Streak", f"{metrics['current_streak']} days")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", metrics['total_questions'])
    with col2:
        st.metric("Questions Done", metrics['completed_questions'])
    with col3:
        st.metric("Question Progress", f"{metrics['question_completion_rate']:.1f}%")
    with col4:
        days_remaining = len(tracker.dsa_plan) - metrics['completed_days']
        st.metric("Days Remaining", days_remaining)
    
    # Progress breakdown
    st.subheader("📊 Progress Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day status distribution
        status_counts = {'completed': 0, 'in-progress': 0, 'planned': 0}
        for day in range(1, len(tracker.dsa_plan) + 1):
            status = tracker.get_day_status(day)
            status_counts[status] += 1
        
        st.write("**Day Status Distribution:**")
        for status, count in status_counts.items():
            percentage = (count / len(tracker.dsa_plan)) * 100
            st.write(f"- **{status.title()}:** {count} days ({percentage:.1f}%)")
    
    with col2:
        # Question difficulty distribution
        difficulty_totals = {'easy': 0, 'medium': 0, 'hard': 0}
        difficulty_completed = {'easy': 0, 'medium': 0, 'hard': 0}
        
        for day_data in tracker.dsa_plan:
            day = day_data['day']
            difficulty_totals['easy'] += day_data['total_easy']
            difficulty_totals['medium'] += day_data['total_medium']
            difficulty_totals['hard'] += day_data['total_hard']
            
            difficulty_completed['easy'] += tracker.get_question_status(day, 'easy')
            difficulty_completed['medium'] += tracker.get_question_status(day, 'medium')
            difficulty_completed['hard'] += tracker.get_question_status(day, 'hard')
        
        st.write("**Questions by Difficulty:**")
        for diff in ['easy', 'medium', 'hard']:
            if difficulty_totals[diff] > 0:
                percent = (difficulty_completed[diff] / difficulty_totals[diff]) * 100
                st.write(f"- **{diff.title()}:** {difficulty_completed[diff]}/{difficulty_totals[diff]} ({percent:.1f}%)")

def display_todays_focus(tracker):
    st.header("🎯 Today's Focus")
    
    start_date = st.session_state.start_date
    today = datetime.now().date()
    day_number = (today - start_date).days + 1
    
    if day_number < 1:
        st.warning("📅 Your DSA journey hasn't started yet! Update your start date in the sidebar.")
        return
    elif day_number > len(tracker.dsa_plan):
        st.success("🎉 Congratulations! You've completed the DSA challenge!")
        st.balloons()
        return
    
    today_data = next((day for day in tracker.dsa_plan if day['day'] == day_number), None)
    if not today_data:
        st.error("❌ No data found for today!")
        return
    
    status = tracker.get_day_status(day_number)
    
    st.subheader(f"Day {day_number}: {', '.join(today_data['topics'])}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Phase:** {today_data['phase']}")
        st.write(f"**Total Questions:** {today_data['total_easy']}E + {today_data['total_medium']}M + {today_data['total_hard']}H")
        st.write(f"**Status:** {status.upper()}")
        
        # Detailed question breakdown
        st.write("**Question Breakdown:**")
        for q in today_data['questions']:
            topic = q['topic']
            easy = q['easy']
            medium = q['medium']
            hard = q['hard']
            if easy + medium + hard > 0:
                st.write(f"• **{topic}:** {easy}E + {medium}M + {hard}H")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("🚀 Start Day", use_container_width=True):
                tracker.update_progress(day_number, 'in-progress')
                st.rerun()
        
        with action_col2:
            if st.button("✅ Complete Day", use_container_width=True):
                tracker.update_progress(day_number, 'completed')
                st.rerun()
    
    with col2:
        # Progress for today
        if status == 'completed':
            st.success("✅ Day Completed!")
        elif status == 'in-progress':
            st.info("🔄 In Progress")
        else:
            st.warning("📋 Planned")
        
        # Today's progress
        completed_easy = tracker.get_question_status(day_number, 'easy')
        completed_medium = tracker.get_question_status(day_number, 'medium')
        completed_hard = tracker.get_question_status(day_number, 'hard')
        
        st.write("**Today's Progress:**")
        if today_data['total_easy'] > 0:
            st.write(f"🟢 Easy: {completed_easy}/{today_data['total_easy']}")
        if today_data['total_medium'] > 0:
            st.write(f"🟡 Medium: {completed_medium}/{today_data['total_medium']}")
        if today_data['total_hard'] > 0:
            st.write(f"🔴 Hard: {completed_hard}/{today_data['total_hard']}")
    
    # Resources section
    st.subheader("💡 Study Resources")
    resources = tracker.get_topic_resources(today_data['topics'])
    for resource in resources[:5]:  # Show top 5 resources
        st.write(f"• {resource}")

def display_topic_mastery(tracker):
    st.header("📊 Topic Mastery")
    
    # Calculate topic-wise progress
    topic_progress = {}
    
    for topic, totals in tracker.topic_totals.items():
        topic_progress[topic] = {
            'total': totals['easy'] + totals['medium'] + totals['hard'],
            'completed': 0,
            'easy_completed': 0,
            'medium_completed': 0,
            'hard_completed': 0
        }
    
    # Calculate completed questions per topic
    for day_data in tracker.dsa_plan:
        day = day_data['day']
        for q in day_data['questions']:
            topic = q['topic']
            if topic in topic_progress:
                # This is a simplified calculation - in a real app, you'd track per-topic progress
                easy_progress = min(q['easy'], tracker.get_question_status(day, 'easy'))
                medium_progress = min(q['medium'], tracker.get_question_status(day, 'medium'))
                hard_progress = min(q['hard'], tracker.get_question_status(day, 'hard'))
                
                topic_progress[topic]['completed'] += easy_progress + medium_progress + hard_progress
                topic_progress[topic]['easy_completed'] += easy_progress
                topic_progress[topic]['medium_completed'] += medium_progress
                topic_progress[topic]['hard_completed'] += hard_progress
    
    # Display topic progress
    st.subheader("Topic-wise Progress")
    
    for topic, progress in sorted(topic_progress.items(), key=lambda x: x[1]['completed']/x[1]['total'] if x[1]['total'] > 0 else 0, reverse=True):
        if progress['total'] > 0:
            completion_rate = (progress['completed'] / progress['total']) * 100
            
            st.write(f"**{topic}**")
            st.write(f"Progress: {progress['completed']}/{progress['total']} ({completion_rate:.1f}%)")
            
            # Progress bar
            st.markdown(f"""
            <div class="topic-progress-bar">
                <div class="topic-progress-fill" style="width: {completion_rate}%;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Difficulty breakdown
            col1, col2, col3 = st.columns(3)
            with col1:
                if tracker.topic_totals[topic]['easy'] > 0:
                    easy_rate = (progress['easy_completed'] / tracker.topic_totals[topic]['easy']) * 100
                    st.caption(f"🟢 Easy: {progress['easy_completed']}/{tracker.topic_totals[topic]['easy']} ({easy_rate:.1f}%)")
            with col2:
                if tracker.topic_totals[topic]['medium'] > 0:
                    medium_rate = (progress['medium_completed'] / tracker.topic_totals[topic]['medium']) * 100
                    st.caption(f"🟡 Medium: {progress['medium_completed']}/{tracker.topic_totals[topic]['medium']} ({medium_rate:.1f}%)")
            with col3:
                if tracker.topic_totals[topic]['hard'] > 0:
                    hard_rate = (progress['hard_completed'] / tracker.topic_totals[topic]['hard']) * 100
                    st.caption(f"🔴 Hard: {progress['hard_completed']}/{tracker.topic_totals[topic]['hard']} ({hard_rate:.1f}%)")
            
            st.markdown("---")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        st.warning("📁 Created 'data' directory. Please add the JSON files to it.")
    
    main()