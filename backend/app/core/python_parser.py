import ast
from typing import List, Dict, Any


class PythonParser:
    def __init__(self):
        self.variables = {}
        self.steps = []

    def parse_code(self, code: str) -> Dict[str, Any]:
        tree = ast.parse(code)
        self.variables = {}
        self.steps = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                self._process_assign(node)
            elif isinstance(node, ast.AnnAssign):
                self._process_ann_assign(node)
            elif isinstance(node, ast.Call):
                self._process_call(node)

        return {
            "variables": self.variables,
            "steps": self.steps
        }

    def _process_assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                value = self._eval_expr(node.value)
                self.variables[var_name] = {
                    "value": value,
                    "type": type(value).__name__,
                    "address": hex(id(value)) if value is not None else None
                }
                self.steps.append({
                    "type": "assign",
                    "variable": var_name,
                    "value": value,
                    "line": node.lineno
                })

    def _process_ann_assign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            value = self._eval_expr(node.value) if node.value else None
            self.variables[var_name] = {
                "value": value,
                "type": type(value).__name__ if value else None,
                "address": hex(id(value)) if value is not None else None
            }
            self.steps.append({
                "type": "assign",
                "variable": var_name,
                "value": value,
                "line": node.lineno
            })

    def _process_call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ["copy", "deepcopy"]:
                self.steps.append({
                    "type": "copy",
                    "method": node.func.attr,
                    "line": node.lineno
                })

    def _eval_expr(self, node: ast.AST):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.List):
            return [self._eval_expr(elem) for elem in node.elts]
        elif isinstance(node, ast.Dict):
            return {self._eval_expr(k): self._eval_expr(v) 
                    for k, v in zip(node.keys, node.values)}
        elif isinstance(node, ast.Name):
            return self.variables.get(node.id, {}).get("value")
        return None
