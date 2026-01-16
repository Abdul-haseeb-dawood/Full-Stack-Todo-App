import uvicorn


def main():
    print("Starting Todo API server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    main()
