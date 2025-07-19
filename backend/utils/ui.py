"""
UI utility functions for the Business Analysis Tool
Updated to work with both Streamlit and FastAPI backends
"""

import streamlit as st
import os

def init_layout():
    """Initialize the basic layout and styles."""
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .custom-divider {
        margin: 2rem 0;
        padding: 5px;
        background-color: #f0f2f6;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .deloitte-green {
        color: #86bc25;
        font-weight: bold;
    }
    .status-active {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .status-inactive {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def show_logo():
    """Display the tool logo."""
    col1, col2 = st.columns([1, 5])
    with col1:
        # Try to load the specific logo file
        try:
            # Check for the specific Deloitte logo file
            if os.path.exists("assets/Partner_logo_16-9_Deloitte.png"):
                st.image("assets/Partner_logo_16-9_Deloitte.png", width=100)
            elif os.path.exists("assets/Partner_logo_16-9_Deloitte.jpg"):
                st.image("assets/Partner_logo_16-9_Deloitte.jpg", width=100)
            elif os.path.exists("assets/Partner_logo_16-9_Deloitte.svg"):
                st.image("assets/Partner_logo_16-9_Deloitte.svg", width=100)
            # Check for generic logo files as fallback
            elif os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", width=100)
            elif os.path.exists("assets/logo.jpg"):
                st.image("assets/logo.jpg", width=100)
            else:
                # Use Deloitte logo from URL as fallback
                st.image("https://upload.wikimedia.org/wikipedia/commons/5/56/Deloitte.svg", width=100)
        except Exception as e:
            # Fallback to text if image loading fails
            st.markdown("## 📊")
            st.write(f"Logo error: {str(e)}")
    
    with col2:
        st.title("Business Analysis Tool")
        st.markdown('<p class="deloitte-green">Powered by Deloitte</p>', unsafe_allow_html=True)

def show_dashboard_titles(active_page):
    """Display the page title based on active page."""
    if active_page == "Dashboard":
        st.header("🏠 Dashboard")
    elif active_page == "RAG/CAG":
        st.header("📚 RAG/CAG Document Manager")
    elif active_page == "Data Analytics":
        st.header("📈 Data Analytics")
    elif active_page == "Parameter":
        st.header("⚙️ Parameter Configuration")
    else:
        st.header(active_page)

def custom_divider(text=""):
    """Create a custom divider with optional text."""
    if text:
        html = f'<div class="custom-divider deloitte-green">{text}</div>'
    else:
        html = '<div class="custom-divider"></div>'
    
    st.markdown(html, unsafe_allow_html=True)
    return html

def show_system_status():
    """Display system status indicators."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if os.path.exists("rag_docs_vectorstore"):
            st.markdown('<div class="status-active">✅ RAG System: Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-inactive">⚠️ RAG System: No vector database</div>', unsafe_allow_html=True)
    
    with col2:
        if os.path.exists("cag_docs_vectorstore"):
            st.markdown('<div class="status-active">✅ CAG System: Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-inactive">⚠️ CAG System: No vector database</div>', unsafe_allow_html=True)
    
    with col3:
        # Check if Ollama/llama3 is available (simplified check)
        try:
            from langchain.llms import Ollama
            st.markdown('<div class="status-active">✅ AI Integration: Ready</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="status-inactive">⚠️ AI Integration: Check Ollama</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="status-active">✅ Analytics: SQL & Mapping Ready</div>', unsafe_allow_html=True)

def show_file_upload_section(doc_type, description):
    """Show a file upload section for RAG or CAG documents."""
    st.subheader(f"{doc_type.upper()} Documents")
    st.write(description)
    
    files = st.file_uploader(
        f"Upload {doc_type.upper()} documents", 
        type=["txt", "pdf", "md", "csv", "xlsx"], 
        accept_multiple_files=True, 
        key=doc_type.lower()
    )
    
    return files

def show_document_library(doc_type):
    """Display uploaded documents library."""
    from pathlib import Path
    
    st.subheader(f"{doc_type.upper()} Documents Library")
    doc_path = Path(f"{doc_type.lower()}_docs")
    
    if doc_path.exists():
        docs = list(doc_path.glob("*"))
        if docs:
            for i, doc in enumerate(docs):
                col_doc, col_action = st.columns([3, 1])
                with col_doc:
                    st.write(f"📄 {doc.name}")
                with col_action:
                    if st.button("Delete", key=f"del_{doc_type.lower()}_{i}"):
                        try:
                            os.remove(doc)
                            st.success(f"Deleted {doc.name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {str(e)}")
        else:
            st.info(f"No {doc_type.upper()} documents uploaded yet.")
    else:
        st.info(f"No {doc_type.upper()} documents uploaded yet.")

def show_chat_interface():
    """Display the chat interface for document interaction."""
    st.subheader("💬 Chat with your Documents")
    
    # Initialize chat history
    if "rag_cag_messages" not in st.session_state:
        st.session_state.rag_cag_messages = []
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.rag_cag_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("View Sources"):
                        for i, source in enumerate(message["sources"]):
                            st.write(f"**Source {i+1}:** {source}")
    
    # Chat input
    if prompt := st.chat_input("Ask something based on your documents..."):
        # Add user message to chat history
        st.session_state.rag_cag_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Here you would integrate with your RAG/CAG system
                response = "This is where your RAG/CAG response would appear. Integration with your existing system is needed."
                st.write(response)
                
                # Add assistant response to chat history
                st.session_state.rag_cag_messages.append({
                    "role": "assistant", 
                    "content": response
                })

def show_sql_interface():
    """Display the SQL query interface."""
    st.subheader("🔍 Natural Language to SQL")
    
    # Mode selection
    mode = st.radio("Modus auswählen", ["SQL Abfrage", "Mapping Abgleich"], horizontal=True)
    
    if mode == "SQL Abfrage":
        # Query input
        natural_query = st.text_area(
            "Natürliche Sprache Anfrage",
            placeholder="Beschreiben Sie Ihre Anfrage in natürlicher Sprache...",
            height=100
        )
        
        # Options
        col1, col2, col3 = st.columns(3)
        with col1:
            use_rag = st.checkbox("RAG Kontext verwenden", value=True)
        with col2:
            use_cag = st.checkbox("CAG Kontext verwenden", value=True)
        with col3:
            modify_db = st.checkbox("Datenbank ändern", value=False)
        
        # Generate SQL button
        if st.button("SQL Generieren", type="primary"):
            if natural_query.strip():
                with st.spinner("Generiere SQL..."):
                    # Here you would integrate with your existing SQL generation
                    sql_query = f"-- Generated from: {natural_query}\nSELECT * FROM sample_table WHERE condition = 'example';"
                    
                    st.subheader("Generated SQL:")
                    st.code(sql_query, language="sql")
                    
                    if st.button("Execute Query"):
                        st.success("Query executed successfully! (Mock response)")
            else:
                st.error("Please enter a natural language query first.")
    
    else:
        st.info("Mapping comparison functionality will be available here.")

def show_parameter_settings():
    """Display parameter configuration interface."""
    st.subheader("🔧 RAG/CAG Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chunk_size = st.slider(
            "Chunk Size", 
            min_value=100, 
            max_value=2000, 
            value=1000, 
            step=100,
            help="Size of document chunks for retrieval."
        )
        
        chunk_overlap = st.slider(
            "Chunk Overlap", 
            min_value=0, 
            max_value=500, 
            value=200, 
            step=50,
            help="Overlap between chunks for context continuity."
        )
    
    with col2:
        num_chunks = st.slider(
            "Number of chunks to retrieve", 
            min_value=1, 
            max_value=10, 
            value=4, 
            step=1,
            help="Number of document chunks to retrieve for each query."
        )
        
        embedding_model = st.selectbox(
            "Embedding Model",
            options=["all-MiniLM-L6-v2", "all-mpnet-base-v2"],
            format_func=lambda x: {
                "all-MiniLM-L6-v2": "all-MiniLM-L6-v2 (Default, Fast)",
                "all-mpnet-base-v2": "all-mpnet-base-v2 (Better quality, Slower)"
            }[x],
            help="Model used to create embeddings for document chunks"
        )
    
    if st.button("Save Settings", type="primary"):
        # Save settings to session state or file
        st.session_state.rag_settings = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "num_chunks": num_chunks,
            "embedding_model": embedding_model
        }
        st.success("Settings saved! Rebuild your vector databases for settings to take effect.")
        
        # Display current settings
        st.subheader("Current Configuration")
        st.json(st.session_state.rag_settings)

def create_navigation_buttons():
    """Create navigation buttons for page switching."""
    col1, col2, col3, col4 = st.columns(4)
    
    buttons = {}
    with col1:
        buttons["Dashboard"] = st.button("📊 Dashboard", use_container_width=True)
    with col2:
        buttons["RAG/CAG"] = st.button("📄 RAG/CAG", use_container_width=True)
    with col3:
        buttons["Data Analytics"] = st.button("📈 Data Analytics", use_container_width=True)
    with col4:
        buttons["Parameter"] = st.button("⚙️ Parameter", use_container_width=True)
    
    return buttons