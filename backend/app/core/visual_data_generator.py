from typing import Dict, Any, List


class VisualDataGenerator:
    def __init__(self):
        pass

    def generate_variable_data(self, variables: Dict) -> List[Dict]:
        nodes = []
        links = []

        for var_name, var_info in variables.items():
            nodes.append({
                "id": var_name,
                "label": var_name,
                "type": "variable",
                "value": var_info.get("value"),
                "data_type": var_info.get("type"),
                "address": var_info.get("address")
            })

        return {
            "nodes": nodes,
            "links": links
        }

    def generate_list_data(self, var_name: str, lst: List) -> Dict:
        nodes = []
        links = []

        list_node = {
            "id": var_name,
            "label": var_name,
            "type": "list",
            "length": len(lst)
        }
        nodes.append(list_node)

        for i, item in enumerate(lst):
            item_node = {
                "id": f"{var_name}_{i}",
                "label": str(item),
                "type": "element",
                "index": i,
                "value": item
            }
            nodes.append(item_node)
            links.append({
                "source": var_name,
                "target": f"{var_name}_{i}",
                "type": "contains"
            })

        return {
            "nodes": nodes,
            "links": links
        }

    def generate_copy_comparison(self) -> Dict:
        return {
            "reference": {
                "description": "引用赋值：b = a，两个变量指向同一内存地址",
                "color": "#e74c3c"
            },
            "shallow": {
                "description": "浅拷贝：b = a.copy()，容器是新对象，元素引用原对象",
                "color": "#f39c12"
            },
            "deep": {
                "description": "深拷贝：b = deepcopy(a)，完全独立的副本",
                "color": "#27ae60"
            }
        }
