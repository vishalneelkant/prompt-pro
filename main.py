import os
import pinecone
import re
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

# Load environment variables from .env file
load_dotenv()


# Init Pinecone client
pc = pinecone.Pinecone(api_key=os.getenv('PINECONE'))

# Create index if not exists
index_name = "prompt-technique2"
if index_name not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=pinecone.ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

docs = [
    "Few-shot prompting: Provide a few input-output examples before the actual query to guide the model.",
    "Chain-of-thought prompting: Ask the model to reason step by step before answering.",
    "Zero-shot prompting: Directly ask the model without giving examples.",
    "Role prompting: Assign a role to the model, e.g., 'You are an expert teacher...'.",
    "Self-consistency prompting: Sample multiple reasoning paths and pick the most consistent answer."
]

# Create vectorstore
vectorstore = PineconeVectorStore.from_texts(
    texts=docs,
    embedding=embeddings,
    index_name=index_name
)

retriever = vectorstore.as_retriever()

# Test a query
query = "What is chain-of-thought prompting?"
results = retriever.get_relevant_documents(query)
print(results)
# for r in results:
#     print(r.page_content)

def clean_prompt(prompt: str) -> str:
    useless_words = ["actually", "basically", "just", "like", "I mean", "you know"]
    regex = r"\b(" + "|".join(useless_words) + r")\b"
    cleaned = re.sub(regex, "", prompt, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()

def apply_strategy(user_prompt: str, context: str = "general"):
    # Step 1: Clean
    cleaned_prompt = clean_prompt(user_prompt)

    # Step 2: Retrieve best strategy
    results = retriever.get_relevant_documents(cleaned_prompt)
  
    best_strategy = results[0].page_content if results else "Default: Direct query"
    #print("Strategy Identified: ", best_strategy)

    # Step 3: Apply strategy template
    template = f"""
    You are a Prompt Optimizer AI.

    Your task:
    1. Carefully apply the given prompting strategy.
    2. Rewrite the user’s prompt to make it clearer, more concise, and highly effective for an LLM.
    3. Remove filler words and unnecessary phrases.
    4. Ensure the final prompt maximizes reasoning and output quality.

    Strategy to Apply:
    {best_strategy}

    Original User Prompt:
    {cleaned_prompt}

    Return ONLY the optimized and reformulated prompt.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    response = llm.predict(template)
    return {
        "original": user_prompt,
        "cleaned": cleaned_prompt,
        "strategy": best_strategy,
        "final_prompt": response
    }


#user_prompt = "Can you just basically tell me how to write a poem in detail?"
user_prompt = "Explain machine learning models"
result = apply_strategy(user_prompt, "general")

# Test rephrase context
user_prompt_with_errors = "i recieve ur messege and will definately respond. its very importent for me to, like, get this right."
result_rephrase = apply_strategy(user_prompt_with_errors, "rephrase")

print("🔹 Original Prompt:", result["original"])
print("🔹 Cleaned Prompt:", result["cleaned"])
print("🔹 Selected Strategy:", result["strategy"])
print("🔹 Final Reformulated Prompt:", result["final_prompt"])

print("\n" + "="*60)
print("🧪 TESTING REPHRASE CONTEXT:")
print("🔹 Original Text with Errors:", result_rephrase["original"])
print("🔹 Cleaned Text:", result_rephrase["cleaned"])
print("🔹 Selected Strategy:", result_rephrase["strategy"])
print("🔹 Final Corrected Text:", result_rephrase["final_prompt"])