import streamlit as st
import json
import random
from datetime import datetime, timedelta
import os

# DSA Topics with question counts [easy, medium, hard]
DSA_TOPICS = {
    "Arrays": [6, 17, 3],
    "Strings": [7, 12, 3],
    "2D Array": [0, 9, 1],
    "Searching & Sorting": [6, 10, 7],
    "Backtracking": [0, 8, 13],
    "Linked List": [7, 12, 7],
    "Stack & Queue": [6, 15, 6],
    "Greedy": [7, 9, 6],
    "Binary Trees": [14, 15, 4],
    "BST": [7, 9, 5],
    "Heap & Hashing": [0, 16, 12],
    "Graphs": [4, 25, 11],
    "Tries": [0, 4, 2],
    "DP": [9, 40, 5],
    "Bit Manipulation": [5, 5, 0],
    "Segment Tree": [0, 3, 3]
}

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
DATA_FILE = Path("dsa_progress.json")

def load_data():
    """Load progress data from file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "completed": {},
        "daily_questions": {},
        "last_generated": None
    }

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

def save_data():
    """Save progress data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.data, f, indent=2)

def generate_daily_questions(date_str):
    """Generate 5 random questions for the day"""
    random.seed(date_str)  # Consistent questions for the same day
    questions = []
    
    # Create pool of all questions
    question_pool = []
    for topic, counts in DSA_TOPICS.items():
        for diff_idx, count in enumerate(counts):
            for q_num in range(1, count + 1):
                question_pool.append({
                    "topic": topic,
                    "difficulty": DIFFICULTY_LEVELS[diff_idx],
                    "number": q_num,
                    "id": f"{topic}_{DIFFICULTY_LEVELS[diff_idx]}_{q_num}"
                })
    
    # Select 5 random questions
    if len(question_pool) >= 5:
        questions = random.sample(question_pool, 5)
    else:
        questions = question_pool
    
    return questions

def get_today_str():
    """Get today's date as string"""
    return datetime.now().strftime("%Y-%m-%d")

def mark_complete(question_id):
    """Mark a question as completed"""
    today = get_today_str()
    if today not in st.session_state.data["completed"]:
        st.session_state.data["completed"][today] = []
    
    if question_id not in st.session_state.data["completed"][today]:
        st.session_state.data["completed"][today].append(question_id)
        save_data()

def is_completed(question_id, date_str):
    """Check if a question is completed"""
    return date_str in st.session_state.data["completed"] and \
           question_id in st.session_state.data["completed"][date_str]

def get_topic_stats():
    """Calculate completion statistics by topic"""
    stats = {}
    for topic, counts in DSA_TOPICS.items():
        total = sum(counts)
        completed = 0
        for date_completed in st.session_state.data["completed"].values():
            completed += sum(1 for qid in date_completed if qid.startswith(topic + "_"))
        stats[topic] = {"total": total, "completed": completed}
    return stats

