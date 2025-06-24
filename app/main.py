from server import mcp


def main():
    print("Hello from mcp-doc-agent!")
    mcp.run(transport='sse')

if __name__ == "__main__":
    main()
