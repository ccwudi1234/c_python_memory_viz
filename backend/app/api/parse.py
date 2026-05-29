from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.python_parser import PythonParser
from app.core.memory_simulator import MemorySimulator
from app.core.code_auditor import CodeAuditor

router = APIRouter(prefix="/api/parse", tags=["parse"])


class CodeRequest(BaseModel):
    code: str
    language: str = "python"


@router.post("/python")
async def parse_python(request: CodeRequest):
    try:
        parser = PythonParser()
        result = parser.parse_code(request.code)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simulate")
async def simulate_memory(request: CodeRequest):
    try:
        simulator = MemorySimulator()
        result = simulator.simulate(request.code, request.language)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/audit")
async def audit_code(request: CodeRequest):
    try:
        auditor = CodeAuditor()
        result = auditor.audit(request.code, request.language)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
