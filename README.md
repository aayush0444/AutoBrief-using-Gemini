Dive in Data - Smart Data Analysis Chat
An intelligent data analysis tool that lets you chat with your CSV data using natural language. Ask questions, get insights, and generate visualizations automatically.

Features
Natural Language Queries
Ask questions in plain English and get intelligent responses. No need to know SQL or complex syntax.

Automatic Visualization
The system automatically generates appropriate charts based on your query - line charts for trends, bar charts for comparisons, scatter plots for correlations, and more.

Conversational Memory
Remembers the context of your conversation, so you can build on previous questions naturally.

Smart Column Detection
Finds the right columns even if you don't use exact names. Ask about "sales" and it'll match "total_sales" or "sales_amount".

Varied Responses
Every answer is unique and conversational. The system adapts its responses to avoid repetitive patterns.

Quick Start
Prerequisites
Python 3.8 or higher
Google Gemini API key
Installation
Step 1: Clone the repository

bash
git clone https://github.com/yourusername/dive-in-data.git
cd dive-in-data
Step 2: Install dependencies

bash
pip install -r requirements.txt
Step 3: Set up your API key

Create a .env file in the root directory:

API_KEY=your_gemini_api_key_here
You can get your API key from Google AI Studio

Step 4: Run the application

bash
streamlit run streamlit_app.py
The app will open in your default browser at http://localhost:8501

Usage
Upload Your Data
Use the sidebar to upload any CSV file. The system will automatically analyze its structure and prepare it for queries.

Ask Questions
Here are some example queries you can try:

General Understanding

"What's in this dataset?"
"Give me a summary of the data"
"Show me the column names"
Statistical Analysis

"What's the average revenue?"
"Show me missing values"
"What's the range of prices?"
Comparisons

"Compare sales by region"
"Which category has the highest revenue?"
"Show top 5 products by sales"
Trends and Patterns

"Show sales trends over time"
"Plot monthly revenue"
"Display customer growth"
Correlations

"Plot age vs income"
"Is there a relationship between price and quantity?"
"Show correlation between variables"
View Results
The system provides both textual insights and visual charts. Charts are interactive - you can zoom, pan, and hover for details.

Project Structure
dive-in-data/
│
├── streamlit_app.py          # Main application interface
├── utils/
│   ├── smart_analyzer.py     # Core intelligence and query processing
│   ├── analyzer.py            # Statistical analysis functions
│   └── summarizer.py          # Data summarization utilities
│
├── requirements.txt           # Python dependencies
├── .env                       # API key configuration
└── README.md                  # This file
How It Works
Step 1: Query Understanding
When you ask a question, the system analyzes your intent and determines what kind of analysis or visualization you need.

Step 2: Column Matching
It intelligently matches your query to actual column names in your dataset, even with approximate or partial matches.

Step 3: Analysis and Visualization
Based on the intent, it performs the appropriate analysis and generates relevant charts automatically.

Step 4: Response Generation
The system creates a natural, conversational response that explains the findings in clear language.

Technical Details
Built With

Streamlit - Web interface
Pandas - Data manipulation
Plotly - Interactive visualizations
Google Gemini - Natural language understanding
Python-dotenv - Environment configuration
Chart Types Supported

Line charts for time series and trends
Bar charts for categorical comparisons
Scatter plots for correlations
Pie charts for distributions
Histograms for frequency distributions
Box plots for outlier detection
Configuration
You can modify the system behavior by adjusting parameters in smart_analyzer.py:

temperature - Controls response creativity (0.3-1.0)
max_output_tokens - Maximum response length
Context window size - Number of previous conversations to remember
Troubleshooting
Issue: "API key not found"
Make sure you've created a .env file with your API key in the root directory.

Issue: Charts not displaying
Check that your dataset has the appropriate column types (numeric columns for numerical charts, etc.)

Issue: Column not found
Try using more specific column names or check the actual column names in the sidebar.

Contributing
Contributions are welcome! Feel free to:

Report bugs
Suggest new features
Submit pull requests
Improve documentation
Please ensure your code follows the existing style and includes appropriate comments.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Google Gemini for natural language processing
Streamlit for the web framework
Plotly for interactive visualizations
Contact
For questions or feedback, please open an issue on GitHub.

Note: This tool requires an active internet connection and a valid Google Gemini API key to function.

