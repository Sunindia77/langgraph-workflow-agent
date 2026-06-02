"""Streamlit UI for LangGraph Multi-Agent Workflow System."""
import asyncio
import logging
from typing import Optional
import streamlit as st
from datetime import datetime

from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="LangGraph Workflow Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 2rem;
        }
        .query-input {
            font-size: 16px;
        }
        .result-box {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
        }
        .success-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #c3e6cb;
            margin-top: 1rem;
        }
        .info-box {
            background-color: #d1ecf1;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #bee5eb;
            margin-top: 1rem;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #f5c6cb;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>🤖 LangGraph Multi-Agent Workflow System</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # System information
    st.subheader("System Info")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "🟢 Active")
    with col2:
        st.metric("Time", datetime.now().strftime("%H:%M:%S"))
    
    st.divider()
    
    # Configuration
    st.subheader("Configuration")
    show_logs = st.checkbox("Show Debug Logs", value=False)
    show_details = st.checkbox("Show Detailed Results", value=True)
    
    st.divider()
    
    # Instructions
    st.subheader("📋 Instructions")
    st.markdown("""
    1. Enter your query in the text box
    2. Click "Analyze Query" or press Enter
    3. View results and workflow output
    4. Browse history to run previous queries
    """)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "coordinator" not in st.session_state:
    st.session_state.coordinator = None

# Initialize query variable
if "selected_query" not in st.session_state:
    st.session_state.selected_query = None

# History section (before query input)
with st.expander("📚 Query History", expanded=False):
    if st.session_state.history:
        st.write("Click a query to re-run it:")
        for i, item in enumerate(reversed(st.session_state.history)):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"🕐 {item['timestamp']} - {item['query'][:50]}...", key=f"history_{i}"):
                    st.session_state.selected_query = item['query']
                    st.rerun()
            with col2:
                if st.button("❌", key=f"delete_{i}"):
                    st.session_state.history.pop(len(st.session_state.history) - 1 - i)
                    st.rerun()
    else:
        st.info("No query history yet. Run a query to see it appear here.")

st.divider()

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Query input
    query = st.text_area(
        "Enter your query:",
        placeholder="E.g., What is machine learning? How does deep learning work?",
        height=100,
        value=st.session_state.selected_query or ""
    )

with col2:
    st.write("")
    st.write("")
    analyze_button = st.button("🔍 Analyze Query", type="primary", use_container_width=True)

# Clear selected query after use
if st.session_state.selected_query:
    st.session_state.selected_query = None

st.divider()

# Results section
if analyze_button or query:
    if not query.strip():
        st.error("❌ Please enter a query before analyzing.")
    else:
        # Add to history
        st.session_state.history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Initialize coordinator if needed
        if st.session_state.coordinator is None:
            st.session_state.coordinator = CoordinatorAgent()
        
        # Create a status container
        status_container = st.container()
        
        with status_container:
            st.markdown("### 🔄 Workflow Execution")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Run workflow
            async def run_workflow():
                """Run the workflow asynchronously."""
                try:
                    coordinator = st.session_state.coordinator
                    
                    # Phase 1: Research
                    status_text.text("📡 Phase 1: RESEARCH - Gathering information...")
                    progress_bar.progress(25)
                    
                    state = WorkflowState(query=query)
                    result = await coordinator.execute(state)
                    
                    # Phase 2: Analysis
                    status_text.text("📊 Phase 2: ANALYSIS - Analyzing information...")
                    progress_bar.progress(60)
                    
                    # Phase 3: Synthesis
                    status_text.text("✨ Phase 3: SYNTHESIS - Synthesizing results...")
                    progress_bar.progress(90)
                    
                    # Complete
                    status_text.text("✅ Workflow Complete!")
                    progress_bar.progress(100)
                    
                    return result
                except Exception as e:
                    logger.error(f"Workflow error: {str(e)}")
                    status_text.error(f"❌ Error: {str(e)}")
                    return None
            
            # Execute workflow
            result = asyncio.run(run_workflow())
            
            if result:
                st.markdown("---")
                st.markdown("### ✅ Results")
                
                # Results tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🔍 Details", "📊 Metrics", "📝 Full Answer"])
                
                with tab1:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Sources Processed", len(result.search_results))
                    with col2:
                        st.metric("Messages", len(result.messages))
                    with col3:
                        st.metric("Analysis Steps", len(result.analysis_results.get('steps', [])))
                    with col4:
                        st.metric("Tool Calls", len(result.tool_calls))
                
                with tab2:
                    if show_details:
                        with st.expander("📡 Search Results", expanded=True):
                            if result.search_results:
                                for i, search_result in enumerate(result.search_results[:5], 1):
                                    st.write(f"**Result {i}:**")
                                    st.write(search_result)
                                    st.divider()
                            else:
                                st.info("No search results available.")
                        
                        with st.expander("🔧 Analysis Results", expanded=True):
                            if result.analysis_results:
                                analysis_steps = result.analysis_results.get('steps', [])
                                for i, step in enumerate(analysis_steps[:5], 1):
                                    st.write(f"**Step {i}:** {step}")
                                st.json(result.analysis_results)
                            else:
                                st.info("No analysis results available.")
                        
                        with st.expander("📋 Messages", expanded=False):
                            if result.messages:
                                for i, msg in enumerate(result.messages[:10], 1):
                                    st.write(f"**Message {i}:** {msg}")
                            else:
                                st.info("No messages available.")
                
                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Search Results", len(result.search_results))
                        st.metric("Messages Processed", len(result.messages))
                    with col2:
                        st.metric("Tool Executions", len(result.tool_calls))
                        st.metric("Analysis Quality", "✅ Complete")
                
                with tab4:
                    if result.final_answer:
                        st.markdown("#### Final Answer")
                        st.markdown(result.final_answer)
                    else:
                        st.info("No final answer generated. Check the workflow logs.")
                
                # Logs section
                if show_logs:
                    st.markdown("---")
                    with st.expander("📜 Debug Logs", expanded=False):
                        st.json({
                            "query": result.query,
                            "messages_count": len(result.messages),
                            "search_results_count": len(result.search_results),
                            "tool_calls_count": len(result.tool_calls),
                            "analysis_results": result.analysis_results
                        })
