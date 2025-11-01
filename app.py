import streamlit as st
import json
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="DSA 60-Day Mastery Tracker",
    page_icon="📊",
    layout="wide"
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
        background-color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        padding: 0.2rem 0.5rem;
        margin: 0.1rem;
        background-color: #e0e0e0;
        border-radius: 15px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Complete DSA Plan with EXACT question distribution from your data
dsa_plan = [
    # Days 1-30 with exact question distribution
    {"day": 1, "topics": ["Arrays", "Searching & Sorting", "Bit Manipulation"], "easy": 3, "medium": 2, "hard": 0, "phase": "Foundation"},
    {"day": 2, "topics": ["Strings", "Linked List", "Greedy"], "easy": 3, "medium": 2, "hard": 0, "phase": "Foundation"},
    {"day": 3, "topics": ["Binary Trees", "Stack & Queue"], "easy": 3, "medium": 2, "hard": 0, "phase": "Foundation"},
    {"day": 4, "topics": ["Graphs", "DP"], "easy": 2, "medium": 2, "hard": 0, "phase": "Foundation"},
    {"day": 5, "topics": ["BST", "Heap & Hashing", "Arrays"], "easy": 1, "medium": 3, "hard": 0, "phase": "Foundation"},
    {"day": 6, "topics": ["Backtracking", "2D Array"], "easy": 0, "medium": 3, "hard": 1, "phase": "Foundation"},
    {"day": 7, "topics": ["DP", "Strings", "Bit Manipulation"], "easy": 1, "medium": 3, "hard": 0, "phase": "Foundation"},
    {"day": 8, "topics": ["Graphs", "Greedy"], "easy": 0, "medium": 3, "hard": 1, "phase": "Foundation"},
    {"day": 9, "topics": ["Linked List", "Heap & Hashing", "Searching & Sorting"], "easy": 1, "medium": 3, "hard": 1, "phase": "Foundation"},
    {"day": 10, "topics": ["Binary Trees", "Stack & Queue", "Tries"], "easy": 1, "medium": 3, "hard": 0, "phase": "Foundation"},
    {"day": 11, "topics": ["DP", "Arrays", "Segment Tree"], "easy": 0, "medium": 4, "hard": 0, "phase": "Foundation"},
    {"day": 12, "topics": ["Graphs", "BST"], "easy": 0, "medium": 3, "hard": 1, "phase": "Foundation"},
    {"day": 13, "topics": ["Backtracking", "Strings"], "easy": 0, "medium": 2, "hard": 1, "phase": "Foundation"},
    {"day": 14, "topics": ["Heap & Hashing", "Searching & Sorting"], "easy": 0, "medium": 3, "hard": 1, "phase": "Foundation"},
    {"day": 15, "topics": ["DP", "Bit Manipulation"], "easy": 2, "medium": 1, "hard": 0, "phase": "Foundation"},
    {"day": 16, "topics": ["Graphs", "Stack & Queue"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 17, "topics": ["Binary Trees", "Greedy", "2D Array"], "easy": 2, "medium": 2, "hard": 0, "phase": "Intermediate"},
    {"day": 18, "topics": ["Linked List", "Strings", "Tries"], "easy": 1, "medium": 3, "hard": 0, "phase": "Intermediate"},
    {"day": 19, "topics": ["DP", "BST"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 20, "topics": ["Graphs", "Heap & Hashing"], "easy": 0, "medium": 2, "hard": 1, "phase": "Intermediate"},
    {"day": 21, "topics": ["Backtracking", "Searching & Sorting"], "easy": 0, "medium": 2, "hard": 1, "phase": "Intermediate"},
    {"day": 22, "topics": ["DP", "Segment Tree"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 23, "topics": ["Stack & Queue", "Arrays"], "easy": 1, "medium": 2, "hard": 0, "phase": "Intermediate"},
    {"day": 24, "topics": ["Graphs", "Bit Manipulation"], "easy": 2, "medium": 1, "hard": 0, "phase": "Intermediate"},
    {"day": 25, "topics": ["DP", "Greedy"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 26, "topics": ["Heap & Hashing", "Binary Trees"], "easy": 1, "medium": 2, "hard": 0, "phase": "Intermediate"},
    {"day": 27, "topics": ["Backtracking", "Strings", "Searching & Sorting"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 28, "topics": ["Graphs", "Tries"], "easy": 0, "medium": 2, "hard": 2, "phase": "Intermediate"},
    {"day": 29, "topics": ["DP", "Segment Tree"], "easy": 0, "medium": 3, "hard": 1, "phase": "Intermediate"},
    {"day": 30, "topics": ["Mixed Bag Review"], "easy": 0, "medium": 3, "hard": 2, "phase": "Intermediate"},
]

class DSATracker:
    def __init__(self):
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
        total_days = len(dsa_plan)
        completed_days = len([day for day in st.session_state.progress.values() if day == 'completed'])
        in_progress_days = len([day for day in st.session_state.progress.values() if day == 'in-progress'])
        
        # Calculate total questions
        total_questions = sum(day['easy'] + day['medium'] + day['hard'] for day in dsa_plan)
        
        # Calculate completed questions
        completed_questions = 0
        for day_data in dsa_plan:
            day = day_data['day']
            day_key = f"day_{day}"
            if day_key in st.session_state.question_progress:
                progress = st.session_state.question_progress[day_key]
                completed_questions += progress.get('easy', 0) + progress.get('medium', 0) + progress.get('hard', 0)
        
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
    
    def calculate_streak(self):
        streak = 0
        today = datetime.now().date()
        start_date = st.session_state.start_date
        
        for day in range(1, len(dsa_plan) + 1):
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

def main():
    st.markdown('<h1 class="main-header">🚀 DSA 60-Day Mastery Tracker</h1>', unsafe_allow_html=True)
    
    tracker = DSATracker()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Progress Overview")
        metrics = tracker.calculate_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Days Completed", f"{metrics['completed_days']}/{metrics['total_days']}")
            st.metric("Questions Done", f"{metrics['completed_questions']}/{metrics['total_questions']}")
        with col2:
            st.metric("Completion Rate", f"{metrics['completion_rate']:.1f}%")
            st.metric("Current Streak", f"{metrics['current_streak']} days")
        
        # Start date picker
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.start_date,
            help="Set your start date for the 60-day challenge"
        )
        st.session_state.start_date = start_date
        
        # Phase filter
        phases = ["All"] + list(set(day['phase'] for day in dsa_plan))
        selected_phase = st.selectbox("Filter by Phase", phases)
        
        # Status filter
        statuses = ["All", "Completed", "In Progress", "Planned"]
        selected_status = st.selectbox("Filter by Status", statuses)
        
        st.markdown("---")
        st.header("🎯 Quick Actions")
        if st.button("Mark Today as Completed"):
            today_day = (datetime.now().date() - start_date).days + 1
            if 1 <= today_day <= 30:
                tracker.update_progress(today_day, 'completed')
                st.success(f"Marked Day {today_day} as completed!")
                st.rerun()
        
        if st.button("Reset All Progress"):
            st.session_state.progress = {}
            st.session_state.question_progress = {}
            st.session_state.notes = {}
            st.success("All progress reset!")
            st.rerun()

    # Main content
    tab1, tab2, tab3 = st.tabs(["📅 Day-wise Plan", "📈 Progress Analytics", "🎯 Today's Focus"])

    with tab1:
        display_daywise_plan(tracker, selected_phase, selected_status)
    
    with tab2:
        display_analytics(tracker)
    
    with tab3:
        display_todays_focus(tracker)

def display_daywise_plan(tracker, selected_phase, selected_status):
    st.header("📅 30-Day DSA Plan")
    
    # Filter data
    filtered_data = [day for day in dsa_plan if selected_phase == "All" or day['phase'] == selected_phase]
    
    if selected_status != "All":
        status_map = {"Completed": "completed", "In Progress": "in-progress", "Planned": "planned"}
        filtered_data = [day for day in filtered_data if tracker.get_day_status(day['day']) == status_map[selected_status]]
    
    # Display days
    for day_data in filtered_data:
        display_day_card(day_data, tracker)

def display_day_card(day_data, tracker):
    day = day_data['day']
    topics = day_data['topics']
    easy = day_data['easy']
    medium = day_data['medium']
    hard = day_data['hard']
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
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Day {day}: {', '.join(topics)}")
            if is_today:
                st.markdown("**🎯 TODAY**")
        with col2:
            st.caption(f"Phase: {phase}")
            st.caption(day_date.strftime('%b %d, %Y'))
        
        # Questions breakdown
        st.write(f"**Questions:** {easy}E + {medium}M + {hard}H")
        
        # Progress bars for questions
        completed_easy = tracker.get_question_status(day, 'easy')
        completed_medium = tracker.get_question_status(day, 'medium')
        completed_hard = tracker.get_question_status(day, 'hard')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if easy > 0:
                progress = completed_easy / easy
                st.progress(progress)
                st.caption(f"Easy: {completed_easy}/{easy}")
        with col2:
            if medium > 0:
                progress = completed_medium / medium
                st.progress(progress)
                st.caption(f"Medium: {completed_medium}/{medium}")
        with col3:
            if hard > 0:
                progress = completed_hard / hard
                st.progress(progress)
                st.caption(f"Hard: {completed_hard}/{hard}")
        
        # Status and controls
        st.markdown("---")
        col1, col2 = st.columns([2, 3])
        
        with col1:
            current_status = tracker.get_day_status(day)
            new_status = st.selectbox(
                "Day Status",
                ["planned", "in-progress", "completed"],
                index=["planned", "in-progress", "completed"].index(current_status),
                key=f"status_{day}"
            )
            if new_status != current_status:
                tracker.update_progress(day, new_status)
                st.rerun()
        
        with col2:
            st.write("**Question Progress:**")
            subcol1, subcol2, subcol3 = st.columns(3)
            with subcol1:
                if easy > 0:
                    easy_done = st.number_input("Easy", 0, easy, 
                                              tracker.get_question_status(day, 'easy'),
                                              key=f"easy_{day}")
                    tracker.update_question_progress(day, 'easy', easy_done)
            with subcol2:
                if medium > 0:
                    medium_done = st.number_input("Medium", 0, medium,
                                                tracker.get_question_status(day, 'medium'),
                                                key=f"medium_{day}")
                    tracker.update_question_progress(day, 'medium', medium_done)
            with subcol3:
                if hard > 0:
                    hard_done = st.number_input("Hard", 0, hard,
                                              tracker.get_question_status(day, 'hard'),
                                              key=f"hard_{day}")
                    tracker.update_question_progress(day, 'hard', hard_done)
        
        # Notes
        note_key = f"note_{day}"
        current_note = st.session_state.notes.get(day, "")
        if st.button("📝 Add Notes", key=f"notes_btn_{day}"):
            st.session_state[f"show_notes_{day}"] = not st.session_state.get(f"show_notes_{day}", False)
        
        if st.session_state.get(f"show_notes_{day}", False):
            new_note = st.text_area("Your Notes", value=current_note, key=note_key, height=80)
            if new_note != current_note:
                st.session_state.notes[day] = new_note
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_analytics(tracker):
    st.header("📈 Progress Analytics")
    
    metrics = tracker.calculate_metrics()
    
    # Key metrics
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
        days_remaining = 30 - metrics['completed_days']
        st.metric("Days Remaining", days_remaining)
    
    # Progress charts using native Streamlit elements
    st.subheader("Progress Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = {'completed': 0, 'in-progress': 0, 'planned': 0}
        for day in range(1, 31):
            status = tracker.get_day_status(day)
            status_counts[status] += 1
        
        st.write("**Day Status:**")
        for status, count in status_counts.items():
            if count > 0:
                st.write(f"- {status.title()}: {count} days")
    
    with col2:
        # Question difficulty distribution
        difficulty_totals = {'easy': 0, 'medium': 0, 'hard': 0}
        difficulty_completed = {'easy': 0, 'medium': 0, 'hard': 0}
        
        for day_data in dsa_plan:
            day = day_data['day']
            difficulty_totals['easy'] += day_data['easy']
            difficulty_totals['medium'] += day_data['medium']
            difficulty_totals['hard'] += day_data['hard']
            
            difficulty_completed['easy'] += tracker.get_question_status(day, 'easy')
            difficulty_completed['medium'] += tracker.get_question_status(day, 'medium')
            difficulty_completed['hard'] += tracker.get_question_status(day, 'hard')
        
        st.write("**Questions by Difficulty:**")
        for diff in ['easy', 'medium', 'hard']:
            if difficulty_totals[diff] > 0:
                percent = (difficulty_completed[diff] / difficulty_totals[diff]) * 100
                st.write(f"- {diff.title()}: {difficulty_completed[diff]}/{difficulty_totals[diff]} ({percent:.1f}%)")
    
    # Topic-wise progress
    st.subheader("📊 Topic-wise Coverage")
    topic_coverage = {}
    
    for day_data in dsa_plan:
        for topic in day_data['topics']:
            if topic not in topic_coverage:
                topic_coverage[topic] = 0
            topic_coverage[topic] += 1
    
    st.write("**Days per Topic:**")
    for topic, count in sorted(topic_coverage.items(), key=lambda x: x[1], reverse=True):
        st.write(f"- {topic}: {count} days")

def display_todays_focus(tracker):
    st.header("🎯 Today's Focus")
    
    start_date = st.session_state.start_date
    today = datetime.now().date()
    day_number = (today - start_date).days + 1
    
    if day_number < 1:
        st.warning("Your DSA journey hasn't started yet! Update your start date in the sidebar.")
        return
    elif day_number > 30:
        st.success("🎉 Congratulations! You've completed the 30-day DSA challenge!")
        st.balloons()
        return
    
    today_data = next((day for day in dsa_plan if day['day'] == day_number), None)
    if not today_data:
        st.error("No data found for today!")
        return
    
    status = tracker.get_day_status(day_number)
    
    st.subheader(f"Day {day_number}: {', '.join(today_data['topics'])}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Phase:** {today_data['phase']}")
        st.write(f"**Questions:** {today_data['easy']}E + {today_data['medium']}M + {today_data['hard']}H")
        st.write(f"**Status:** {status.upper()}")
        
        # Quick actions
        st.subheader("Quick Actions")
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("Start Day", key="start_day"):
                tracker.update_progress(day_number, 'in-progress')
                st.rerun()
        
        with action_col2:
            if st.button("Complete Day", key="complete_day"):
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
    
    # Resources section
    st.subheader("💡 Study Resources")
    resources = get_topic_resources(today_data['topics'])
    for resource in resources:
        st.write(f"• {resource}")

def get_topic_resources(topics):
    resource_map = {
        "Arrays": ["Array manipulation basics", "Two-pointer technique", "Sliding window pattern"],
        "DP": ["DP patterns sheet", "State transition practice", "Memoization vs tabulation"],
        "Graphs": ["Graph traversal algorithms", "Shortest path algorithms", "Cycle detection"],
        "Binary Trees": ["Tree traversal methods", "Tree construction", "Tree properties"],
        "Strings": ["String matching algorithms", "Palindrome problems", "String manipulation"],
        "Linked List": ["Pointer manipulation", "Cycle detection", "Reversal patterns"],
        "Searching & Sorting": ["Binary search variations", "Sorting algorithms", "Search applications"],
        "BST": ["BST properties", "Tree operations", "Balanced trees"],
        "Heap & Hashing": ["Heap operations", "Hash map applications", "Priority queues"],
        "Backtracking": ["Permutations/combinations", "Constraint satisfaction", "Pruning techniques"],
        "Greedy": ["Greedy proofs", "Interval scheduling", "Optimal selection"],
        "Bit Manipulation": ["Bit operations", "Bit masking", "Number properties"],
        "Stack & Queue": ["Stack applications", "Queue implementations", "Monotonic stacks"],
        "Tries": ["Trie implementation", "Prefix search", "String storage"],
        "Segment Tree": ["Range queries", "Tree construction", "Lazy propagation"],
        "2D Array": ["Matrix traversal", "Grid problems", "Dynamic programming on grids"]
    }
    
    resources = []
    for topic in topics:
        if topic in resource_map:
            resources.extend(resource_map[topic])
    
    return resources if resources else ["Practice fundamental problems", "Review basic concepts"]

if __name__ == "__main__":
    main()