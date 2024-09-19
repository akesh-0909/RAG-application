from langchain_core.messages import AIMessage, HumanMessage
from helper import *
from dotenv import load_dotenv
import json
import streamlit as st
print('page realoed')
load_dotenv()
Gemini_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={os.environ['GEMINI']}"

st.set_page_config(page_title="Chat wit Websites")
col1,col2 = st.columns(2)

st.title('😀 Paste and Chat',)

website_url = st.text_input('Enter the URL here')
upload_pdf = st.file_uploader('Upload your PDF here',type='pdf')

if (website_url and upload_pdf) or (not website_url and not upload_pdf):
    st.warning("Please enter either a website URL or upload a PDF, not both or neither.")
else:
    if website_url:
        print("website Url ",website_url)
        document = load_documents(website_url, _type='url')
    elif upload_pdf:
        print('document',upload_pdf)
        with open(f"./temp_{upload_pdf.name}", "wb") as f:
            f.write(upload_pdf.getbuffer())

        pdf_path = f"./temp_{upload_pdf.name}"
        print('Uploaded PDF: ', upload_pdf.name)
        
        document = load_documents(pdf_path, _type='pdf')

    else:
        print('got nothing')
    chunks = make_chunks(document)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            message_template('Hey, I am a bot, How can I help you?', _type='ai')
        ]

    if "vector_store" not in st.session_state:
        st.session_state['vector_store'] = vector_store_chunks_retriver(chunks)

    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "" :
        st.session_state.chat_history.append(message_template(user_query, _type='human'))
        
        retrived_documents = st.session_state['vector_store'].get_relevant_documents(user_query)
        context_map = ' '.join([retrived_documents[i].page_content for i in range(len(retrived_documents))])

        print('\ncontext_map',context_map)
        prompt = get_prompt(user_query, context_map)
        Gemini_input_json = {"contents": [{"parts": [{"text": f"{prompt}"}]}]}        
        response = llm(Gemini_input_json)
        response = response['candidates'][0]['content']['parts'][0]['text']
        
        st.session_state.chat_history.append(message_template(response, _type='ai'))
        
    for message in st.session_state.chat_history:
        print('\nmessage',message)
        if message[0] == 'ai':
            with st.chat_message("AI"):
                st.write(message[2])
        elif message[0] == 'human':
            with st.chat_message("Human"):
                st.write(message[2])

