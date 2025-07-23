# lollms-code-patcher/app.py
import uvicorn
import argparse
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from flexipatch import RobustPatcher # <-- Import from your library!

class PatchRequest(BaseModel):
    original_code: str
    patch_text: str

app = FastAPI(
    title="Code Patcher API",
    description="An API to apply git-style patches to code using the FlexiPatch library.",
    version="3.0.0" # App version 3, powered by library version 1!
)

@app.post("/patch")
async def apply_patch_route(request: PatchRequest):
    try:
        patcher = RobustPatcher()
        patched_code = patcher.apply_patch(request.original_code, request.patch_text)
        return JSONResponse(content={"patched_code": patched_code})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {str(e)}")

app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Patcher Lollms App")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=9601, help="Port to run the server on")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
