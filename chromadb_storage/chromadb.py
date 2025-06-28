import chromadb

# New ChromaDB persistent client (2024+ compatible)
chroma_client = chromadb.PersistentClient(path="./chromadb_storage")

#Create or get a collection to store versioned files
collection = chroma_client.get_or_create_collection(name="versioned_files")
