import os
import tiktoken
from openai import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
files_dir = os.path.join(current_dir, "docs")
db_dir = os.path.join(current_dir, "db")

# Initialize tokenizer for text-embedding-3-large
tokenizer = tiktoken.get_encoding("cl100k_base")

# Initialize OpenAI client
openai_client = OpenAI()


def count_tokens(text):
    """Get exact token count using OpenAI's tiktoken"""
    return len(tokenizer.encode(text))


def create_rag_prompt(query, retrieved_docs):
    """Create a comprehensive RAG prompt with retrieved context"""
    context_text = ""

    for i, doc in enumerate(retrieved_docs, 1):
        source = doc.metadata.get("source", "Unknown") if doc.metadata else "Unknown"
        context_text += f"--- Document {i} (Source: {os.path.basename(source)}) ---\n"
        context_text += f"{doc.page_content}\n\n"

    prompt = f"""Du bist ein Experte für Bankenregulierung und Risikomanagement. Beantworte die folgende Frage basierend auf den bereitgestellten Dokumenten.

KONTEXT AUS DOKUMENTEN:
{context_text}

FRAGE:
{query}

ANWEISUNGEN:
- Verwende nur Informationen aus den bereitgestellten Dokumenten
- Wenn die Antwort nicht in den Dokumenten zu finden ist, sage das explizit
- Zitiere spezifische Dokumente wenn möglich
- Erkläre deine Schlussfolgerungen Schritt für Schritt
- Antworte auf Deutsch

ANTWORT:"""

    return prompt


def create_openai_embeddings(doc_path):
    if doc_path.endswith(".docx"):
        loader = Docx2txtLoader(doc_path)
    elif doc_path.endswith(".pdf"):
        loader = PyPDFLoader(doc_path)
    else:
        raise ValueError(f"Unsupported file type: {doc_path}")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    docs = text_splitter.split_documents(documents)
    print(f"Processed {doc_path}: {len(docs)} chunks")
    openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return docs, openai_embeddings


def get_supported_files(directory):
    """Get all supported document files from directory"""
    supported_extensions = [".docx", ".pdf"]
    files = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if any(file.endswith(ext) for ext in supported_extensions):
                files.append(os.path.join(directory, file))
    return files


def get_existing_sources(store_name):
    """Get list of source files already in the vector store"""
    persistent_directory = os.path.join(db_dir, store_name)
    existing_sources = set()

    if os.path.exists(persistent_directory):
        try:
            embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
            db = Chroma(
                persist_directory=persistent_directory, embedding_function=embeddings
            )
            # Get all documents to check their sources
            all_docs = db.get()
            if all_docs and "metadatas" in all_docs:
                for metadata in all_docs["metadatas"]:
                    if metadata and "source" in metadata:
                        existing_sources.add(metadata["source"])
        except Exception as e:
            print(f"Warning: Could not check existing sources: {e}")

    return existing_sources


def create_batches(docs, max_tokens_per_batch=200000):
    """Split documents into batches to stay under OpenAI token limits"""
    batches = []
    current_batch = []
    current_tokens = 0

    print(f"Creating batches with max {max_tokens_per_batch} tokens per batch")

    for i, doc in enumerate(docs):
        doc_tokens = count_tokens(doc.page_content)

        # If adding this doc would exceed the limit, start a new batch
        if current_tokens + doc_tokens > max_tokens_per_batch and current_batch:
            print(
                f"  Batch {len(batches) + 1}: {len(current_batch)} chunks, {current_tokens} tokens"
            )
            batches.append(current_batch)
            current_batch = [doc]
            current_tokens = doc_tokens
        else:
            current_batch.append(doc)
            current_tokens += doc_tokens

    # Add the last batch if it has documents
    if current_batch:
        print(
            f"  Batch {len(batches) + 1}: {len(current_batch)} chunks, {current_tokens} tokens"
        )
        batches.append(current_batch)

    total_tokens = sum(count_tokens(doc.page_content) for doc in docs)
    print(f"Total exact tokens: {total_tokens}")

    return batches


def create_or_update_vector_store(docs, embeddings, store_name):
    """Create new vector store or add documents to existing one"""
    persistent_directory = os.path.join(db_dir, store_name)

    if not os.path.exists(persistent_directory):
        print(f"\n--- Creating new vector store: {store_name} ---")
        # For new stores, we can still create in batches if needed
        if len(docs) > 100:  # Arbitrary threshold for batching
            batches = create_batches(docs)
            print(f"Creating vector store in {len(batches)} batches")

            # Create with first batch
            db = Chroma.from_documents(
                batches[0], embeddings, persist_directory=persistent_directory
            )
            print(f"Created initial store with {len(batches[0])} chunks")

            # Add remaining batches
            for i, batch in enumerate(batches[1:], 2):
                print(f"Adding batch {i}/{len(batches)} ({len(batch)} chunks)")
                db.add_documents(batch)
        else:
            db = Chroma.from_documents(
                docs, embeddings, persist_directory=persistent_directory
            )
        print(f"--- Created vector store with {len(docs)} total chunks ---")
    else:
        print(f"\n--- Adding documents to existing vector store: {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory, embedding_function=embeddings
        )

        # Process in batches to avoid token limits
        batches = create_batches(docs)
        print(f"Adding {len(docs)} chunks in {len(batches)} batches")

        for i, batch in enumerate(batches, 1):
            print(f"Processing batch {i}/{len(batches)} ({len(batch)} chunks)")
            try:
                db.add_documents(batch)
                print(f"  ✅ Batch {i} added successfully")
            except Exception as e:
                print(f"  ❌ Error adding batch {i}: {e}")
                # Continue with remaining batches
                continue

        print(f"--- Finished adding documents to vector store ---")

    return db


