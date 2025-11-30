import os
import getpass
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def setup_rag():
    """
    Sets up the Retrieval-Augmented Generation (RAG) system by loading a PDF,
    splitting it into chunks, embedding the chunks, and creating a FAISS vector store.
    """
    # Suppress pypdf warnings to prevent stderr noise
    logging.getLogger("pypdf").setLevel(logging.ERROR)

    # 1. Setup OpenAI API Key
    # Check environment, then userdata, then prompt
    if "OPENAI_API_KEY" not in os.environ:
        try:
            from google.colab import userdata
            # Attempt to get key from Colab secrets
            key = userdata.get('OPENAI_API_KEY')
            if key:
                os.environ["OPENAI_API_KEY"] = key
        except ImportError:
            pass
        except Exception:
            # Fail silently on userdata access to avoid alarming stdout/stderr
            pass

    if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
        print("Prompting for API Key...")
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API Key: ")

    # 2. Load the training PDF
    pdf_path = "CISO_Knowledge_Base/CISA_Phising_Training.pdf"
    print(f"Loading PDF from: {pdf_path}")

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        print(f"Loaded {len(docs)} pages.")

        # 3. Split the loaded documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        print(f"Split into {len(splits)} chunks.")

        # 4. Initialize OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()

        # 5. Create FAISS vector store
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

        print(f"Successfully indexed {len(splits)} document chunks into FAISS vectorstore.")

    except Exception as e:
        print(f"An error occurred during RAG setup: {e}")

        return vectorstore