def main():
    st.set_page_config(page_title="DSA Progress Tracker", page_icon="📚", layout="wide")
    
    st.title("📚 DSA Progress Tracker")
    st.markdown("*Track your daily DSA practice with 5 random questions each day*")
    
    # Show data file location
    with st.expander("ℹ️ Data Storage Info"):
        st.caption(f"Progress saved to: `{DATA_FILE}`")
        if os.path.exists(DATA_FILE):
            file_size = os.path.getsize(DATA_FILE)
            st.caption(f"File size: {file_size} bytes")
            
            # Add export/import functionality
            col1, col2 = st.columns(2)
            with col1:
                # Export data
                with open(DATA_FILE, 'r') as f:
                    data_json = f.read()
                st.download_button(
                    label="📥 Export Progress",
                    data=data_json,
                    file_name="dsa_progress_backup.json",
                    mime="application/json"
                )
            with col2:
                # Import data
                uploaded_file = st.file_uploader("📤 Import Progress", type=['json'], key="import_data")
                if uploaded_file is not None:
                    try:
                        imported_data = json.load(uploaded_file)
                        st.session_state.data = imported_data
                        save_data()
                        st.success("✅ Progress imported successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error importing data: {e}")
        else:
            st.caption("No progress file found yet. Start solving questions to create one!")
    
    # Sidebar - Overall Progress
    with st.sidebar:
        st.header("📊 Overall Progress")
        
        topic_stats = get_topic_stats()
        total_questions = sum(sum(counts) for counts in DSA_TOPICS.values())
        total_completed = sum(stats["completed"] for stats in topic_stats.values())
        
        progress_pct = (total_completed / total_questions * 100) if total_questions > 0 else 0
        st.metric("Total Progress", f"{total_completed}/{total_questions}", 
                  f"{progress_pct:.1f}%")
        
        st.subheader("By Topic")
        for topic in sorted(DSA_TOPICS.keys()):
            stats = topic_stats[topic]
            if stats["total"] > 0:
                pct = (stats["completed"] / stats["total"] * 100)
                st.progress(pct / 100, text=f"{topic}: {stats['completed']}/{stats['total']}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Today's Questions", "📈 History", "📋 All Topics", "✏️ Manual Entry"])
    
    # Tab 1: Today's Questions
    with tab1:
        today = get_today_str()
        
        # Generate or load today's questions
        if today not in st.session_state.data["daily_questions"]:
            st.session_state.data["daily_questions"][today] = generate_daily_questions(today)
            save_data()
        
        questions = st.session_state.data["daily_questions"][today]
        
        st.header(f"🎯 Questions for {datetime.now().strftime('%B %d, %Y')}")
        
        completed_today = sum(1 for q in questions if is_completed(q["id"], today))
        st.progress(completed_today / len(questions), 
                   text=f"Completed: {completed_today}/{len(questions)}")
        
        st.divider()
        
        for idx, q in enumerate(questions, 1):
            col1, col2 = st.columns([0.9, 0.1])
            
            with col1:
                difficulty_color = {
                    "Easy": "🟢",
                    "Medium": "🟡",
                    "Hard": "🔴"
                }
                
                is_done = is_completed(q["id"], today)
                checkbox_label = f"{difficulty_color[q['difficulty']]} **{q['topic']}** - {q['difficulty']}"
                
                if is_done:
                    st.markdown(f"~~{checkbox_label}~~ ✅")
                else:
                    st.markdown(checkbox_label)
            
            with col2:
                if not is_done:
                    if st.button("✓", key=f"complete_{q['id']}", help="Mark as complete"):
                        mark_complete(q["id"])
                        st.rerun()
        
        if completed_today == len(questions):
            st.success("🎉 Congratulations! You've completed all questions for today!")
            st.balloons()
    
    # Tab 2: History
    with tab2:
        st.header("📜 Practice History")
        
        if st.session_state.data["daily_questions"]:
            dates = sorted(st.session_state.data["daily_questions"].keys(), reverse=True)
            
            for date_str in dates:
                questions = st.session_state.data["daily_questions"][date_str]
                completed_count = sum(1 for q in questions if is_completed(q["id"], date_str))
                
                with st.expander(f"📅 {date_str} - {completed_count}/{len(questions)} completed"):
                    for q in questions:
                        is_done = is_completed(q["id"], date_str)
                        status = "✅" if is_done else "⬜"
                        st.markdown(f"{status} {q['topic']} - {q['difficulty']}")
        else:
            st.info("No history yet. Start solving today's questions!")
    
    # Tab 3: All Topics
    with tab3:
        st.header("📚 All DSA Topics")
        
        col1, col2 = st.columns(2)
        
        for idx, (topic, counts) in enumerate(sorted(DSA_TOPICS.items())):
            stats = topic_stats[topic]
            total = sum(counts)
            
            with col1 if idx % 2 == 0 else col2:
                st.subheader(topic)
                st.caption(f"Easy: {counts[0]} | Medium: {counts[1]} | Hard: {counts[2]}")
                
                if total > 0:
                    progress = stats["completed"] / total
                    st.progress(progress, text=f"{stats['completed']}/{total} solved")
                else:
                    st.caption("No questions available")
                
                st.divider()
    
    # Tab 4: Manual Entry
    with tab4:
        st.header("✏️ Manually Mark Questions")
        st.markdown("*Manually mark questions as solved to update your progress*")
        
        st.divider()
        
        # Topic selection
        selected_topic = st.selectbox("Select Topic", sorted(DSA_TOPICS.keys()))
        
        if selected_topic:
            counts = DSA_TOPICS[selected_topic]
            
            st.subheader(f"📚 {selected_topic}")
            st.caption(f"Total: {sum(counts)} questions (Easy: {counts[0]}, Medium: {counts[1]}, Hard: {counts[2]})")
            
            # Create columns for each difficulty
            col1, col2, col3 = st.columns(3)
            
            difficulties = ["Easy", "Medium", "Hard"]
            today = get_today_str()
            
            for idx, (col, difficulty, count) in enumerate(zip([col1, col2, col3], difficulties, counts)):
                with col:
                    if count > 0:
                        st.markdown(f"**🟢 {difficulty}**" if idx == 0 else f"**🟡 {difficulty}**" if idx == 1 else f"**🔴 {difficulty}**")
                        
                        # Count completed for this difficulty
                        completed_in_diff = sum(
                            1 for completed_list in st.session_state.data["completed"].values()
                            for qid in completed_list 
                            if qid.startswith(f"{selected_topic}_{difficulty}_")
                        )
                        st.caption(f"{completed_in_diff}/{count} solved")
                        st.write("")
                        
                        for q_num in range(1, count + 1):
                            question_id = f"{selected_topic}_{difficulty}_{q_num}"
                            
                            # Check if question is already completed (across all dates)
                            is_completed_ever = any(
                                question_id in completed_list 
                                for completed_list in st.session_state.data["completed"].values()
                            )
                            
                            # Use on_change callback for immediate update
                            def toggle_question(qid=question_id):
                                today = get_today_str()
                                # Check current state
                                is_done = any(
                                    qid in completed_list 
                                    for completed_list in st.session_state.data["completed"].values()
                                )
                                
                                if not is_done:
                                    # Mark as complete
                                    mark_complete(qid)
                                else:
                                    # Remove from all dates
                                    for date_str in list(st.session_state.data["completed"].keys()):
                                        if qid in st.session_state.data["completed"][date_str]:
                                            st.session_state.data["completed"][date_str].remove(qid)
                                    save_data()
                            
                            st.checkbox(
                                f"Question {q_num}", 
                                value=is_completed_ever,
                                key=f"manual_{question_id}_{selected_topic}",
                                on_change=toggle_question
                            )
                    else:
                        st.markdown(f"**{difficulty}**")
                        st.caption("No questions")
            
            # Show summary
            st.divider()
            topic_completed = sum(
                1 for completed_list in st.session_state.data["completed"].values()
                for qid in completed_list if qid.startswith(selected_topic + "_")
            )
            total_topic = sum(counts)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                progress_pct = (topic_completed / total_topic * 100) if total_topic > 0 else 0
                st.progress(progress_pct / 100)
                st.metric(f"{selected_topic} Progress", f"{topic_completed}/{total_topic}", f"{progress_pct:.1f}%")

if __name__ == "__main__":
    main()