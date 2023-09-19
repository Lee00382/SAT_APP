import streamlit as st
import openai
import pandas as pd
import io
import xlsxwriter

api_key = "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"

openai.api_key = api_key

st.title("SAT Question Explanation Generator")
st.write("Upload an Excel file with SAT questions, and this tool will generate explanations for each question.")

def generate_explanation(question, answer_a, answer_b, answer_c, answer_d, correct_answer_choice):
    user_prompt = f"Explain the following SAT question: {question}\n"
    user_prompt += f"a) {answer_a}\n"
    user_prompt += f"b) {answer_b}\n"
    user_prompt += f"c) {answer_c}\n"
    user_prompt += f"d) {answer_d}\n"
    user_prompt += f"The correct answer is choice {correct_answer_choice}."

    system_prompt = "You are a helpful SAT assistant for making clear and succinct explanations given a question and correct answer choice. You should give why the correct answer is correct and why other choices are incorrect. If the question is short answer question, just give how you got to the correct answer. Please be concise in your response."
    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
    )

    explanation = response['choices'][0]['message']['content']
    return explanation

def process_excel_file(file):
    try:
        df = pd.read_excel(file)
        explanations = []
        for _, row in df.iterrows():
            explanation_text = generate_explanation(
                row['Question'],
                row['Answer_A'],
                row['Answer_B'],
                row['Answer_C'],
                row['Answer_D'],
                row['Correct_Answer_Choice']
            )
            explanations.append(explanation_text)
        df['Explanation'] = explanations
        return df
    except Exception as e:
        return str(e)

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        st.write("Generating explanations...")
        result_df = process_excel_file(uploaded_file)
        st.subheader("Explanations for SAT Questions:")
        st.dataframe(result_df)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, sheet_name='Explanations', index=False)
            writer.save()
        output.seek(0)
        st.download_button(
            label="Download Explanations and Questions (Excel)",
            data=output,
            file_name="sat_explanations_and_questions.xlsx",
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
