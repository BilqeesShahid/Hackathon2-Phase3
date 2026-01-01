"""Main FastAPI application for Phase II Todo Backend."""
from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.db.init import init_db

# Create FastAPI application
app = FastAPI(
    title="Evolution of Task by Chatbot API",
    description="REST API for Phase III Full-Stack Todo Application",
    version="1.0.0",
    contact={
        "name": "Phase III Development Team",
    },
)

# Add CORS middleware
add_cors_middleware(app)


@app.on_event("startup")
async def startup_event():
    """Initialize database and MCP server on startup."""
    try:
        init_db()
        print("✅ Database tables initialized successfully.")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {str(e)}")
        print("⚠️  Server will continue but database operations may fail.")
        print("⚠️  Please check your DATABASE_URL and network connection.")

    # Initialize MCP server with tools
    from app.mcp.server import get_mcp_server
    from app.mcp.tools.add_task import register_add_task_tool
    from app.mcp.tools.list_tasks import register_list_tasks_tool
    from app.mcp.tools.update_task import register_update_task_tool
    from app.mcp.tools.complete_task import register_complete_task_tool
    from app.mcp.tools.delete_task import register_delete_task_tool
    from app.mcp.tools.view_task import register_view_task_tool
    from app.db.config import get_session

    mcp_server = get_mcp_server()

    # Register tools with a database session
    # Note: Each tool invocation will use its own session via dependency injection
    # This is just for registration
    try:
        db = next(get_session())
        try:
            register_add_task_tool(mcp_server, db)
            register_list_tasks_tool(mcp_server, db)
            register_view_task_tool(mcp_server, db)
            register_update_task_tool(mcp_server, db)
            register_complete_task_tool(mcp_server, db)
            register_delete_task_tool(mcp_server, db)
            print(f"✅ MCP Server initialized with tools: {mcp_server.list_tools()}")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️  MCP tool registration failed: {str(e)}")
        print("⚠️  Chat functionality may not work until database is accessible.")

    print("✅ Application startup complete.")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint - API welcome message."""
    return {
        "message": "Phase3: Welcome to Evolution of Todo API",
        "title": "Evolution of Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Import and include routers
from app.routers import tasks, auth, chat
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
