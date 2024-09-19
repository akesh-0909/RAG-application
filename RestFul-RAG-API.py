from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from helper import *  # Assuming this contains your document loaders and vector store functions
import uvicorn
from fastapi.middleware.wsgi import WSGIMiddleware

# Initialize Flask and Flask-Restful
flask_app = Flask(__name__)
fastapi_app = Api(flask_app)

# Create a global retriever holder
class RetrieverHolder:
    def __init__(self):
        self.retriever = None

retriever_holder = RetrieverHolder()
global retriver_holder


class CreateVectorStore(Resource):
    def post(self):
        """
        Load document from a URL and create vector store (retriever)
        """
        try:
            data = request.json
            url = data['input']['url']
            print('POST request received with URL:', url)
            
            # Load and process document
            document = load_documents(url)
            chunks = make_chunks(document)
            
            # Create vector store retriever from chunks
            retriever_holder.retriever = vector_store_chunks_retriver(chunks)
            print('Retriever created:', retriever_holder.retriever)
            
            return jsonify({"message": "Vector store created successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def get(self):
        """
        Check if vector store exists
        """
        if retriever_holder.retriever is None:
            return jsonify({"error": "Vector store not created"})
        else:
            return jsonify({"message": "Hit /query endpoint to retrieve response"})

class RAG_api(Resource):
    def post(self):
        """
        RAG API to retrieve documents and generate a response
        """
        try:
            # Check if retriever exists
            if retriever_holder.retriever is None:
                return jsonify({"error": "Vector store not created. Please hit /url to create it."})

            data = request.json
            query = data['input']['query']
            print('Query received:', query)
            
            # Retrieve relevant documents using the query
            retrieved_documents = retriever_holder.retriever.get_relevant_documents(query)
            print('Retrieved documents:', retrieved_documents)
            
            # Combine retrieved documents into a context
            context_map = ' '.join([doc.page_content for doc in retrieved_documents])
            print('\ncontext_map',context_map)
            # Get prompt and query LLM for a response
            prompt = get_prompt(query, context_map)

            print('\nprompt',prompt)

            Gemini_input_json = {"contents":[{"parts":[{"text":f"{prompt}"}]}]}
            print('Gemini_input_json',Gemini_input_json)
            llm_response = llm(Gemini_input_json)
      
            
            return jsonify({"message": "Data retrieved successfully", "data": llm_response['candidates'][0]['content']['parts'][0]['text']})
        except Exception as e:
            return jsonify({"error line 76": str(e)})

if __name__ == '__main__':
    fastapi_app.add_resource(CreateVectorStore, '/url')
    fastapi_app.add_resource(RAG_api, '/query')
    flask_app.run(debug=True)
