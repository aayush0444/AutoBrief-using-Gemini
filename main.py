from utils.smart_analyzer import summarize_data, eda_, clarifier, eda_and_summarize
from utils.data_loader import data_load
from utils.analyzer import analyze_dataset
import pandas as pd

def main():
    # Load dataset
    df = pd.read_csv(r'D:\EDRIVE\My projects\auto_summarizer\data\nearest-earth-objects(1910-2024).csv')
    
    chathistory = {}
    query_id = 0

    while True:
        print('Enter your query (or "exit" to quit):')
        print('=' * 70)
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            print('Exiting...')
            break

        # Prepare data and analysis
        data = data_load(df)
        eda_answers = analyze_dataset(df)
        
        # Clarify user intent
        res = clarifier(user_input.lower(), chathistory)
        intent = res.text.lower().strip()
        
        summarizer_prompt = f'{user_input}+{data}'
        print('=' * 70)
        
        # Route based on intent
        if 'eda and summarize' in intent:
            response = eda_and_summarize(summarizer_prompt, eda_answers)
            print(response.text)
            
        elif 'only eda' in intent:
            response = eda_(summarizer_prompt, eda_answers)
            print(response.text)
            
        elif 'only summarize' in intent:
            response = summarize_data(summarizer_prompt)
            print(response.text)
            
        else:
            # Default to eda and summarize
            response = eda_and_summarize(summarizer_prompt, eda_answers)
            print(response.text)
        
        # Store in chat history
        query_id += 1
        chathistory[query_id] = {
            'query': user_input,
            'response': response.text[:200]  # Store first 200 chars
        }
        
        print('\n' + '=' * 70 + '\n')

if __name__ == '__main__':
    try:
        print('Running main file...')
        main()
    except Exception as e:
        print(f'An error occurred during execution: {e}')
        print('Execution terminated.')