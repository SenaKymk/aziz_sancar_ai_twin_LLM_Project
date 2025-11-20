# steps/rag/retrieve_context.py
from zenml import step
from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector

@step
def retrieve_context(query: str = "nobel ödülü kazandıktan sonra gençlere ne öğütü verdin?"):
    """
    Retrieves the most relevant context documents from Qdrant DB.
    """
    qdrant = QdrantDatabaseConnector()
    results, _ = qdrant.scroll(collection_name="embedded_articles", limit=3)

    print("\n🔍 Retrieved Context Documents:")
    contexts = []
    for r in results:
        payload = r.payload if hasattr(r, "payload") else {}
        title = payload.get("title", "Untitled")
        content = payload.get("text", "")
        print(f" - {title}")
        contexts.append(f"{title}\n{content}")

    return "\n\n".join(contexts)
