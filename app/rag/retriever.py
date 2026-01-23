#Finds the most relevant properties for a user query

def get_retriever(vector_store, k: int = 5):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
