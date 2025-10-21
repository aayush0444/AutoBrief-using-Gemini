from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('API_KEY')

def summarize_data(summarizer_prompt):
    system_prompt = '''You are an intelligent *AI Analyst*.
                    your Task- 
                    you will get data set in a tablular form,your task to summarize the Data for user in some line and provide inside of the data.
                    For **example**- if the data contains columns like-name,age,sex,occupation,salary, and etx.
                    you would provide. That this data is about a general company data or a country or state data telling about the working society this data contains some missing values and like this.

                    u have to end with a good flow and be user friendly be concise 
                    *** Do Not provide large context of all the thing and complete in about 5 to 15 lines***
               
                    '''

    getclient = genai.Client(api_key=GEMINI_API_KEY)
    config_params = types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=500
    )
    summ_response = getclient.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=summarizer_prompt,
        config=config_params
    )
    return summ_response

def eda_(prompt_user, eda_answers):
    eda_prompt = f"""
        You are an intelligent Data Analyst specialized in **Exploratory Data Analysis (EDA)**.
        
        Your primary input is a pre-computed, structured analysis dictionary (provided below as 'EDA ANSWERS') which contains all necessary numerical summaries (min, max, mean, missing counts) and categorical summaries (unique counts, mode, missing counts).
        
        Your task is to interpret this structured analysis and present the results in a professional, easy-to-read **markdown format**.

        ### Strict Output Requirements:
        
        1.  **Structure:** The response MUST be divided into three markdown sections: 
            a.  ## 📊 Categorical Data Summary
            b.  ## 🔢 Numerical Data Summary
            c.  ## 🎯 Insight and Next Steps

        2.  **Categorical Table:** For the categorical features, generate a markdown table with the following columns:
            | Feature | Unique Values | Missing Count | Most Frequent Category | Key Insight |
            (Fill the table using information from the 'EDA ANSWERS' data.)

        3.  **Numerical Table:** For the numerical features, generate a markdown table with the following columns:
            | Feature | Min Value | Max Value | Mean (or Std Dev) | Missing Count | Key Insight |
            (Fill the table using information from the 'EDA ANSWERS' data.)

        4.  **Content:** Do NOT perform mathematical computation yourself. Translate the provided dictionary values into the required tables and insights.
        
        5.  **Insight Section:** The final section (🎯) must include:
            * A **Data Quality** assessment (commenting on missing values or outliers).
            * A **Key Opportunity** (suggesting what patterns or relationships are most interesting).
            * An **Actionable Next Step** (recommending the next analysis or data cleaning step).
            
        6.  **Style:** Write as if presenting to a non-technical manager. Be concise and focus on the most impactful data points.

        Here's the dataset analysis result you have to interpret:
        
        {eda_answers}
    """

    getclient = genai.Client(api_key=GEMINI_API_KEY)
    config_params = types.GenerateContentConfig(
        system_instruction=eda_prompt,
        max_output_tokens=600
    )
    eda_response = getclient.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt_user,
        config=config_params,
    )
    return eda_response

def eda_and_summarize(prompt_user, eda_answers):
    combined_prompt = f"""
        You are an expert *AI Data Analyst* and your job is to **analyze and summarize datasets comprehensively**.

        ### TASK OVERVIEW:
        You are given two inputs:
        1. A **user query** asking for both summary and EDA.
        2. A structured **EDA result dictionary** (called 'EDA ANSWERS') containing:
           - Numerical summaries (mean, min, max, missing count, etc.)
           - Categorical summaries (unique values, top category, missing count, etc.)

        ### OBJECTIVE:
        Create a single professional, clear, and human-readable markdown report that includes both:
        - 📘 **Dataset Summary** — Explain what the dataset represents, its context, and high-level insights.
        - 📊 **Exploratory Data Analysis (EDA)** — Present numerical and categorical feature summaries using the provided data.

        ### OUTPUT STRUCTURE (STRICT):
        1. ## 🧾 Dataset Summary
           * 4—8 concise sentences describing what this dataset seems to be about.
           * Mention notable aspects like data diversity, completeness, and size.
           * Avoid listing every column — group them logically (e.g., demographics, sales info).

        2. ## 📊 Categorical Feature Analysis
           | Feature | Unique Values | Missing Count | Most Frequent Category | Key Insight |
           (Use the information from the EDA ANSWERS dictionary. Do **not** calculate anything new.)

        3. ## 🔢 Numerical Feature Analysis
           | Feature | Min Value | Max Value | Mean / Std Dev | Missing Count | Key Insight |
           (Use the values directly from the provided EDA ANSWERS.)

        4. ## 🎯 Overall Insights & Next Steps
           * Comment on data quality and completeness.
           * Highlight any interesting patterns or anomalies.
           * Recommend actionable next steps (e.g., correlation analysis, cleaning, or visualization).

        ### STYLE RULES:
        - Write like you're presenting to a business audience (clear and professional).
        - Don't perform math or statistics yourself; use the provided values.
        - Keep the response concise — ideally 10—20 lines total.

        Below is the structured EDA result for your reference:

        {eda_answers}
    """

    getclient = genai.Client(api_key=GEMINI_API_KEY)
    config_params = types.GenerateContentConfig(
        system_instruction=combined_prompt,
        max_output_tokens=800
    )
    
    combined_response = getclient.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=prompt_user,
        config=config_params,
    )
    return combined_response

def clarifier(user_query, chathistory):
    # Convert chathistory dict to readable format
    history_text = "\n".join([f"Query {qid}: {data['query']} -> Response: {data['response']}" 
                              for qid, data in chathistory.items()]) if chathistory else "No previous history"
    
    full_prompt = f"""
    User Query: {user_query}
    
    Chat History:
    {history_text}
    
    Based on the user query and chat history, classify the intent into ONE of these categories:
    - "only summarize" - if user wants just a summary of the data
    - "only eda" - if user wants exploratory data analysis
    - "eda and summarize" - if user wants both summary and EDA
    
    Respond with ONLY one of these three phrases, nothing else.
    """
    
    system_prompt = '''You are an intelligent AI agent. Your task is to classify user queries into one of three categories:
    1. "only summarize" - user wants data summary
    2. "only eda" - user wants exploratory data analysis  
    3. "eda and summarize" - user wants both
    
    Respond with ONLY the category phrase, nothing else.'''
    
    getclient = genai.Client(api_key=GEMINI_API_KEY)
    config_params = types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=50
    )
    clarification = getclient.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=full_prompt,
        config=config_params,
    )
    return clarification