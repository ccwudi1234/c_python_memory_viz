import re
from typing import Dict, Any, List


class CParser:
    def __init__(self):
        self.variables = {}
        self.steps = []
        self.memory_address = 0x10000000

    def parse_code(self, code: str) -> Dict[str, Any]:
        self.variables = {}
        self.steps = []
        self.memory_address = 0x10000000
        
        lines = code.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('//') or stripped_line.startswith('#'):
                continue
            
            if 'int main(' in stripped_line or stripped_line == '{' or stripped_line == '}' or 'return' in stripped_line:
                continue
            
            array_declare = re.match(r'(\w+)\s+(\w+)\[(\d+)\](?:\s*=\s*\{(.+)\})?;', stripped_line)
            if array_declare:
                var_type = array_declare.group(1)
                var_name = array_declare.group(2)
                size = int(array_declare.group(3))
                values_str = array_declare.group(4)
                self._process_array_declare(var_type, var_name, size, values_str, line_num)
                continue
            
            declare_match = re.match(r'(\w+(?:\s*\*)+)\s+(\w+)\s*(?:=\s*(.+))?;', stripped_line)
            if declare_match:
                var_type = declare_match.group(1).strip()
                var_name = declare_match.group(2)
                value_str = declare_match.group(3)
                self._process_pointer_declare(var_type, var_name, value_str, line_num)
                continue
            
            declare_match = re.match(r'(\w+)\s+(\w+)\s*(?:=\s*(.+))?;', stripped_line)
            if declare_match:
                var_type = declare_match.group(1).strip()
                var_name = declare_match.group(2)
                value_str = declare_match.group(3)
                self._process_declare(var_type, var_name, value_str, line_num)
                continue
            
            pointer_assign = re.match(r'(\w+)\s*=\s*&(\w+);', stripped_line)
            if pointer_assign:
                var_name = pointer_assign.group(1)
                target_var = pointer_assign.group(2)
                self._process_pointer_assign(var_name, target_var, line_num)
                continue
            
            deref_assign = re.match(r'\*(\w+)\s*=\s*(.+);', stripped_line)
            if deref_assign:
                var_name = deref_assign.group(1)
                value_str = deref_assign.group(2)
                self._process_deref_assign(var_name, value_str, line_num)
                continue
            
            array_assign = re.match(r'(\w+)\[(\d+)\]\s*=\s*(.+);', stripped_line)
            if array_assign:
                var_name = array_assign.group(1)
                index = int(array_assign.group(2))
                value_str = array_assign.group(3)
                self._process_array_assign(var_name, index, value_str, line_num)
                continue
            
            assign_match = re.match(r'(\w+)\s*=\s*(.+);', stripped_line)
            if assign_match and not stripped_line.startswith(('int', 'char', 'float', 'double', 'void', 'long', 'short')):
                var_name = assign_match.group(1)
                value_str = assign_match.group(2)
                self._process_assign(var_name, value_str, line_num)
                continue

        return {
            "variables": self.variables,
            "steps": self.steps
        }

    def _allocate_address(self):
        addr = f"0x{self.memory_address:08x}"
        self.memory_address += 4
        return addr

    def _process_declare(self, var_type: str, var_name: str, value_str: str, line_num: int):
        value = self._parse_c_value(value_str) if value_str else None
        address = self._allocate_address()
        self.variables[var_name] = {
            "value": value,
            "type": var_type,
            "address": address,
            "is_pointer": False
        }
        self.steps.append({
            "type": "declare",
            "variable": var_name,
            "value": value,
            "line": line_num,
            "address": address
        })

    def _process_pointer_declare(self, var_type: str, var_name: str, value_str: str, line_num: int):
        value = self._parse_c_value(value_str) if value_str else "NULL"
        address = self._allocate_address()
        pointer_level = var_type.count('*')
        self.variables[var_name] = {
            "value": value,
            "type": var_type,
            "address": address,
            "is_pointer": True,
            "pointer_level": pointer_level
        }
        self.steps.append({
            "type": "declare",
            "variable": var_name,
            "value": value,
            "line": line_num,
            "address": address,
            "is_pointer": True
        })

    def _process_pointer_assign(self, var_name: str, target_var: str, line_num: int):
        if var_name in self.variables and target_var in self.variables:
            target_addr = self.variables[target_var]["address"]
            self.variables[var_name]["value"] = target_addr
            self.steps.append({
                "type": "pointer_assign",
                "variable": var_name,
                "value": target_addr,
                "line": line_num,
                "target": target_var
            })

    def _process_deref_assign(self, var_name: str, value_str: str, line_num: int):
        if var_name in self.variables and self.variables[var_name]["is_pointer"]:
            ptr_value = self.variables[var_name]["value"]
            if ptr_value != "NULL" and ptr_value.startswith("0x"):
                for name, info in self.variables.items():
                    if info["address"] == ptr_value:
                        value = self._parse_c_value(value_str)
                        self.variables[name]["value"] = value
                        self.steps.append({
                            "type": "deref_assign",
                            "variable": var_name,
                            "value": value,
                            "line": line_num,
                            "target_address": ptr_value
                        })
                        break

    def _process_array_declare(self, var_type: str, var_name: str, size: int, values_str: str, line_num: int):
        address = self._allocate_address()
        values = []
        if values_str:
            values = [self._parse_c_value(x.strip()) for x in values_str.split(',')]
        while len(values) < size:
            values.append(0)
        
        self.variables[var_name] = {
            "value": values,
            "type": f"{var_type}[{size}]",
            "address": address,
            "is_array": True,
            "size": size
        }
        self.steps.append({
            "type": "declare",
            "variable": var_name,
            "value": values,
            "line": line_num,
            "address": address,
            "is_array": True
        })

    def _process_array_assign(self, var_name: str, index: int, value_str: str, line_num: int):
        if var_name in self.variables and self.variables[var_name].get("is_array"):
            values = self.variables[var_name]["value"].copy()
            if index < len(values):
                values[index] = self._parse_c_value(value_str)
                self.variables[var_name]["value"] = values
                self.steps.append({
                    "type": "assign",
                    "variable": var_name,
                    "value": values,
                    "line": line_num,
                    "index": index
                })

    def _process_assign(self, var_name: str, value_str: str, line_num: int):
        if var_name in self.variables:
            value = self._parse_c_value(value_str)
            if isinstance(value, str) and value in self.variables:
                value = self.variables[value]["value"]
            self.variables[var_name]["value"] = value
            self.steps.append({
                "type": "assign",
                "variable": var_name,
                "value": value,
                "line": line_num
            })

    def _parse_c_value(self, value_str: str):
        if value_str is None:
            return None
        value_str = value_str.strip()
        if value_str == "NULL":
            return "NULL"
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        elif value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1]
        elif value_str.startswith('{') and value_str.endswith('}'):
            content = value_str[1:-1].strip()
            if content:
                return [self._parse_c_value(x.strip()) for x in content.split(',') if x.strip()]
            return []
        elif value_str.replace('.', '', 1).replace('-', '', 1).isdigit():
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        elif value_str.startswith('&'):
            target_var = value_str[1:]
            if target_var in self.variables:
                return self.variables[target_var]["address"]
            return f"&{target_var}"
        return value_str
