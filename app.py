from helper import *

import json
import requests

document = load_documents(input('Enter the url : '))
chunks = make_chunks(document)
VectorStoreRetriver = vector_store_chunks_retriver(chunks)





while True:
    question = input('\n"exit" or Enter your Query : ')
    if question == 'exit':
        print('Exiting')
        break

    print('\n',20*'#',"Retrieval Started",'#'*20)
    retrived_documents = VectorStoreRetriver.get_relevant_documents(question)
    print('\n',"Retrieval Successfully Done.",)

    print('\n',20*'#',"Augmentation Started",'#'*20)
    context_map = ' '.join([retrived_documents[i].page_content for i in range(len(retrived_documents))])
    prompt = get_prompt(question,context_map)
    print('\n',"Augmentation Successfully Done.",)


    print('\n',20*'#',"Generation Started",'#'*20)
    Gemini_input_json = {"contents":[{"parts":[{"text":f"{prompt}"}]}]}

    response = llm(
         Gemini_input_json
    )
    print('\n',"Generation Successfully Done.",)

    print("\n\nQuestion: ",question)
    print('\n Answer: ',response['candidates'][0]['content']['parts'][0]['text'])



