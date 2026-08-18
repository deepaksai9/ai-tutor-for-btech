import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Check for API Key in Streamlit Secrets or Environment
load_dotenv()

# Import Chains
try:
    from chains.assessment_chain import create_assessment_chain
    from chains.learning_path_chain import create_learning_path_chain
    from chains.lesson_chain import create_lesson_chain
    from chains.quiz_chain import create_quiz_chain
    from chains.evaluation_chain import create_evaluation_chain
    from memory.progress_store import ProgressStore
except ModuleNotFoundError:
    # If running from parent directory
    from ai_tutor.chains.assessment_chain import create_assessment_chain
    from ai_tutor.chains.learning_path_chain import create_learning_path_chain
    from ai_tutor.chains.lesson_chain import create_lesson_chain
    from ai_tutor.chains.quiz_chain import create_quiz_chain
    from ai_tutor.chains.evaluation_chain import create_evaluation_chain
    from ai_tutor.memory.progress_store import ProgressStore

# Setup Page
st.set_page_config(page_title="AI Genius Tutor", page_icon="🧠", layout="wide")

# Custom UI Styling
st.markdown("""
<style>
    /* Styling for the main app container - Light Mode */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    
    /* Custom button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 2.8em;
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    
    /* Header gradients */
    h1, h2, h3 {
        color: #1a1a1a;
        font-weight: 700;
        background: none;
        -webkit-text-fill-color: initial;
    }
    
    /* Card-like containers for metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 5px;
        color: #495057;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f5e9;
        color: #2e7d32;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🧠 AI Genius Tutor")
    st.markdown("Your personalized path to coding mastery.")
    
    st.divider()
    
    user_id = st.text_input("User Profile", "student_01")
    
    if st.button("Load Profile"):
        st.session_state["user_id"] = user_id
        st.rerun()

    # Reset
    st.markdown("---")
    if st.button("♻️ Reset All Progress", type="secondary"):
        if "user_id" in st.session_state:
            s = ProgressStore(st.session_state["user_id"])
            s.data = s._default_structure()
            s.save()
            st.rerun()

# --- Initialization ---
if "user_id" not in st.session_state:
    st.session_state["user_id"] = user_id

store = ProgressStore(st.session_state["user_id"])

# Use Groq
llm = ChatGroq(
    temperature=0.7, 
    model_name="openai/gpt-oss-20b", 
    api_key=os.getenv("GROQ_API_KEY")
)

# --- Main App Flow ---

# 1. Assessment Phase and Language Selection
if not store.get_user_level():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎯 Skill Assessment")
        st.markdown("### Let's find your starting point")
        st.write("First, what do you want to learn today?")
        
        # Language Selection
        language_input = st.text_input("Enter Programming Language", "Python", help="e.g. Python, JavaScript, Rust, Go")
    
    with col2:
        st.markdown(f"### Assessing for: **{language_input}**")
        st.write("Answer a few questions to generate your personalized curriculum.")
    
    with st.form("assessment_form"):
        q1 = st.radio(f"What is your experience with {language_input}?", 
                      ["None", "I know basic syntax", f"I work with {language_input} professionally"])
        
        q2 = st.radio("How comfortable are you with concepts like recursion or memory management?", 
                      ["Not at all", "Somewhat comfortable", "Very comfortable"])
        
        q3 = st.radio("Have you built any projects independently?", 
                      ["No", "Small scripts", "Full applications"])
        
        submitted = st.form_submit_button("🚀 Launch My Journey")
        
        if submitted:
            store.set_language(language_input)
            with st.spinner(f"Analyzing your {language_input} profile..."):
                user_answers = f"1. {q1}\n2. {q2}\n3. {q3}"
                chain = create_assessment_chain(llm)
                
                try:
                    data = chain.invoke({"user_answers": user_answers, "language": language_input})
                    store.update_assessment(data['level'], data.get('strengths', []), data.get('weaknesses', []))
                    st.success(f"Assessment complete! You are at level: **{data['level']}**")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing assessment: {e}")

# 2. Learning Path Generation
elif not store.get_learning_path():
    level = store.get_user_level()
    language = store.get_language()
    st.header(f"🚀 Building Your {language} Roadmap ({level})")
    
    with st.spinner("Constructing your 30-day journey..."):
        chain = create_learning_path_chain(llm)
        
        try:
            path = chain.invoke({"level": level, "language": language})
            store.save_learning_path(path)
            st.success("Roadmap generated!")
            st.rerun()
        except Exception as e:
            st.error(f"Error generating path: {e}")

# 3. Learning Dashboard
else:
    level = store.get_user_level()
    language = store.get_language()
    
    st.markdown(f"## 🎓 {language} Mastery | {level}")
    
    # Metrics
    path = store.get_learning_path()
    total = 30
    completed = len(store.data.get("completed_days", []))
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Current Streak", f"{completed} Days")
    col_m2.metric("XP Score", f"{completed * 100}")
    
    next_topic_key = "day_" + str(completed + 1)
    next_topic = path.get(next_topic_key, {}).get("topic", "All complete!")
    col_m3.metric("Next Topic", next_topic)
    
    st.progress(completed / total)
    
    st.divider()
    
    # Content Area
    col_nav, col_content = st.columns([1, 2])
    
    with col_nav:
        st.subheader("📅 Curriculum")
        days = list(path.keys())
        days = sorted(days, key=lambda x: int(x.split('_')[1]))
        
        # Find index for current day
        current_day_idx = min(completed, len(days)-1)
        selected_day_key = st.selectbox("Select Day", days, index=current_day_idx, format_func=lambda x: f"Day {x.split('_')[1]}: {path[x]['topic']}")
        
        day_num = int(selected_day_key.split('_')[1])
        day_content = path[selected_day_key]
        
        st.info(f"**Goal**: {day_content['goal']}")
        st.caption(f"**Practice**: {day_content.get('practice', '')}")

    with col_content:
        st.subheader(f"Day {day_num}: {day_content['topic']}")
        
        # Tabs for Workflow
        tab_lesson, tab_quiz, tab_eval = st.tabs(["📚 Learn", "📝 Practice", "🏆 Result"])
        
        # --- Lesson Tab ---
        with tab_lesson:
           
            if st.button("Start Lesson", key="btn_lesson"):
                with st.spinner("AI Tutor is preparing your lesson..."):
                    chain = create_lesson_chain(llm)
                    lesson_text = chain.invoke({
                        "topic": day_content['topic'], 
                        "level": level,
                        "language": language
                    })
                    st.session_state["current_lesson_content"] = lesson_text
                    
            if "current_lesson_content" in st.session_state:
                st.markdown(st.session_state["current_lesson_content"])
            else:
                st.write("Click 'Start Lesson' to begin.")
                
        # --- Quiz Tab ---
        with tab_quiz:
            if st.button("Generate Challenge", key="btn_quiz"):
                with st.spinner("Generating challenges..."):
                    chain = create_quiz_chain(llm)
                    try:
                        q_obj = chain.invoke({
                            "topic": day_content['topic'], 
                            "level": level,
                            "language": language
                        })
                        st.session_state["quiz_object"] = q_obj
                        st.session_state["quiz_answers"] = {} 
                    except Exception as e:
                        st.error(f"Failed to generate quiz JSON: {e}")
            
            if "quiz_object" in st.session_state:
                q_obj = st.session_state["quiz_object"]
                
                with st.form("quiz_form"):
                    user_responses = {}
                    
                    # MCQs
                    if "mcq" in q_obj:
                        st.markdown("### Multiple Choice")
                        for idx, item in enumerate(q_obj["mcq"]):
                            st.write(f"**{idx+1}. {item['question']}**")
                            user_responses[f"mcq_{idx}"] = st.radio(
                                "Select Option:", item['options'], key=f"radio_{idx}", label_visibility="collapsed"
                            )
                        st.divider()
                    
                    # Coding
                    if "coding" in q_obj:
                        st.markdown("### Coding Challenge")
                        st.write(q_obj["coding"].get("question"))
                        user_responses["code_answer"] = st.text_area("Your Solution:", height=150)
                    
                    submitted_quiz = st.form_submit_button("Submit Solution")
                    if submitted_quiz:
                        st.session_state["quiz_answers_submitted"] = user_responses
                        st.success("Answers submitted! check the Result tab.")
            else:
                 st.info("Ready to practice? Generate a challenge!")
    
        # --- Evaluation Tab ---
        with tab_eval:
            if "quiz_answers_submitted" in st.session_state:
                if st.button("Evaluate My Work"):
                    with st.spinner("Grading..."):
                        chain = create_evaluation_chain(llm)
                        
                        try:
                            eval_data = chain.invoke({
                                "topic": day_content['topic'],
                                "level": level,
                                "language": language,
                                "user_submission": str(st.session_state["quiz_answers_submitted"]),
                                "quiz_data": str(st.session_state.get("quiz_object", {}))
                            })
                            
                            score = eval_data.get("score", 0)
                            
                            col_res1, col_res2 = st.columns([1,3])
                            with col_res1:
                                st.metric("Your Score", f"{score}/100")
                            
                            with col_res2:
                                if score >= 70:
                                    st.balloons()
                                    st.success("🎉 Excellent! You've mastered this topic.")
                                    store.mark_day_complete(day_num)
                                    store.add_quiz_score(day_num, day_content['topic'], score)
                                else:
                                    st.warning("Keep practicing. You need 70% to advance.")
                                
                            st.markdown("### 💡 Feedback")
                            st.info(eval_data.get("feedback"))
                            
                            st.markdown("### 🌟 Recommendation")
                            st.write(eval_data.get("recommendation"))
                            
                        except Exception as e:
                            st.error(f"Error reading evaluation result: {e}")
            else:
                st.write("Submit your quiz answers first.")