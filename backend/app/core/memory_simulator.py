from typing import Dict, Any, List


class MemorySimulator:
    def __init__(self):
        self.memory_blocks = {}
        self.variable_map = {}
        self.step_counter = 0

    def simulate(self, code: str, language: str = "python") -> Dict[str, Any]:
        self.memory_blocks = {}
        self.variable_map = {}
        self.step_counter = 0
        states = []
        variables = {}

        if language in ["python", "py"]:
            from app.core.python_parser import PythonParser
            parser = PythonParser()
            parse_result = parser.parse_code(code)
            variables = parse_result["variables"]
            steps = parse_result["steps"]

            for step in steps:
                state = self._process_python_step(step, variables)
                states.append(state)
        elif language in ["c", "cpp", "c++"]:
            from app.core.c_parser import CParser
            parser = CParser()
            parse_result = parser.parse_code(code)
            variables = parse_result["variables"]
            steps = parse_result["steps"]

            for step in steps:
                state = self._process_c_step(step, variables)
                states.append(state)

        return {
            "initial_state": self._get_state(),
            "states": states,
            "variables": variables
        }

    def _process_python_step(self, step: Dict, variables: Dict) -> Dict:
        self.step_counter += 1
        
        if step["type"] == "assign":
            var_name = step["variable"]
            value = step["value"]
            
            # Remove variable from any existing block first
            for addr, block in list(self.memory_blocks.items()):
                if var_name in block["refs"]:
                    block["refs"].remove(var_name)
                    if not block["refs"]:
                        del self.memory_blocks[addr]
            
            address = hex(id(value)) if value is not None else None
            self.variable_map[var_name] = address
            
            if address and address not in self.memory_blocks:
                self.memory_blocks[address] = {
                    "value": value,
                    "type": type(value).__name__ if value else None,
                    "size": self._estimate_size(value),
                    "refs": [var_name]
                }
            elif address:
                if var_name not in self.memory_blocks[address]["refs"]:
                    self.memory_blocks[address]["refs"].append(var_name)

        return {
            "step": self.step_counter,
            "type": step["type"],
            "line": step.get("line", 0),
            "memory": dict(self.memory_blocks),
            "variables": dict(self.variable_map)
        }

    def _process_c_step(self, step: Dict, variables: Dict) -> Dict:
        self.step_counter += 1
        
        if step["type"] in ["declare", "assign"]:
            var_name = step["variable"]
            var_info = variables.get(var_name, {})
            address = var_info.get("address", f"0x{hash(var_name) & 0xffffffff:08x}")
            
            self.variable_map[var_name] = address
            
            if address not in self.memory_blocks:
                self.memory_blocks[address] = {
                    "value": step.get("value") or var_info.get("value"),
                    "type": var_info.get("type", "unknown"),
                    "size": 4,
                    "refs": [var_name]
                }
            else:
                self.memory_blocks[address]["value"] = step.get("value") or var_info.get("value")
                
                if var_name not in self.memory_blocks[address]["refs"]:
                    self.memory_blocks[address]["refs"].append(var_name)

        return {
            "step": self.step_counter,
            "type": step["type"],
            "line": step.get("line", 0),
            "memory": dict(self.memory_blocks),
            "variables": dict(self.variable_map)
        }

    def _get_state(self) -> Dict:
        return {
            "memory": dict(self.memory_blocks),
            "variables": dict(self.variable_map)
        }

    def _estimate_size(self, value) -> int:
        if isinstance(value, (int, float)):
            return 28
        elif isinstance(value, str):
            return 49 + len(value)
        elif isinstance(value, list):
            size = 40
            for item in value:
                if isinstance(item, list):
                    size += self._estimate_size(item)
                else:
                    size += 28
            return size
        elif isinstance(value, dict):
            size = 232
            for k, v in value.items():
                size += self._estimate_size(k) + self._estimate_size(v)
            return size
        return 0
