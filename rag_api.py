import os

from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

client=Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding=HuggingFaceEmbeddings(

model_name="BAAI/bge-small-en-v1.5"

)

db=Chroma(

persist_directory="chroma_db",

embedding_function=embedding

)

retriever=db.as_retriever(search_kwargs={"k":3})


def ask(question):

    docs=retriever.invoke(question)

    context="\n\n".join([d.page_content for d in docs])

    prompt = f"""
    You are a Bank of America Credit Card assistant.

    Use ONLY the provided context.

    Rules:
    1. Mention the card name exactly as it appears in the context.
    2. Do not guess or use outside knowledge.
    3. If multiple cards match, list all of them.
    4. If the answer is missing, reply:
    "I couldn't find that information."

    Context:
    {context}

    Question:
    {question}
    """

    response=client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ]

    )

    answer=response.choices[0].message.content

    return answer,docs