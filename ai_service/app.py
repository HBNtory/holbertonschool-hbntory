from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


@app.post("/query")
async def query(request: Request):
    query_json = await request.json()

    question = query_json.get("query")

    if not question:
        raise HTTPException(status_code=400,
                            detail="The 'query' field is required")

    return {"answer": "To build "}
