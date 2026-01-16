import uvicorn
import asyncio
import sys
import traceback

def main():
    print("Starting Todo API server with debug info...")
    try:
        # Import the app here to catch any import errors
        from app.main import app
        print("App imported successfully")
        
        # Run the server
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()