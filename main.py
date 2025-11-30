from fastmcp import FastMCP
from ciso_rag import setup_ciso_rag
from ciso_prompts import prompt_CoT

mcp = FastMCP(name="CISO-Agent-Phishing")

vectorstore = setup_ciso_rag()

@mcp.tool(
    name="CISO Agent - Phishing",
    description="Cybersecurity agent tool used to prevent phishing attacks on agents.",
    tags={"cybersecurity", "phishing"},
    meta={"version": "1", "author": "Jose M Luna and Ron Litvak"}
)

def ciso_check(url) -> str:
    """
    Consults the CISO security policy RAG index to provide context-aware advice.
    Args:
        query: The specific URL about to be accessed.
    Returns:
        A security assessment based on the training materials.
    """
    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # a. Retrieve relevant documents
    # Utilizing the 'vectorstore' created in the previous step
    docs = vectorstore.similarity_search(url, k=3)

    # b. Construct context
    context_text = "\n\n".join([d.page_content for d in docs])

    # c. Create prompt
    prompt = prompt_CoT(query, context_text)

    # d. Generate response
    response = llm.invoke(prompt)
    return response.content