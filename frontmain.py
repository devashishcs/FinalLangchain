import streamlit as st
from main import run_llm

# Full purple-themed CSS with enhanced sidebar styling
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background: linear-gradient(120deg, #8e44ad 0%, #c471ed 50%, #f64f59 100%);
        background-attachment: fixed;
        background-size: cover;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(120deg, #6a3093 0%, #a044ff 100%) !important;
        color: white;
    }
    [data-testid="stSidebarContent"] {
        padding: 1.5rem;
        background: transparent !important;
        color: white;
    }
    .stAppToolbar {
        background: linear-gradient(120deg, #6a3093 0%, #a044ff 100%) !important;
        color: white !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Enhanced sidebar collapse button visibility */
    [data-testid="stSidebarCollapseButton"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 8px !important;
        color: white !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(255, 255, 255, 0.5) !important;
        border-color: white !important;
        transform: scale(1.05);
    }
    
    /* Menu item styling */
    .menu-item {
        display: block;
        padding: 12px 16px;
        margin: 8px 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: left;
    }
    .menu-item:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
    }
    .menu-item.active {
        background: linear-gradient(90deg, #ffffff20, #ffffff30);
        border-color: rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
    }
    .menu-item-icon {
        margin-right: 10px;
        font-size: 1.1rem;
    }
    
    .profile-pic {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid #ffffff;
        margin-bottom: 12px;
        object-fit: cover;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(255,255,255,0.2);
    }
    .app-desc {
        font-size: 1.1rem;
        color: #f0e6ff;
        text-align: center;
        margin-bottom: 15px;
    }
    .main-heading {
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 0 2px 12px #5e1780;
        margin-bottom: 24px;
        text-align: center;
    }
    /* Main content text inputs only */
    .main .stTextInput > div > div > input {
        background: rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        border: 2px solid #cc8af0 !important;
        font-size: 1.1rem !important;
        color: white !important;
        padding: 10px !important;
    }
    .main .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    .main .stTextInput > div > div > input:focus {
        background: rgba(255,255,255,0.25) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.3) !important;
        outline: none !important;
    }
    .main .stTextInput > label {
        color: white !important;
        font-weight: 600 !important;
    }
    .main .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        border: 2px solid #cc8af0 !important;
        font-size: 1.1rem !important;
        color: white !important;
        padding: 10px !important;
    }
    .main .stTextArea > div > div > textarea::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    .main .stTextArea > div > div > textarea:focus {
        background: rgba(255,255,255,0.25) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.3) !important;
        outline: none !important;
    }
    .main .stTextArea > label {
        color: white !important;
        font-weight: 600 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #a678c7 0%, #8e44ad 100%);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 10px 18px;
        box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.2);
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        margin-bottom: 12px;
        padding: 12px 20px;
        color: #ffffff;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .stAlert {
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
    }
    hr {
        border-color: rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for menu selection
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = "Previous Chat"

# Sidebar with custom menu
with st.sidebar:
    st.markdown(
        '<img src="https://i.pravatar.cc/150?img=8" class="profile-pic" alt="Profile Picture"/>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="app-title">📄 Document Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-desc">Your intelligent assistant for exploring, querying, and summarizing documents with ease.</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # Custom menu items
    menu_items = [
        ("Previous Chat", "💬"),
        ("Document Upload", "📁"),
        ("Editor", "✏️"),
        ("About Us", "ℹ️")
    ]
    
    for item, icon in menu_items:
        active_class = "active" if st.session_state["selected_menu"] == item else ""
        if st.button(f"{icon} {item}", key=f"menu_{item}", use_container_width=True):
            st.session_state["selected_menu"] = item
            st.rerun()
    
    st.markdown("---")
    st.info("💡 Tip: Ask questions like *What is the diagnosis?* or *Summarize the report*.")
    st.write("📁 You can upload your files in the document upload section.")

# Main heading
st.markdown('<div class="main-heading">Document Assistant</div>', unsafe_allow_html=True)

# Session initialization
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Menu logic based on selected menu
if st.session_state["selected_menu"] == "Previous Chat":
    # Display chat history
    if st.session_state["chat_answer_history"]:
        for user_query, generated_response in zip(
            st.session_state["user_prompt_history"], st.session_state["chat_answer_history"]
        ):
            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(generated_response)
    else:
        st.info("No previous chats yet.")
        
    # Place the input at the bottom of the chat
    prompt = st.text_input("Prompt", placeholder="Enter your Prompt here...", label_visibility="collapsed")
    
    # Processing user input
    if prompt and (not st.session_state["user_prompt_history"] or prompt != st.session_state["user_prompt_history"][-1]):
        with st.spinner("✨ Generating Response..."):
            langchain_chat_history = [(r, c) for r, c in st.session_state["chat_history"]]
            generated_response = run_llm(query=prompt, chat_history=langchain_chat_history)

            if not generated_response["source_documents"]:
                formatted_response = f"{generated_response['result']}  \n\n_No source documents found._"
            else:
                sources = set(doc.metadata["source"] for doc in generated_response["source_documents"])
                formatted_response = f"{generated_response['result']}  \n\n**Sources:** {sources}"

            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response["result"]))
            
            # Rerun to show the new messages
            st.rerun()
        
elif st.session_state["selected_menu"] == "Document Upload":
    st.subheader("📁 Upload Your Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
        # Add your document processing logic here
        
elif st.session_state["selected_menu"] == "Editor":
    st.subheader("✏️ Document Editor")
    st.text_area("Edit your document here", height=300, placeholder="Start typing your document...")
    col1, col2 = st.columns(2)
    with col1:
        st.button("💾 Save Document")
    with col2:
        st.button("🔄 Clear All")
    
elif st.session_state["selected_menu"] == "About Us":
    st.subheader("ℹ️ About Document Assistant")
    st.markdown("""
        ### Welcome to Document Assistant! 🚀
        
        This intelligent application helps you:
        - **Explore** your documents with ease
        - **Query** specific information quickly  
        - **Summarize** long documents efficiently
        - **Chat** with your documents naturally
        
        **Features:**
        - 📄 Support for PDF, DOCX, and TXT files
        - 💬 Interactive chat interface
        - 🔍 Smart document search
        - 📝 Built-in document editor
        
        ---
        **Created with ❤️ by Your Team**
        
        For support or feedback, please contact us!
    """)