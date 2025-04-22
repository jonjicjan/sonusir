try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import pickle
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
    import time
except Exception as e:
    st.error(f"Error loading dependencies: {str(e)}")
    st.info("Please check if all required packages are installed correctly.")
    st.stop()

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'model_info' not in st.session_state:
    st.session_state.model_info = None
if 'label_encoder' not in st.session_state:
    st.session_state.label_encoder = None
if 'scaler' not in st.session_state:
    st.session_state.scaler = None
if 'feature_names' not in st.session_state:
    st.session_state.feature_names = None

# Page configuration
st.set_page_config(
    page_title="Intranet Attack Detection",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Modern color scheme and base styles */
    :root {
        --primary: #4f46e5;
        --primary-light: #818cf8;
        --secondary: #0ea5e9;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --background: #f8fafc;
        --text: #1e293b;
    }

    .header-container {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(14, 165, 233, 0.1) 100%);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }

    .main-title {
        color: var(--text);
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: var(--text);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.9;
    }

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Container styles */
    .main {
        padding: 2rem;
    }

    .block-container {
        padding: 2rem;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Button styles */
    .stButton>button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Heading styles */
    h1 {
        color: var(--text);
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: var(--text);
        font-size: 1.875rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    h3 {
        color: var(--text);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* DataFrame styles */
    .stDataFrame {
        background: white;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Markdown content */
    .stMarkdown {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Sidebar styles */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary) 0%, var(--primary-light) 100%);
        padding: 2rem 1rem;
    }

    div[data-testid="stSidebarNav"] {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.75rem;
        backdrop-filter: blur(10px);
    }

    .sidebar .sidebar-content {
        background: transparent;
    }

    /* Success/Info/Warning/Error message styling */
    .stSuccess, div[data-baseweb="notification"] {
        background: white !important;
        border-radius: 0.75rem !important;
        border-left: 4px solid var(--success) !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }

    .stInfo {
        background: white !important;
        border-radius: 0.75rem !important;
        border-left: 4px solid var(--secondary) !important;
        padding: 1rem !important;
    }

    .stWarning {
        background: white !important;
        border-radius: 0.75rem !important;
        border-left: 4px solid var(--warning) !important;
        padding: 1rem !important;
    }

    .stError {
        background: white !important;
        border-radius: 0.75rem !important;
        border-left: 4px solid var(--danger) !important;
        padding: 1rem !important;
    }

    /* Input fields */
    .stNumberInput input, .stTextInput input {
        border-radius: 0.5rem !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--primary) !important;
    }

    /* File uploader */
    .stFileUploader {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        border: 2px dashed #e2e8f0;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: var(--primary);
    }

    /* Selectbox */
    .stSelectbox {
        border-radius: 0.5rem !important;
    }

    .stSelectbox > div {
        background: white;
        border-radius: 0.5rem !important;
    }

    /* Plot styling */
    .stPlot {
        background: white;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Caching for performance
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

@st.cache_data
def create_visualizations(df):
    figs = {}
    
    # Correlation Heatmap
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.select_dtypes(include=['number']).corr(), 
                cmap="coolwarm", 
                annot=True, 
                fmt='.2f', 
                linewidths=0.5)
    plt.title("Feature Correlation Heatmap")
    figs['correlation'] = fig1

    # Class Distribution
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='type', order=df['type'].value_counts().index)
    plt.title("Class Distribution")
    plt.xticks(rotation=45)
    figs['distribution'] = fig2

    return figs

# Main menu
menu = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Home", "📊 Upload & Train", "🔮 Prediction", "📚 Attack Types"],
    key="navigation"
)

