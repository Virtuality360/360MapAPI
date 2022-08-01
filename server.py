import uvicorn

def main() -> None:
    """Starts up the uvicorn server"""
    uvicorn.run(
        "src.api:api",
        host='0.0.0.0',
        port=8888,
    )

if __name__ == "__main__":
    main()