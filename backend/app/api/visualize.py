from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.visual_data_generator import VisualDataGenerator
from typing import Dict

router = APIRouter(prefix="/api/visualize", tags=["visualize"])


class VariableRequest(BaseModel):
    variables: Dict


class ListRequest(BaseModel):
    var_name: str
    list_data: list


@router.post("/variable")
async def get_variable_visual_data(request: VariableRequest):
    try:
        generator = VisualDataGenerator()
        data = generator.generate_variable_data(request.variables)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/list")
async def get_list_visual_data(request: ListRequest):
    try:
        generator = VisualDataGenerator()
        data = generator.generate_list_data(request.var_name, request.list_data)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/copy")
async def get_copy_comparison():
    try:
        generator = VisualDataGenerator()
        data = generator.generate_copy_comparison()
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
