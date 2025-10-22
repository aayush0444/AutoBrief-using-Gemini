from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('API_KEY')

class SmartAnalyzer:
    def __init__(self, df):
        self.df = df
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.numeric_cols = df.select_dtypes(include='number').columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.date_cols = self._detect_date_columns()
    
    def _detect_date_columns(self):
        date_cols = []
        for col in self.df.columns:
            try:
                pd.to_datetime(self.df[col], errors='raise')
                date_cols.append(col)
            except:
                pass
        return date_cols
    
    def process_query(self, user_query, context):
        # Step 1: Understand what user wants
        intent = self._understand_intent(user_query, context)
        
        # Step 2: Generate response and chart based on intent
        return self._generate_response(user_query, intent)
    
    def _understand_intent(self, query, context):
        context_text = "\n".join([f"User: {c['user']}\nAssistant: {c['assistant']}" for c in context[-2:]])
        
        dataset_info = f"""
Dataset Info:
- Total rows: {len(self.df)}
- Numeric columns: {', '.join(self.numeric_cols[:10])}
- Categorical columns: {', '.join(self.categorical_cols[:10])}
- Date columns: {', '.join(self.date_cols[:5])}
"""
        
        system_prompt = """You are a smart query analyzer. Analyze the user's query and return a JSON with:
{
  "intent": "summary/statistics/comparison/trend/correlation/distribution/specific_question",
  "chart_type": "none/line/bar/scatter/pie/histogram/box",
  "columns_needed": ["col1", "col2"],
  "aggregation": "mean/sum/count/none",
  "needs_calculation": true/false
}

Examples:
- "what's in this data" -> intent: summary, chart_type: none
- "show sales trends" -> intent: trend, chart_type: line, columns_needed: [date_col, sales_col]
- "compare prices by category" -> intent: comparison, chart_type: bar
- "average salary" -> intent: statistics, needs_calculation: true
- "plot age vs income" -> intent: correlation, chart_type: scatter, columns_needed: [age, income]

Be smart and infer column names from user query even if not exact."""

        full_prompt = f"{dataset_info}\n\nRecent context:\n{context_text}\n\nUser query: {query}"
        
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=300,
            temperature=0.3
        )
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=full_prompt,
            config=config
        )
        
        try:
            intent_json = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return intent_json
        except:
            return {"intent": "summary", "chart_type": "none", "columns_needed": [], "aggregation": "none"}
    
    def _generate_response(self, query, intent):
        chart = None
        
        # Generate chart based on intent
        if intent['chart_type'] != 'none':
            chart = self._create_chart(intent)
        
        # Generate text response
        response_text = self._create_text_response(query, intent, chart is not None)
        
        return {
            'response': response_text,
            'chart': chart
        }
    
    def _create_chart(self, intent):
        chart_type = intent['chart_type']
        cols = intent['columns_needed']
        
        try:
            if chart_type == 'line':
                x_col, y_col = self._smart_column_match(cols, prefer_date=True)
                if x_col and y_col:
                    df_sorted = self.df.sort_values(x_col)
                    return px.line(df_sorted, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            
            elif chart_type == 'bar':
                if len(cols) >= 2:
                    x_col, y_col = cols[0], cols[1]
                elif len(cols) == 1:
                    x_col = cols[0]
                    y_col = self.numeric_cols[0] if self.numeric_cols else None
                else:
                    x_col = self.categorical_cols[0] if self.categorical_cols else None
                    y_col = self.numeric_cols[0] if self.numeric_cols else None
                
                if x_col and y_col:
                    agg = intent.get('aggregation', 'mean')
                    if agg == 'mean':
                        df_agg = self.df.groupby(x_col)[y_col].mean().reset_index()
                    elif agg == 'sum':
                        df_agg = self.df.groupby(x_col)[y_col].sum().reset_index()
                    else:
                        df_agg = self.df.groupby(x_col)[y_col].count().reset_index()
                    
                    return px.bar(df_agg, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            
            elif chart_type == 'scatter':
                if len(cols) >= 2:
                    x_col, y_col = cols[0], cols[1]
                    return px.scatter(self.df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
            
            elif chart_type == 'pie':
                col = cols[0] if cols else self.categorical_cols[0]
                counts = self.df[col].value_counts().head(10)
                return px.pie(values=counts.values, names=counts.index, title=f"Distribution of {col}")
            
            elif chart_type == 'histogram':
                col = cols[0] if cols else self.numeric_cols[0]
                return px.histogram(self.df, x=col, title=f"Distribution of {col}")
            
            elif chart_type == 'box':
                col = cols[0] if cols else self.numeric_cols[0]
                return px.box(self.df, y=col, title=f"Box Plot of {col}")
        
        except Exception as e:
            print(f"Chart creation error: {e}")
            return None
        
        return None
    
    def _smart_column_match(self, requested_cols, prefer_date=False):
        """Match user's requested columns to actual dataframe columns"""
        matched = []
        
        for req_col in requested_cols[:2]:
            req_lower = req_col.lower()
            
            # Try exact match first
            exact_match = [c for c in self.df.columns if c.lower() == req_lower]
            if exact_match:
                matched.append(exact_match[0])
                continue
            
            # Try partial match
            partial_match = [c for c in self.df.columns if req_lower in c.lower() or c.lower() in req_lower]
            if partial_match:
                matched.append(partial_match[0])
                continue
            
            # Fall back to column type
            if prefer_date and self.date_cols:
                matched.append(self.date_cols[0])
            elif self.numeric_cols:
                matched.append(self.numeric_cols[0])
        
        return matched if len(matched) == 2 else (None, None)
    
    def _create_text_response(self, query, intent, has_chart):
        sample_data = self.df.sample(min(30, len(self.df))).to_csv(index=False)
        
        # Calculate basic stats
        stats = {}
        for col in self.numeric_cols[:5]:
            stats[col] = {
                'mean': round(self.df[col].mean(), 2),
                'min': round(self.df[col].min(), 2),
                'max': round(self.df[col].max(), 2),
                'missing': int(self.df[col].isnull().sum())
            }
        
        cat_stats = {}
        for col in self.categorical_cols[:5]:
            cat_stats[col] = {
                'unique': int(self.df[col].nunique()),
                'top': str(self.df[col].mode()[0]) if not self.df[col].mode().empty else 'N/A',
                'missing': int(self.df[col].isnull().sum())
            }
        
        system_prompt = f"""You are a friendly data analyst. Answer the user's question naturally and conversationally.

Dataset Overview:
- Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns
- Numeric stats: {stats}
- Categorical stats: {cat_stats}

Rules:
1. Be conversational and natural - vary your responses
2. Don't repeat the same format every time
3. {"A chart has been generated, so keep your text brief and explain what the chart shows" if has_chart else "No chart generated, provide a detailed answer"}
4. If user asks for specific calculations, do them using the stats provided
5. Be helpful and suggest related things they might want to explore
6. Keep it under 8 lines unless specifically asked for detail
7. Use emojis sparingly (1-2 max)

Sample data for reference:
{sample_data[:1000]}"""
        
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=400,
            temperature=0.7
        )
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=query,
            config=config
        )
        
        return response.text