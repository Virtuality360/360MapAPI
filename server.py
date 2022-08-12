import uvicorn

def main() -> None:
    """Starts up the uvicorn server"""
    uvicorn.run(
        "src.api:api",
        host='0.0.0.0',
        port=8882,
        reload=True
    )

if __name__ == "__main__":
    main()