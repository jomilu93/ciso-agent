from fastmcp import FastMCP, Context
from ciso_rag import setup_rag
from ciso_prompts import prompt_CoT
from langchain_openai import ChatOpenAI
import sys
import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

@dataclass
class AppContext:
    """Application context holding initialized resources."""
    vectorstore: object  # FAISS vectorstore - always available if server started

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Server lifespan manager - initializes RAG vectorstore on startup."""
    print("Initializing CISO Agent RAG vectorstore...")
    vectorstore = setup_rag()  # Let exceptions propagate - fail fast on errors
    print("Vectorstore initialized successfully.")

    ctx = AppContext(vectorstore=vectorstore)

    try:
        yield ctx
    finally:
        print("Shutting down CISO Agent...")

mcp = FastMCP(name="CISO-Agent-Phishing", lifespan=app_lifespan)

@mcp.tool(
    name="CISO Agent - Phishing",
    description="Cybersecurity agent tool used to prevent phishing attacks on agents.",
    tags={"cybersecurity", "phishing"},
    meta={"version": "1", "author": "Jose M Luna and Ron Litvak"}
)

async def ciso_check(url: str, ctx: Context) -> str:
    """
    Consults the CISO security policy RAG index to provide context-aware advice.
    Args:
        url: The specific URL about to be accessed.
        ctx: FastMCP context with access to lifespan resources.
    Returns:
        A security assessment based on the training materials.
    """
    # Access vectorstore from lifespan context
    app_ctx: AppContext = ctx.fastmcp._lifespan_result

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # a. Retrieve relevant documents
    docs = app_ctx.vectorstore.similarity_search(url, k=3)

    # b. Construct context
    context_text = "\n\n".join([d.page_content for d in docs])

    # c. Create prompt
    prompt = prompt_CoT(url, context_text)

    # d. Generate response
    response = llm.invoke(prompt)
    return response.content

# Check if the user passed an argument (e.g., "python main.py test www.google.com")
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode: Initialize vectorstore directly
        print("--- Manual Testing Mode ---")
        vectorstore = setup_rag()

        test_url = sys.argv[2] if len(sys.argv) > 2 else "www.google.com"
        print(f"Testing URL: {test_url}")

        # Create a mock context for testing
        @dataclass
        class MockFastMCP:
            _lifespan_result: AppContext

        @dataclass
        class MockContext:
            fastmcp: MockFastMCP

        test_app_ctx = AppContext(vectorstore=vectorstore)
        mock_fastmcp = MockFastMCP(_lifespan_result=test_app_ctx)
        mock_ctx = MockContext(fastmcp=mock_fastmcp)

        # Get the unwrapped function
        ciso_check_fn = ciso_check.fn

        # Run the async function
        try:
            result = asyncio.run(ciso_check_fn(test_url, mock_ctx))
            print("\nRESULT:")
            print(result)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    else:
        # Normal mode: Start the MCP Server
        print("Starting MCP Server... (Use 'fastmcp dev main.py' to test visually)")
        mcp.run(transport="stdio")
