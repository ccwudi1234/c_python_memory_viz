import docker
import os
import re
import tempfile
from pathlib import Path

CONTAINER_NAME = 'c_sandbox'

def instrument_code_for_analysis(code: str) -> str:
    global_vars = []
    local_vars = []
    malloc_vars = []

    for match in re.finditer(r'^(?:static\s+)?(?:int|char|float|double)\s+\*?([a-zA-Z_][a-zA-Z0-9_]*)', code, re.MULTILINE):
        name = match.group(1)
        global_vars.append(name)

    main_body = re.search(r'int\s+main\s*\([^\)]*\)\s*\{([\s\S]*)\}$', code)
    if main_body:
        body = main_body.group(1)
        for match in re.finditer(r'(?:int|char|float|double)\s+\*?([a-zA-Z_][a-zA-Z0-9_]*)', body):
            local_vars.append(match.group(1))
        for match in re.finditer(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*malloc\s*\(([^\)]+)\)', body):
            malloc_vars.append((match.group(1), match.group(2).strip()))

    helper_code = '''\n#include <stdio.h>\n#include <stdlib.h>\n
static void __dump_int(const char *name, void *addr, int value) {\n    printf("ANALYZER:STACK:name=%s;addr=%p;value=%d;type=int\\n", name, addr, value);\n}\n
static void __dump_ptr(const char *name, void *addr, void *value) {\n    printf("ANALYZER:STACK:name=%s;addr=%p;value=%p;type=pointer\\n", name, addr, value);\n}\n
static void __dump_heap(const char *name, void *addr, const char *size_expr) {\n    printf("ANALYZER:HEAP:name=%s;addr=%p;size=%s;type=malloc\\n", name, addr, size_expr);\n}\n\n'''

    injection_lines = []
    for name in local_vars:
        if name in [m[0] for m in malloc_vars]:
            injection_lines.append(f'  if ({name}) __dump_ptr("{name}", &{name}, {name});')
            size_expr = next((expr for var, expr in malloc_vars if var == name), 'unknown')
            injection_lines.append(f'  __dump_heap("{name}", {name}, "{size_expr}");')
        else:
            injection_lines.append(f'  __dump_int("{name}", &{name}, {name});')

    injected_code = code
    if main_body and injection_lines:
        brace_index = injected_code.rfind('}')
        if brace_index != -1:
            injected_code = injected_code[:brace_index] + '\n' + '\n'.join(injection_lines) + '\n' + injected_code[brace_index:]
        injected_code = helper_code + injected_code
    else:
        injected_code = helper_code + injected_code

    return injected_code


def compile_and_run(code: str, timeout: int = 5) -> dict:
    client = docker.from_env()
    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        raise RuntimeError('未找到 Docker 沙箱容器，请先运行 docker/start.sh。')

    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / 'temp.c'
        source_code = instrument_code_for_analysis(code)
        source_path.write_text(source_code, encoding='utf-8')

        try:
            with open(source_path, 'rb') as src_file:
                container.put_archive('/code', create_tar_archive(source_path))
        except Exception as exc:
            raise RuntimeError(f'无法将源文件传入 Docker 容器：{exc}')

        try:
            dest_path = '/code/temp.c'
            compile_cmd = f'gcc -g {dest_path} -o /code/a.out -O0 -std=c11'
            compile_exec = container.exec_run(cmd=['sh', '-lc', compile_cmd], stderr=True, stdout=True, demux=True)
            compile_output = ''
            if isinstance(compile_exec.output, tuple):
                stdout, stderr = compile_exec.output
                compile_output = (stdout or b'').decode('utf-8', errors='ignore') + (stderr or b'').decode('utf-8', errors='ignore')
            else:
                compile_output = (compile_exec.output or b'').decode('utf-8', errors='ignore')
            if compile_exec.exit_code != 0:
                return {'compile_error': compile_output}
        except Exception as exc:
            raise RuntimeError(f'编译失败：{exc}')

        try:
            run_cmd = f'timeout {timeout}s /code/a.out'
            run_exec = container.exec_run(cmd=['sh', '-lc', run_cmd], stderr=True, stdout=True, demux=True)
            run_stdout, run_stderr = run_exec.output if hasattr(run_exec, 'output') else run_exec
            run_output = (run_stdout or b'').decode('utf-8', errors='ignore') + (run_stderr or b'').decode('utf-8', errors='ignore')
        except Exception as exc:
            raise RuntimeError(f'运行失败：{exc}')

        return {
            'compile_output': compile_output,
            'run_output': run_output,
            'analysis_output': run_output
        }


def create_tar_archive(file_path: Path) -> bytes:
    import tarfile
    import io
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        tar.add(str(file_path), arcname=file_path.name)
    tar_stream.seek(0)
    return tar_stream.read()
