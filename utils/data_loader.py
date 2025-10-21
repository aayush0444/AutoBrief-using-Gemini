import pandas as pd

df = pd.read_csv(r'D:\EDRIVE\auto_summarizer\data\nearest-earth-objects(1910-2024).csv')
def data_load():
    df = pd.read_csv(r'D:\EDRIVE\auto_summarizer\data\nearest-earth-objects(1910-2024).csv')
    sample_data=df.sample(50)

    df_string=sample_data.to_csv(index=False)
    return df_string
