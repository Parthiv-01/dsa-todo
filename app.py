import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="DSA 60-Day Mastery Tracker",
    page_icon="📊",
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
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
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
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# DSA Plan Data
dsa_plan = [
    # Days 1-15
    {"day": 1, "topics": ["Arrays", "Searching & Sorting", "Bit Manipulation"], "difficulty": "2E + 2M + 1H", "phase": "Foundation"},
    {"day": 2, "topics": ["Strings", "Linked List", "Greedy"], "difficulty": "2E + 2M + 1H", "phase": "Foundation"},
    {"day": 3, "topics": ["Binary Trees", "Stack & Queue"], "difficulty": "2E + 2M + 1H", "phase": "Foundation"},
    {"day": 4, "topics": ["Graphs", "DP"], "difficulty": "2E + 2M + 1H", "phase": "Foundation"},
    {"day": 5, "topics": ["BST", "Heap & Hashing", "Arrays"], "difficulty": "2E + 2M + 1H", "phase": "Foundation"},
    {"day": 6, "topics": ["Backtracking", "2D Array"], "difficulty": "0E + 3M + 2H", "phase": "Foundation"},
    {"day": 7, "topics": ["DP", "Strings", "Bit Manipulation"], "difficulty": "1E + 3M + 1H", "phase": "Foundation"},
    {"day": 8, "topics": ["Graphs", "Greedy"], "difficulty": "0E + 3M + 2H", "phase": "Foundation"},
    {"day": 9, "topics": ["Linked List", "Heap & Hashing", "Searching & Sorting"], "difficulty": "1E + 3M + 1H", "phase": "Foundation"},
    {"day": 10, "topics": ["Binary Trees", "Stack & Queue", "Tries"], "difficulty": "1E + 3M + 1H", "phase": "Foundation"},
    {"day": 11, "topics": ["DP", "Arrays", "Segment Tree"], "difficulty": "1E + 3M + 1H", "phase": "Foundation"},
    {"day": 12, "topics": ["Graphs", "BST"], "difficulty": "0E + 3M + 2H", "phase": "Foundation"},
    {"day": 13, "topics": ["Backtracking", "Strings"], "difficulty": "0E + 3M + 2H", "phase": "Foundation"},
    {"day": 14, "topics": ["Heap & Hashing", "Searching & Sorting"], "difficulty": "0E + 3M + 2H", "phase": "Foundation"},
    {"day": 15, "topics": ["DP", "Bit Manipulation"], "difficulty": "1E + 3M + 1H", "phase": "Foundation"},
    # Days 16-30
    {"day": 16, "topics": ["Graphs", "Stack & Queue"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 17, "topics": ["Binary Trees", "Greedy", "2D Array"], "difficulty": "2E + 2M + 1H", "phase": "Intermediate"},
    {"day": 18, "topics": ["Linked List", "Strings", "Tries"], "difficulty": "1E + 3M + 1H", "phase": "Intermediate"},
    {"day": 19, "topics": ["DP", "BST"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 20, "topics": ["Graphs", "Heap & Hashing"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 21, "topics": ["Backtracking", "Searching & Sorting"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 22, "topics": ["DP", "Segment Tree"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 23, "topics": ["Stack & Queue", "Arrays"], "difficulty": "1E + 3M + 1H", "phase": "Intermediate"},
    {"day": 24, "topics": ["Graphs", "Bit Manipulation"], "difficulty": "1E + 3M + 1H", "phase": "Intermediate"},
    {"day": 25, "topics": ["DP", "Greedy"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 26, "topics": ["Heap & Hashing", "Binary Trees"], "difficulty": "1E + 3M + 1H", "phase": "Intermediate"},
    {"day": 27, "topics": ["Backtracking", "Strings", "Searching & Sorting"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 28, "topics": ["Graphs", "Tries"], "difficulty": "0E + 2M + 3H", "phase": "Intermediate"},
    {"day": 29, "topics": ["DP", "Segment Tree"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    {"day": 30, "topics": ["Mixed Bag Review"], "difficulty": "0E + 3M + 2H", "phase": "Intermediate"},
    # Days 31-45
    {"day": 31, "topics": ["Advanced DP"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 32, "topics": ["Graph Algorithms"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 33, "topics": ["Tree Mastery"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 34, "topics": ["System Design Basics"], "difficulty": "1E + 3M + 1H", "phase": "Advanced"},
    {"day": 35, "topics": ["Advanced Strings"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 36, "topics": ["Math & Geometry"], "difficulty": "1E + 3M + 1H", "phase": "Advanced"},
    {"day": 37, "topics": ["DP on Trees"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 38, "topics": ["Graph Connectivity"], "difficulty": "0E + 3M + 2H", "phase": "Advanced"},
    {"day": 39, "topics": ["Heap Advanced"], "difficulty": "1E + 3M + 1H", "phase": "Advanced"},
    {"day": 40, "topics": ["Weak Areas Review"], "difficulty": "Custom", "phase": "Advanced"},
    {"day": 41, "topics": ["Sliding Window"], "difficulty": "1E + 3M + 1H", "phase": "Patterns"},
    {"day": 42, "topics": ["Two Pointers"], "difficulty": "1E + 3M + 1H", "phase": "Patterns"},
    {"day": 43, "topics": ["Fast & Slow Pointers"], "difficulty": "1E + 3M + 1H", "phase": "Patterns"},
    {"day": 44, "topics": ["Merge Intervals"], "difficulty": "1E + 3M + 1H", "phase": "Patterns"},
    {"day": 45, "topics": ["Cyclic Sort"], "difficulty": "1E + 3M + 1H", "phase": "Patterns"},
    # Days 46-60
    {"day": 46, "topics": ["In-place Reversal"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 47, "topics": ["Tree BFS"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 48, "topics": ["Tree DFS"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 49, "topics": ["Two Heaps"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 50, "topics": ["Subsets"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 51, "topics": ["Behavioral + Coding"], "difficulty": "2E + 3M + 0H", "phase": "Interview Prep"},
    {"day": 52, "topics": ["System Design + Coding"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 53, "topics": ["Mock Interview 1"], "difficulty": "0E + 3M + 2H", "phase": "Interview Prep"},
    {"day": 54, "topics": ["Weak Area Deep Dive"], "difficulty": "Custom", "phase": "Interview Prep"},
    {"day": 55, "topics": ["Company-specific"], "difficulty": "1E + 3M + 1H", "phase": "Interview Prep"},
    {"day": 56, "topics": ["Speed Practice"], "difficulty": "0E + 5M + 0H", "phase": "Interview Prep"},
    {"day": 57, "topics": ["Hard Problem Strategy"], "difficulty": "0E + 2M + 3H", "phase": "Interview Prep"},
    {"day": 58, "topics": ["Mock Interview 2"], "difficulty": "0E + 3M + 2H", "phase": "Interview Prep"},
    {"day": 59, "topics": ["Final Review"], "difficulty": "2E + 3M + 0H", "phase": "Interview Prep"},
    {"day": 60, "topics": ["Confidence Day"], "difficulty": "3E + 2M + 0H", "phase": "Interview Prep"}
]

class DSATracker:
    def __init__(self):
        self.df = pd.DataFrame(dsa_plan)
        self.initialize_session_state()
    
    def initialize_session_state(self):
        if 'progress' not in st.session_state:
            st.session_state.progress = {}
        if 'start_date' not in st.session_state:
            st.session_state.start_date = datetime.now().date()
        if 'notes' not in st.session_state:
            st.session_state.notes = {}
        if 'time_spent' not in st.session_state:
            st.session_state.time_spent = {}
    
    def calculate_metrics(self):
        total_days = len(self.df)
        completed_days = len([day for day in st.session_state.progress.values() if day == 'completed'])
        in_progress_days = len([day for day in st.session_state.progress.values() if day == 'in-progress'])
        
        return {
            'total_days': total_days,
            'completed_days': completed_days,
            'in_progress_days': in_progress_days,
            'completion_rate': (completed_days / total_days) * 100 if total_days > 0 else 0,
            'current_streak': self.calculate_streak()
        }
    
    def calculate_streak(self):
        streak = 0
        today = datetime.now().date()
        start_date = st.session_state.start_date
        
        for day in range(1, len(self.df) + 1):
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

def main():
    st.markdown('<h1 class="main-header">🚀 DSA 60-Day Mastery Tracker</h1>', unsafe_allow_html=True)
    
    tracker = DSATracker()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Progress Overview")
        metrics = tracker.calculate_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Completed", f"{metrics['completed_days']}/{metrics['total_days']}")
            st.metric("Completion Rate", f"{metrics['completion_rate']:.1f}%")
        with col2:
            st.metric("In Progress", metrics['in_progress_days'])
            st.metric("Current Streak", f"{metrics['current_streak']} days")
        
        # Start date picker
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.start_date,
            help="Set your start date for the 60-day challenge"
        )
        st.session_state.start_date = start_date
        
        # Phase filter
        phases = ["All"] + list(tracker.df['phase'].unique())
        selected_phase = st.selectbox("Filter by Phase", phases)
        
        # Status filter
        statuses = ["All", "Completed", "In Progress", "Planned"]
        selected_status = st.selectbox("Filter by Status", statuses)
        
        st.markdown("---")
        st.header("🎯 Quick Actions")
        if st.button("Mark Today as Completed"):
            today_day = (datetime.now().date() - start_date).days + 1
            if 1 <= today_day <= 60:
                tracker.update_progress(today_day, 'completed')
                st.success(f"Marked Day {today_day} as completed!")
        
        if st.button("Reset All Progress"):
            if st.button("Confirm Reset?"):
                st.session_state.progress = {}
                st.rerun()

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Day-wise Plan", "📈 Progress Analytics", "🎯 Today's Focus", "📝 Notes & Resources"])
    
    with tab1:
        display_daywise_plan(tracker, selected_phase, selected_status)
    
    with tab2:
        display_analytics(tracker)
    
    with tab3:
        display_todays_focus(tracker)
    
    with tab4:
        display_notes_resources(tracker)

def display_daywise_plan(tracker, selected_phase, selected_status):
    st.header("📅 60-Day DSA Plan")
    
    # Filter data
    filtered_df = tracker.df.copy()
    if selected_phase != "All":
        filtered_df = filtered_df[filtered_df['phase'] == selected_phase]
    
    # Display days in columns
    days_per_row = 3
    days_list = filtered_df.to_dict('records')
    
    for i in range(0, len(days_list), days_per_row):
        cols = st.columns(days_per_row)
        for j, day_data in enumerate(days_list[i:i+days_per_row]):
            with cols[j]:
                display_day_card(day_data, tracker)

def display_day_card(day_data, tracker):
    day = day_data['day']
    topics = day_data['topics']
    difficulty = day_data['difficulty']
    phase = day_data['phase']
    status = tracker.get_day_status(day)
    
    # Calculate actual date
    start_date = st.session_state.start_date
    day_date = start_date + timedelta(days=day-1)
    is_today = day_date == datetime.now().date()
    
    # Status colors
    status_colors = {
        'completed': '#00cc96',
        'in-progress': '#ffa15c', 
        'planned': '#636efa'
    }
    
    # Card styling
    border_color = status_colors.get(status, '#636efa')
    card_style = f"border-left: 5px solid {border_color}; background-color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
    
    if is_today:
        card_style += " border: 2px solid #ff4b4b;"
    
    with st.container():
        st.markdown(f'<div style="{card_style}">', unsafe_allow_html=True)
        
        # Header
        st.subheader(f"Day {day}")
        if is_today:
            st.markdown("**🎯 TODAY**")
        st.caption(f"Phase: {phase} | {day_date.strftime('%b %d, %Y')}")
        
        # Topics
        st.write("**Topics:**")
        for topic in topics:
            st.write(f"• {topic}")
        
        # Difficulty
        st.write(f"**Problems:** {difficulty}")
        
        # Status
        current_status = tracker.get_day_status(day)
        new_status = st.selectbox(
            "Status",
            ["planned", "in-progress", "completed"],
            index=["planned", "in-progress", "completed"].index(current_status),
            key=f"status_{day}"
        )
        
        if new_status != current_status:
            tracker.update_progress(day, new_status)
            st.rerun()
        
        # Notes
        note_key = f"note_{day}"
        current_note = st.session_state.notes.get(day, "")
        new_note = st.text_area("Notes", value=current_note, key=note_key, height=60)
        if new_note != current_note:
            st.session_state.notes[day] = new_note
        
        # Time spent
        time_key = f"time_{day}"
        current_time = st.session_state.time_spent.get(day, 0)
        new_time = st.number_input("Time Spent (hours)", min_value=0.0, value=float(current_time), key=time_key)
        if new_time != current_time:
            st.session_state.time_spent[day] = new_time
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_analytics(tracker):
    st.header("📈 Progress Analytics")
    
    metrics = tracker.calculate_metrics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Days", metrics['total_days'])
    with col2:
        st.metric("Completed", metrics['completed_days'])
    with col3:
        st.metric("Completion Rate", f"{metrics['completion_rate']:.1f}%")
    with col4:
        st.metric("Current Streak", f"{metrics['current_streak']} days")
    
    # Progress chart
    st.subheader("Progress Over Time")
    
    # Create progress data
    progress_data = []
    for day in range(1, 61):
        status = tracker.get_day_status(day)
        progress_data.append({
            'Day': day,
            'Status': status,
            'Date': st.session_state.start_date + timedelta(days=day-1)
        })
    
    progress_df = pd.DataFrame(progress_data)
    
    # Status count chart
    status_counts = pd.Series([tracker.get_day_status(day) for day in range(1, 61)]).value_counts()
    fig_pie = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Status Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Timeline chart
    fig_timeline = go.Figure()
    
    status_mapping = {'planned': 0, 'in-progress': 1, 'completed': 2}
    colors = {'planned': '#636efa', 'in-progress': '#ffa15c', 'completed': '#00cc96'}
    
    for status in ['planned', 'in-progress', 'completed']:
        status_days = progress_df[progress_df['Status'] == status]
        if not status_days.empty:
            fig_timeline.add_trace(go.Scatter(
                x=status_days['Date'],
                y=[status_mapping[status]] * len(status_days),
                mode='markers',
                name=status,
                marker=dict(size=10, color=colors[status]),
                hovertemplate='Day: %{x}<br>Status: ' + status + '<extra></extra>'
            ))
    
    fig_timeline.update_layout(
        title="Progress Timeline",
        yaxis=dict(
            tickvals=[0, 1, 2],
            ticktext=['Planned', 'In Progress', 'Completed'],
            title="Status"
        ),
        xaxis_title="Date",
        height=300
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

def display_todays_focus(tracker):
    st.header("🎯 Today's Focus")
    
    start_date = st.session_state.start_date
    today = datetime.now().date()
    day_number = (today - start_date).days + 1
    
    if day_number < 1:
        st.warning("Your DSA journey hasn't started yet! Update your start date in the sidebar.")
        return
    elif day_number > 60:
        st.success("🎉 Congratulations! You've completed the 60-day DSA challenge!")
        return
    
    today_data = tracker.df[tracker.df['day'] == day_number].iloc[0]
    status = tracker.get_day_status(day_number)
    
    st.subheader(f"Day {day_number}: {', '.join(today_data['topics'])}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Phase:** {today_data['phase']}")
        st.write(f"**Problems:** {today_data['difficulty']}")
        st.write(f"**Status:** {status.upper()}")
        
        # Quick actions
        st.subheader("Quick Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("Start Day", key="start_day"):
                tracker.update_progress(day_number, 'in-progress')
                st.rerun()
        
        with action_col2:
            if st.button("Complete Day", key="complete_day"):
                tracker.update_progress(day_number, 'completed')
                st.rerun()
        
        with action_col3:
            if st.button("Add Notes", key="add_notes"):
                st.session_state.show_notes = True
    
    with col2:
        # Progress for today
        if status == 'completed':
            st.success("✅ Day Completed!")
        elif status == 'in-progress':
            st.info("🔄 In Progress")
        else:
            st.warning("📋 Planned")
    
    # Resources section
    st.subheader("💡 Study Resources")
    resources = get_topic_resources(today_data['topics'])
    for resource in resources:
        st.write(f"• {resource}")

def display_notes_resources(tracker):
    st.header("📝 Notes & Resources")
    
    tab1, tab2, tab3 = st.tabs(["Personal Notes", "Study Resources", "Topic References"])
    
    with tab1:
        st.subheader("Your Notes Across All Days")
        notes_days = [day for day in range(1, 61) if day in st.session_state.notes and st.session_state.notes[day]]
        
        if not notes_days:
            st.info("No notes yet. Add notes to days to see them here!")
        else:
            for day in notes_days:
                with st.expander(f"Day {day} - {', '.join(tracker.df[tracker.df['day'] == day].iloc[0]['topics'])}"):
                    st.write(st.session_state.notes[day])
    
    with tab2:
        st.subheader("General Study Resources")
        resources = {
            "Platforms": [
                "LeetCode - Practice problems",
                "GeeksforGeeks - Detailed explanations",
                "InterviewBit - Curated problem sets",
                "HackerRank - Coding challenges"
            ],
            "Books": [
                "Cracking the Coding Interview",
                "Elements of Programming Interviews",
                "Introduction to Algorithms (CLRS)"
            ],
            "YouTube Channels": [
                "NeetCode - Pattern explanations",
                "Abdul Bari - Algorithm deep dives",
                "Take U Forward - DSA series"
            ]
        }
        
        for category, items in resources.items():
            with st.expander(category):
                for item in items:
                    st.write(f"• {item}")
    
    with tab3:
        st.subheader("Topic-wise Reference")
        all_topics = sorted(set([topic for sublist in tracker.df['topics'] for topic in sublist]))
        selected_topic = st.selectbox("Select Topic", all_topics)
        
        if selected_topic:
            topic_resources = get_topic_resources([selected_topic])
            st.write(f"**Resources for {selected_topic}:**")
            for resource in topic_resources:
                st.write(f"• {resource}")

def get_topic_resources(topics):
    resource_map = {
        "Arrays": ["Array manipulation basics", "Two-pointer technique", "Sliding window pattern"],
        "DP": ["DP patterns sheet", "State transition practice", "Memoization vs tabulation"],
        "Graphs": ["Graph traversal algorithms", "Shortest path algorithms", "Cycle detection"],
        "Trees": ["Tree traversal methods", "BST operations", "Tree DP patterns"],
        "Strings": ["String matching algorithms", "Palindrome problems", "String manipulation"],
        "Linked List": ["Pointer manipulation", "Cycle detection", "Reversal patterns"],
        "Sorting": ["Comparison sorts", "Non-comparison sorts", "Sorting applications"],
        "Searching": ["Binary search variations", "Search in rotated arrays", "Matrix search"]
    }
    
    resources = []
    for topic in topics:
        if topic in resource_map:
            resources.extend(resource_map[topic])
        else:
            resources.append(f"General practice for {topic}")
    
    return resources if resources else ["Practice fundamental problems", "Review basic concepts"]

if __name__ == "__main__":
    main()