from mcp.server.fastmcp import FastMCP
from milvus import get_retriever

rag_db = get_retriever("TestCollection")
mcp = FastMCP(name="Milvus Server")
mcp.settings.port = 8080

@mcp.tool()
async def rag_search(query: str) -> str:
    """Retrieve information related to the documents."""
    try: 
        return await rag_db.ainvoke(query)
    except Exception as e:
        return f"Failed to get information. Error: {repr(e)}"

if __name__ == "__main__":
    print("Starting Milvus server...")
    mcp.run(transport="sse")