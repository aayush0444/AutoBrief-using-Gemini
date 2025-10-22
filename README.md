Dive in Data — Smart Data Analysis Chat

Dive in Data is an intelligent chat-based data analysis tool that lets you explore CSV files through natural language.
You can upload a dataset, ask questions, and instantly receive analytical insights and visualizations — without writing a single line of code.

🔹 Features

Natural Language Queries — Ask questions in plain English and get meaningful data insights.

Automatic Visualization — Generates the most suitable charts (line, bar, scatter, pie, etc.) based on your query.

Conversational Memory — Remembers context across multiple questions for smoother, natural conversations.

Smart Column Detection — Detects related columns even if names don’t match exactly (e.g., “sales” → “total_sales”).

Interactive Results — Displays charts and summaries you can explore directly in the browser.

🔹 Quick Start
1. Prerequisites

Python 3.8 or higher

Google Gemini API key

2. Installation
git clone (https://github.com/aayush0444/AutoBrief-using-Gemini.git)
cd dive-in-data
pip install -r requirements.txt

3. Set up your API key

Create a .env file in the project root and add your key:

API_KEY=your_gemini_api_key_here


You can get your API key from Google AI Studio
.

4. Run the App
streamlit run streamlit_app.py


The app will soon be deployed to streamlit

🔹 How to Use

Upload Your Dataset
Use the sidebar to upload any CSV file.

Ask Questions
Type your queries like:

“Summarize this dataset.”

“Show missing values.”

“Plot sales by region.”

“Compare revenue across categories.”

View Results
Get both text-based explanations and interactive charts generated automatically.

🔹 Project Structure
dive-in-data/
│
├── streamlit_app.py          # Main web interface
├── utils/
│   ├── smart_analyzer.py     # Query understanding and visualization logic
│   ├── analyzer.py           # Core statistical functions
│   └── data_loader.py         # Data summarization utilities
│
├── requirements.txt          # Dependencies
├── .env                      # API configuration
└── README.md                 # Documentation

🔹 Technologies Used

Streamlit — Web application interface

Pandas — Data analysis and manipulation

Plotly — Interactive visualizations

Google Gemini API — Natural language query processing

Python-dotenv — Secure API key handling

🔹 Common Issues

“API key not found” → Ensure .env file exists with the correct key.

Charts not showing → Verify your dataset has valid numeric or categorical columns.

Column not recognized → Try referring to the exact or closely matching column name.

🔹 Future Improvements

Better query understanding and natural reasoning

Support for multiple datasets in one session

Enhanced visualization customization

Option to export results and summaries

🔹 License

This project is licensed under the MIT License — see the LICENSE file for details.
