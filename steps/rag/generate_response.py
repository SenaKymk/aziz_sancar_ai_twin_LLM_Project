# steps/rag/generate_response.py
from zenml import step
from zenml.client import Client
from zenml.logger import get_logger
from openai import OpenAI
from llm_engineering.settings import settings


@step
def generate_response(context: str, query: str = "nobel ödülü kazandıktan sonra gençlere ne öğütü verdin?") -> str:
    """
    Generates a response using the retrieved context and OpenAI model.
    Also logs metadata (context length, response length, model name) to ZenML.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    logger = get_logger(__name__)
    zenml_client = Client()

    messages = [
        {
            "role": "system",
            "content": (
                "You are the digital twin of Prof. Aziz Sancar, a Nobel Prize–winning biochemist and molecular biologist. "
                "You speak in the first person as Aziz Sancar himself, referring to your life, discoveries, and publications "
                "as 'my work', 'my research', and 'my colleagues'. "
                "You possess deep, factual knowledge about Aziz Sancar’s biography, education, Nobel Prize–winning research on DNA repair, "
                "and all major publications related to molecular biology, photolyase enzymes, and nucleotide excision repair. "
                "When asked 'Who is Aziz Sancar?', respond as 'I am Aziz Sancar...' "
                "When asked about a publication, respond as if you are explaining your own article, for example: "
                "'In my paper titled ... I demonstrated that ...'. "
                "Use an informative yet humble and professional tone, mirroring how Aziz Sancar would communicate in an academic interview."
            ),
        },
        {
            "role": "user",
            "content": f"Kontekst: {context}\n\nSoru: {query}",
        },
    ]

    # === 2️⃣ Model çağrısı ===
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )

    answer = completion.choices[0].message.content.strip()

    # === 3️⃣ Metadata loglama ===
    metadata = {
        "context_length": len(context),
        "response_length": len(answer),
        "model_name": "gpt-4o-mini",
        "query": query[:80],  # uzun sorguları kısaltarak sakla
    }

    try:
        zenml_client.get_pipeline_run().log_metadata(metadata)
        logger.info(f"✅ Metadata logged successfully: {metadata}")
    except Exception as e:
        logger.warning(f"⚠️ Metadata could not be logged: {e}")

    # === 4️⃣ Terminal çıktısı ===
    print("\n💬 Yanıt:\n", answer)
    return answer