from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from c_compiler import compile_and_run
from memory_analyzer import parse_memory

class CodePayload(BaseModel):
    code: str

app = FastAPI(
    title='C Memory Visualization Backend',
    description='通过 Docker 沙箱编译运行 C 代码并返回内存布局数据的后端服务。'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/run_c')
async def run_c(payload: CodePayload):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail='C 代码不能为空。')

    try:
        compile_result = compile_and_run(payload.code)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))

    if compile_result.get('compile_error'):
        raise HTTPException(status_code=400, detail=compile_result['compile_error'])

    try:
        memory_data = parse_memory(compile_result['analysis_output'])
    except Exception as error:
        raise HTTPException(status_code=500, detail=f'内存解析失败：{error}')

    return memory_data
