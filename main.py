import os
import cohere
import uvicorn

from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException,Depends,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED


cohere_api_token = os.environ['cohere_api_key']
co = cohere.Client(cohere_api_token)
app = FastAPI()
security = HTTPBasic()


class Promt(BaseModel):
    query: str
    query_name: Optional[str] = None
    model: str = "command-nightly"
    num_of_generate : int = 1

@app.post("/generate/")
async def generate_answer(promt: Promt, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != os.environ["user_name"] or credentials.password != os.environ["user_password"]:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Basic"},
        )
    response = co.generate(
        model=promt.model,
        prompt=promt.query,
        return_likelihoods='GENERATION',
        num_generations = promt.num_of_generate,
        max_tokens=200)
    return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_201_CREATED)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)