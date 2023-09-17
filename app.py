import streamlit as st
import pandas as pd
import openai
import os

openai.api_key = "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"

st.title("SAT Question Answering App")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.write("Data from Excel file:")
        st.write(df)

        st.header("Ask a Question")

        user_question = st.text_input("Enter your question:")

        if user_question:
            response = openai.Completion.create(
                engine="text-davinci-002",  
                prompt=f"Data: {df.to_string()}\nQuestion: {user_question}\nAnswer:",
                max_tokens=1000
            )
            
            chatbot_answer = response.choices[0].text.strip()
            st.write(f"Answer: {chatbot_answer}")
            
            if st.button("Export to Excel"):
                df = pd.DataFrame({"Question": [user_question], "Answer": [chatbot_answer]})

            excel_file_path = "chatbot_answer.xlsx"
            df.to_excel(excel_file_path, index=False, engine="openpyxl")    

            st.success("Answers exported to Excel")


    except Exception as e:
        st.error(f"An error occurred: {e}")