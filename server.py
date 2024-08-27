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

query_engine = index.as_query_engine(streaming=True)

from bottle import route, request, run, static_file

from gevent import monkey; monkey.patch_all()

from os import path

root = path.join(path.dirname(__file__), 'frontend/build')
print(root)

@route('/')
def root():
    return static_file('index.html', root=root)

@route('/<filename>')
def server_static(filename):
    return static_file(filename, root=root)

@route('/chat')
def chat():
    history = request.query.history or ''
    query = request.query.query
    print(history + 'Prompt >\n' + query)
    response = query_engine.query(history + query)
    for text in response.response_gen:
        print(text, end='')
        yield text
    print('\n')

run(host='0.0.0.0', port=8080, server='gevent')
