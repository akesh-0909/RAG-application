# RAG Chat Application 
![image](https://github.com/user-attachments/assets/ee0ac9d4-fb19-4851-9dd7-e7645b216889)

**What is RAG?** [Beginner Friendly Article](https://dev.to/akeshlovescience/rag-architecture-explained-beginner-5hn4)

## Overview
```markdown
│
├── app.py                     # Command-line interface
├── RestFul-RAG-API.py         # API interface using Flask
├── streamlit-RAG-ChatBot.py   # User interface using Streamlit
│
├── requirements.txt           # List of project dependencies
├── README.md                  # Project documentation
│
├── .env                       # Environment variables file (not in version control)
│
├── images/
│   ├── image.png
│   ├── image-1.png
│   └── image-2.png
│

└── helper.py # components
```

Welcome to the **Retrieval-Augmented Generation (RAG) Application**! This project is designed to demonstrate the power of RAG by allowing users to generate context-aware responses from both URLs and PDF inputs. We’ve implemented three variants of the application to cater to different use cases: command-line interface, API interface, and user interface.



## Features

1. **Command-Line Interface (`app.py`)**: 
   - Easily access RAG functionality from your terminal.
   - Supports URL-based input.
   
2. **API Interface (`RestFul-RAG-API.py`)**:
   - Exposes API endpoints using Flask for integration into other applications.
   - URL-based input support for document retrieval.
   
3. **User Interface (`streamlit-RAG-ChatBot.py`)**:
   - A sleek and interactive GUI using Streamlit for ease of use.
   - Supports both URL and PDF inputs, perfect for a web-based experience.
   - Drag-and-drop functionality for PDFs for seamless input.

---

## Components Used

- **Generation**: Powered by Google’s **Gemini API**, providing rich, context-driven responses.
- **Embeddings**: Utilizes the **BAAI/bge-base-en-v1.5** model for efficient and accurate embeddings.
- **Additional Tools**:
   - **LangChain** for managing chains and retrieval logic.
   - **ChromaDB** for efficient vector storage and search.
   - **HuggingFace** for leveraging pre-trained models.
   - **Flask, RestAPI** to serve API endpoints.
   - **Streamlit** for the web-based user interface.

---

## How to Use

### 1. Command-Line Interface (CLI)
Run RAG via the terminal:

```bash
python app.py --url <your-url>
```

Example:
![alt text](images/image.png)
```bash
python app.py --url https://example.com
```

### 2. API Interface (RestFulFlask)
Start the Flask API:

```bash
python RestFul-RAG-API.py
```

Access the API endpoint:
- **POST**: `/url` with URL as payload to create Vector Store Resource.
```json
{
"input": {
"url": "https://medium.com/artical-url"
}
}
```

- **POST**: `/query` with query as payload to get response from the model.
```json
{
    "input": {
        "query": "What are adapters?"
    }
}
```




### 3. User Interface (Streamlit)
Launch the Streamlit app:

```bash
streamlit run streamlit-RAG-ChatBot.py
```

You can either:
- Enter a **URL** for text retrieval, or
- Upload a **PDF** to retrieve relevant content and generate responses.
Example:
 <center> <img src="https://github.com/user-attachments/assets/c0c418b3-132f-4c85-94e2-09b66d5adaa0"> 

---

---

## PDF Support (Streamlit Variant Only)
While the command-line and API interfaces are designed for URL inputs, the Streamlit GUI brings extra functionality by allowing **PDF input**. Simply drag and drop your PDF into the interface to retrieve content, ask questions, and receive generated responses. This makes it ideal for document-based workflows.


## Setup Instructions

### Prerequisites

- Python 3.9+
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables
- Create `.env` file and add your Google Gemini API key and HuggingFace credentials in the `.env` file.

```bash
GEMINI_API_KEY=your-api-key
HUGGINGFACE_API_KEY=your-api-key
```



## Contributing

Feel free to fork this repository and contribute! Whether it's improving the UI, optimizing retrieval logic, or integrating new models, contributions are welcome.


## License

This project is licensed under the MIT License.



Enjoy exploring the capabilities of RAG across multiple interfaces! 

Thank you for your time.