def process_all_documents(store_name="chroma_db"):
    """Process all supported documents in the files directory"""
    print(f"\n--- Processing all documents in {files_dir} ---")

    # Get all supported files
    doc_files = get_supported_files(files_dir)

    if not doc_files:
        print("No supported documents found (.docx, .pdf)")
        return None

    print(f"Found {len(doc_files)} document(s) to process")

    # Check which files are already in the vector store
    existing_sources = get_existing_sources(store_name)
    new_files = [f for f in doc_files if f not in existing_sources]

    if existing_sources:
        print(f"Files already in vector store: {len(existing_sources)}")
        for source in existing_sources:
            print(f"  - {os.path.basename(source)}")

    if not new_files:
        print("All files have already been processed!")
        # Still return the embeddings object for querying
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        persistent_directory = os.path.join(db_dir, store_name)
        if os.path.exists(persistent_directory):
            db = Chroma(
                persist_directory=persistent_directory, embedding_function=embeddings
            )
            return db, embeddings
        return None

    print(f"New files to process: {len(new_files)}")
    for file in new_files:
        print(f"  - {os.path.basename(file)}")

    all_docs = []
    embeddings = None

    # Process only new documents
    for doc_path in new_files:
        try:
            docs, emb = create_openai_embeddings(doc_path)
            all_docs.extend(docs)
            if embeddings is None:
                embeddings = emb
        except Exception as e:
            print(f"Error processing {doc_path}: {e}")
            continue

    if not all_docs:
        print("No new documents were successfully processed")
        return None

    print(f"\n--- Total new chunks to add: {len(all_docs)} ---")

    # Create or update vector store
    db = create_or_update_vector_store(all_docs, embeddings, store_name)
    return db, embeddings


# Function to query a vector store
def query_vector_store(store_name, query, embedding_function):
    """Query vector store and display raw results (for debugging)"""
    persistent_directory = os.path.join(db_dir, store_name)
    if os.path.exists(persistent_directory):
        print(f"\n--- Querying the Vector Store {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_function,
        )
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.1},
        )
        relevant_docs = retriever.invoke(query)
        # Display the relevant results with metadata
        print(f"\n--- Relevant Documents for {store_name} ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"Document {i}/{len(relevant_docs)}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")
    else:
        print(f"Vector store {store_name} does not exist.")


def query_with_rag(store_name, query, embedding_function, model="gpt-4o"):
    """Query vector store and generate response using RAG with GPT-4o"""
    persistent_directory = os.path.join(db_dir, store_name)

    if not os.path.exists(persistent_directory):
        print(f"Vector store {store_name} does not exist.")
        return None

    print(f"\n--- RAG Query: {store_name} ---")
    print(f"Question: {query}\n")

    # Retrieve relevant documents
    db = Chroma(
        persist_directory=persistent_directory,
        embedding_function=embedding_function,
    )
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.1,
        },  # Get more docs for better context
    )
    relevant_docs = retriever.invoke(query)

    if not relevant_docs:
        print("No relevant documents found for this query.")
        return None

    print(f"Found {len(relevant_docs)} relevant document chunks")

    # Create RAG prompt
    rag_prompt = create_rag_prompt(query, relevant_docs)

    # Check token count
    prompt_tokens = count_tokens(rag_prompt)
    print(f"Prompt tokens: {prompt_tokens}")

    if prompt_tokens > 120000:  # Leave room for response tokens
        print(
            "Warning: Prompt is very long, consider reducing the number of retrieved documents"
        )

    try:
        print("\n--- Generating response with GPT-4o ---")
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": rag_prompt}],
            max_tokens=8000,
            temperature=0.3,
        )

        answer = response.choices[0].message.content

        print("\n" + "=" * 80)
        print("RAG RESPONSE:")
        print("=" * 80)
        print(answer)
        print("=" * 80)

        # Optional: Show source documents used
        print(f"\n--- Sources used ({len(relevant_docs)} documents) ---")
        for i, doc in enumerate(relevant_docs, 1):
            source = (
                doc.metadata.get("source", "Unknown") if doc.metadata else "Unknown"
            )
            print(f"{i}. {os.path.basename(source)}")

        return answer

    except Exception as e:
        print(f"Error generating response: {e}")
        return None


if __name__ == "__main__":
    # Process all documents and create/update vector store
    result = process_all_documents("chroma_db")

    if result:
        db, embeddings = result

        # Test query with RAG
        test_query = """
        Erkläre wieso dieses Geschäft den Risikoansatz B500 = 2 (IRB) hat und untersuche, welchen CCF Faktor (Feld B017) dieses Geschäft bekommen müsste. 
        Nutze dazu die Mapping-Dateien: 
        Position_ID = FRWDH2765765 ; A020 = "Deutsche Großbank AG"; A100 = 45000000000; B010 = "Corporate Banking"; B017 = ? ; B020 = "Firmenkundengeschäft"; B100 = 2500000; B120 = "Betriebsmittelkredit"; B200 = 15000000000; B300 = "BB+"; B400 = 3.5PD in %; B500 = 2; B600 = "T"; C010 = "Deutschland"
        """

        # Use RAG with GPT-4o to generate comprehensive answer
        answer = query_with_rag("chroma_db", test_query, embeddings)

        # Optional: Also show raw retrieved documents for debugging
        if answer:
            print("\n" + "=" * 80)
            print("RAW RETRIEVED DOCUMENTS (for debugging):")
            print("=" * 80)
            query_vector_store("chroma_db", test_query, embeddings)
    else:
        print("No documents to process or errors occurred")
