from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

documents = SimpleDirectoryReader("data").load_data()

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

index = VectorStoreIndex.from_documents(
    documents,
)

history = ""

query_engine = index.as_query_engine(streaming=True)

while True:
    print("\nPrompt >")
    query = input()
    response = query_engine.query(history + query)
    history += query + '\n'
    for text in response.response_gen:
        print(text, end='')
        history += text
    history += '\n'
