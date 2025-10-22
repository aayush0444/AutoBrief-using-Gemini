import pandas as pd
df = pd.read_csv(r'D:\EDRIVE\My projects\auto_summarizer\data\nearest-earth-objects(1910-2024).csv')
def numerical_analysis(df):
    numerical_summary = {}
    numeric_col = df.select_dtypes(include='number').columns.tolist()

    for col in numeric_col:
        numerical_summary[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'mode': df[col].mode(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'missing': df[col].isnull().sum()
        }
    return numerical_summary

def categorical_analysis(df):
    categorical_summary = {}
    categorical_col = df.select_dtypes(include=['object', 'category']).columns.tolist()

    for col in categorical_col:
        categorical_summary[col] = {
            'unique_val': df[col].nunique(),
            "top_value": df[col].mode()[0] if not df[col].mode().empty else None,
            "missing": df[col].isnull().sum()
        }
    return categorical_summary

def analyze_dataset(df):
    analysis = {
        'categorical_summary': categorical_analysis(df),
        'numerical_summary': numerical_analysis(df)
    }
    return analysis