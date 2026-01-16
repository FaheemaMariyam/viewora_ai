#Finds the most relevant properties for a user query
# def get_retriever(vector_store, k=5):
#     """
#     Returns a retriever that fetches top-k similar documents.
#     """
#     return vector_store.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": k}
#     )
def get_retriever(vector_store, k: int = 5):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
