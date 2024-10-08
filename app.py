import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompt import Prompt
import chainlit as cl 
import mysql.connector
import pandas as pd
import plotly.graph_objects as go

load_dotenv() 
client=genai.configure(api_key=os.getenv('gemini_api_key'))
model = genai.GenerativeModel('gemini-pro',generation_config={'temperature':0.4})

prompt1 = [
        {'role': 'user', 
            'parts': [f'{Prompt}']
            },
        {'role': 'model', 
            'parts': ["Understood"]
            }
]
chat = model.start_chat(history=prompt1 )    


def genai2(input_message):        
    '''
    "generationConfig": {
                "temperature": 0.4,
                "topP":0.5,
                "topK": 3,
                "candidateCount": 1,
                "maxOutputTokens": 2600,
            }
    '''
    response = chat.send_message(input_message)
    return response.text

    
def query_database(query):
        host=str(os.getenv('host'))
        conn = mysql.connector.connect(
                host=host,
                user=os.getenv('user'),
                password=os.getenv('password'),
                database=os.getenv('database'),
                port=3306
        )
                
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description] if cur.description else []
        conn.close()
        return rows, columns



@cl.on_message
async def main(message: cl.Message):
    await cl.Avatar(
            name="Smartola",
            url="https://pics.craiyon.com/2023-11-16/LFXsTXnkR9mZ9vK5OS11bQ.webp",
        ).send()
    res=genai2(message.content)
    if "```sql" in res:
        query = (((res.split("```"))[1]).removeprefix("sql\n")).removesuffix("\n")
        rows,columns=query_database(query)
        df=pd.DataFrame(rows,columns=columns)   
        if len(rows)==1 and len(columns)==1:
            await cl.Message(content=f"{res}\n\n\n **The answer is : {rows[0][0]}**",author="Smartola").send()
        else:
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),line_color='black'),
                cells=dict(values=[df[i] for i in df.columns],fill_color='white',line_color='black')
                )],layout=dict(autosize=True))
            fig.update_layout(paper_bgcolor='#f5f5f5')

            elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

            await cl.Message(content=f"{res}\n\n**Count : {len(rows)}**", elements=elements,author="Smartola").send()

            csv_content = df.to_csv(sep=',', index=False).encode('utf-8')
            elements = [
            cl.File(
            name="data.csv",
            content=csv_content,
            display="inline",
            ),
            ]

            await cl.Message(content="**Download the data as CSV file**", elements=elements,author="Smartola").send()


    else:
        await cl.Message(
            content=res
            ,author="Smartola"
        ).send()
