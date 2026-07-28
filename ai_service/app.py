from fastapi import FastAPI, HTTPException, Request
from services.runner import run_inventory_agent

app = FastAPI()


@app.post("/query")
async def ask_inventory_agent(request: Request):
    query_json = await request.json()
    print(query_json)
    question = query_json.get("query")

    if not question:
        raise HTTPException(status_code=400,
                            detail="The 'query' field can not be empty")

    answer = await run_inventory_agent(question)
    return {"answer": answer}