# Home page
if menu == "🏠 Home":
    # Add hero image and title in a container
    st.markdown("""
        <div class="header-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" 
                 style="width: 150px; margin-bottom: 1.5rem;">
            <div class="main-title">An Advanced Approach for Detecting Behavior-Based Intranet Attacks</div>
            <div class="subtitle">Machine Learning Classification Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🤖 Machine Learning Classification Platform")
    
    # Add decorative images alongside content
    st.markdown("""
        <div style="display: flex; align-items: center; margin: 2rem 0;">
            <div style="flex: 1;">
                <img src="https://emeritus.org/in/wp-content/uploads/sites/3/2023/01/What-is-machine-learning-Definition-types.jpg.optimal.jpg" 
                     style="width: 70%; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            </div>
            <div style="flex: 1; padding-left: 2rem;">
                <h3>Welcome to the ML Classification Platform!</h3>
                <p>This application helps you:</p>
                <ol>
                    <li><strong>Upload</strong> your dataset</li>
                    <li><strong>Analyze</strong> data characteristics</li>
                    <li><strong>Train</strong> multiple classification models</li>
                    <li><strong>Compare</strong> model performances</li>
                    <li><strong>Make</strong> predictions</li>
                </ol>
            </div>
        </div>

        <div style="display: flex; align-items: center; margin: 2rem 0;">
            <div style="flex: 1; padding-right: 2rem;">
                <h4>How to use:</h4>
                <ol>
                    <li>Navigate to "📊 Upload & Train" to start with your dataset</li>
                    <li>Upload a CSV file containing your features and 'type' column</li>
                    <li>Review the visualizations and model performances</li>
                    <li>Go to "🔮 Prediction" to make predictions using the best model</li>
                </ol>
            </div>
            <div style="flex: 1;">
                <img src="https://researchworld.com/uploads/attachments/cm2d73ps00qab69tdc9pnizbd-gettyimages-1448152453.max.jpg" 
                     style="width: 70%; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            </div>
        </div>

        <div style="background: white; padding: 2rem; border-radius: 10px; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4>Supported Models:</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://images.spiceworks.com/wp-content/uploads/2022/04/11040521/46-4-e1715636469361.png" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>Logistic Regression</p>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://i0.wp.com/spotintelligence.com/wp-content/uploads/2024/05/support-vector-machine-svm.jpg?fit=1200%2C675&ssl=1" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>Support Vector Machine (SVM)</p>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://i0.wp.com/analyticsarora.com/wp-content/uploads/2022/07/knn-visually-shown-classify-unknown-point.png?resize=800%2C600&ssl=1" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>K-Nearest Neighbors (KNN)</p>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://miro.medium.com/v2/resize:fit:1400/0*Ga2SY3cwKnkCRCTZ.jpg" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>Random Forest</p>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://images.prismic.io/turing/65a540097a5e8b1120d58950_Types_of_Naive_Bayes_Classifier_08826a71f0.webp?auto=format,compress" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>Naïve Bayes</p>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <img src="https://miro.medium.com/v2/resize:fit:1400/1*OZPOQUKiaVmZOEMm_-8iYA.png" 
                         style="width: 100px; height: 100px; object-fit: contain;">
                    <p>Gradient Boosting</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif menu == "📊 Upload & Train":
    # Add header image for Upload & Train page
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" 
                 style="width: 150px; margin-bottom: 1rem;">
        </div>
    """, unsafe_allow_html=True)
    
    st.title("📊 Data Analysis & Model Training")
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        with st.spinner('Loading and processing your data...'):
            st.session_state.df = load_data(uploaded_file)
            df = st.session_state.df
            
            # Data Overview
            col1, col2 = st.columns(2)
            with col1:
                st.write("### 📋 Dataset Overview")
                st.write(f"**Rows:** {df.shape[0]}")
                st.write(f"**Columns:** {df.shape[1]}")
                st.write("**Sample Data:**")
                st.dataframe(df.head(), use_container_width=True)
            
            with col2:
                st.write("### 📊 Data Statistics")
                st.write("**Numerical Features Summary:**")
                st.dataframe(df.describe(), use_container_width=True)
            
            # Missing Values Analysis
            st.write("### 🔍 Missing Values Analysis")
            missing_values = df.isnull().sum()
            if missing_values.sum() > 0:
                st.warning(f"Found {missing_values.sum()} missing values")
                st.write(missing_values[missing_values > 0])
            else:
                st.success("No missing values found in the dataset!")

            # Data Visualization
            st.write("### 📈 Data Visualization")
            figs = create_visualizations(df)
            
            viz_col1, viz_col2 = st.columns(2)
            with viz_col1:
                st.write("#### Correlation Heatmap")
                st.pyplot(figs['correlation'])
            
            with viz_col2:
                st.write("#### Class Distribution")
                st.pyplot(figs['distribution'])

            # Model Training
            st.write("### 🤖 Model Training")
            if st.button("Train Models"):
                with st.spinner('Training models... Please wait...'):
                    # Data Preprocessing
                    df = df.dropna(axis=1, thresh=0.9 * len(df))
                    df.fillna(df.median(numeric_only=True), inplace=True)

                    st.session_state.label_encoder = LabelEncoder()
                    df["type"] = st.session_state.label_encoder.fit_transform(df["type"])
                    
                    X = df.drop(columns=["type"])
                    y = df["type"]
                    st.session_state.scaler = StandardScaler()
                    X_scaled = st.session_state.scaler.fit_transform(X)
                    
                    X_train, X_test, y_train, y_test = train_test_split(
                        X_scaled, y, test_size=0.2, random_state=42, stratify=y
                    )

                    models = {
                        "Logistic Regression": LogisticRegression(max_iter=1000),
                        "Naïve Bayes": GaussianNB(),
                        "SVM": SVC(probability=True),
                        "KNN": KNeighborsClassifier(),
                        "Random Forest": RandomForestClassifier(),
                        "Gradient Boosting": GradientBoostingClassifier()
                    }

                    results = {}
                    best_model = None
                    best_accuracy = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, (model_name, model) in enumerate(models.items()):
                        status_text.text(f"Training {model_name}...")
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        accuracy = accuracy_score(y_test, y_pred)
                        
                        results[model_name] = {
                            "Accuracy": accuracy,
                            "Precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
                            "Recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
                            "F1 Score": f1_score(y_test, y_pred, average='weighted', zero_division=0)
                        }
                        
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_model = model
                        
                        progress_bar.progress((idx + 1) / len(models))
                    
                    status_text.text("Training completed!")
                    time.sleep(1)
                    status_text.empty()
                    progress_bar.empty()

                    # Display Results
                    st.write("### 📊 Model Performance Comparison")
                    results_df = pd.DataFrame(results).T
                    
                    # Style the dataframe
                    styled_results = results_df.style.format("{:.4f}")\
                        .background_gradient(cmap='YlOrRd')\
                        .highlight_max(axis=0, color='lightgreen')
                    
                    st.dataframe(styled_results, use_container_width=True)
                    
                    # Save best model
                    if best_model is not None:
                        st.session_state.model_info = {
                            'model': best_model,
                            'scaler': st.session_state.scaler,
                            'label_encoder': st.session_state.label_encoder,
                            'feature_names': list(X.columns)
                        }
                        st.session_state.feature_names = list(X.columns)
                        st.success(f"Best model saved successfully! (Best accuracy: {best_accuracy:.4f})")

elif menu == "🔮 Prediction":
    # Add header image for Prediction page
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" 
                 style="width: 150px; margin-bottom: 1rem;">
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🔮 Make Predictions")
    
    if st.session_state.model_info is None:
        st.error("⚠️ No trained model found. Please upload a dataset and train the model first!")
        st.info("👈 Go to the 'Upload & Train' section to train a model.")
    else:
        st.info("💡 Enter the feature values for prediction below:")
        
        # Create a more organized input interface
        col1, col2 = st.columns(2)
        input_data = {}
        
        for idx, feature in enumerate(st.session_state.feature_names):
            if idx % 2 == 0:
                with col1:
                    input_data[feature] = st.number_input(
                        f"📊 {feature}",
                        value=0.0,
                        help=f"Enter value for {feature}"
                    )
            else:
                with col2:
                    input_data[feature] = st.number_input(
                        f"📊 {feature}",
                        value=0.0,
                        help=f"Enter value for {feature}"
                    )
        
        if st.button("🔮 Predict", key="predict_button"):
            with st.spinner("Making prediction..."):
                input_array = np.array(list(input_data.values())).reshape(1, -1)
                input_scaled = st.session_state.scaler.transform(input_array)
                prediction = st.session_state.model_info['model'].predict(input_scaled)
                predicted_label = st.session_state.label_encoder.inverse_transform(prediction)[0]
                
                # Get prediction probabilities
                try:
                    probabilities = st.session_state.model_info['model'].predict_proba(input_scaled)[0]
                    prob_df = pd.DataFrame({
                        'Class': st.session_state.label_encoder.inverse_transform(range(len(probabilities))),
                        'Probability': probabilities
                    })
                    
                    st.success(f"🎯 Predicted Class: **{predicted_label}**")
                    
                    # Display probabilities as a bar chart
                    st.write("### Prediction Probabilities")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sns.barplot(data=prob_df, x='Class', y='Probability')
                    plt.title("Prediction Probabilities by Class")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    
                except:
                    st.success(f"🎯 Predicted Class: **{predicted_label}**")
                    st.info("Note: Probability distribution not available for this model type.")

elif menu == "📚 Attack Types":
    st.title("📚 Attack Types & Indicators")
    
    # Define attack type data
    attack_types = [
        {
            "Attack Type": "🔥 DoS (Denial of Service)",
            "System Metrics Affected": "Processor % Processor Time, Network Bytes Sent/sec, Memory Pool Paged Bytes",
            "Expected Behavior": "High CPU load, high memory usage, spike in outbound network traffic"
        },
        {
            "Attack Type": "🌊 DDoS (Distributed DoS)",
            "System Metrics Affected": "Network Packets/sec, Output Queue Length, TCP Connections, Memory Committed Bytes",
            "Expected Behavior": "Massive spike in incoming network traffic, connection queue overflow, memory exhaustion"
        },
        {
            "Attack Type": "💉 SQL/Code Injection",
            "System Metrics Affected": "Process Handle Count, Memory Pages/sec, Process Page File Bytes, Virtual Bytes",
            "Expected Behavior": "Subtle increases in memory/CPU for exploited processes, abnormal IO activity"
        }
    ]
    
    # Convert to DataFrame
    df_attacks = pd.DataFrame(attack_types)
    
    # Add custom CSS for better styling
    st.markdown("""
        <style>
        .attack-table {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .attack-header {
            color: var(--primary);
            font-weight: bold;
            padding: 10px;
            border-bottom: 2px solid var(--primary-light);
        }
        .attack-row {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .attack-row:hover {
            background-color: #f8f9fa;
        }
        .metric-highlight {
            color: var(--danger);
            font-weight: 500;
        }
        .behavior-highlight {
            color: var(--warning);
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display the table with custom styling
    st.markdown("### 📊 Attack Types Overview")
    
    # Create a container for the table
    with st.container():
        # Display each attack type in a card-like format
        for attack in attack_types:
            with st.expander(attack["Attack Type"], expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**System Metrics Affected:**")
                    st.markdown(f'<div class="metric-highlight">{attack["System Metrics Affected"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown("**Expected Behavior:**")
                    st.markdown(f'<div class="behavior-highlight">{attack["Expected Behavior"]}</div>', unsafe_allow_html=True)
                st.markdown("---")
    
    # Add search functionality
    st.markdown("### 🔍 Search Attack Types")
    search_term = st.text_input("Search by attack type, metric, or behavior", "")
    
    if search_term:
        filtered_df = df_attacks[
            df_attacks['Attack Type'].str.contains(search_term, case=False) |
            df_attacks['System Metrics Affected'].str.contains(search_term, case=False) |
            df_attacks['Expected Behavior'].str.contains(search_term, case=False)
        ]
        if not filtered_df.empty:
            st.dataframe(filtered_df, hide_index=True, use_container_width=True)
        else:
            st.info("No matching attacks found. Try a different search term.")
    
    # Add a download button for the attack types data
    csv = df_attacks.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Attack Types Data",
        data=csv,
        file_name="attack_types.csv",
        mime="text/csv",
        help="Download the complete attack types information as a CSV file"
    )