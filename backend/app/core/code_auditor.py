import ast
import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class AuditIssue:
    line: int
    column: int
    severity: str
    code: str
    message: str
    suggestion: str


class CodeAuditor:
    def __init__(self):
        self.issues = []
        
    def audit(self, code: str, language: str = "python") -> Dict[str, Any]:
        self.issues = []
        
        if language in ["python", "py"]:
            self._audit_python(code)
        elif language in ["c", "cpp", "c++"]:
            self._audit_c(code)
            
        return {
            "issues": self.issues,
            "summary": {
                "total": len(self.issues),
                "errors": sum(1 for i in self.issues if i.severity == "error"),
                "warnings": sum(1 for i in self.issues if i.severity == "warning"),
                "info": sum(1 for i in self.issues if i.severity == "info")
            }
        }
    
    def _audit_python(self, code: str):
        lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
            self._check_syntax_ast(tree, lines)
        except SyntaxError as e:
            self.issues.append(AuditIssue(
                line=e.lineno or 1,
                column=e.offset or 0,
                severity="error",
                code="SYNTAX_ERROR",
                message=f"语法错误: {e.msg}",
                suggestion="请检查语法是否正确"
            ))
            return
        
        self._check_common_python_issues(lines)
    
    def _check_syntax_ast(self, tree, lines):
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                self._check_assign(node, lines)
            elif isinstance(node, ast.Name):
                self._check_name(node, lines)
            elif isinstance(node, ast.Call):
                self._check_call(node, lines)
            elif isinstance(node, ast.If):
                self._check_if(node, lines)
            elif isinstance(node, ast.For):
                self._check_for(node, lines)
            elif isinstance(node, ast.While):
                self._check_while(node, lines)
    
    def _check_assign(self, node, lines):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if var_name.startswith('_'):
                    self.issues.append(AuditIssue(
                        line=target.lineno,
                        column=target.col_offset,
                        severity="info",
                        code="UNDERSCORE_PREFIX",
                        message=f"变量名 '{var_name}' 以下划线开头",
                        suggestion="以下划线开头的变量通常表示内部使用"
                    ))
    
    def _check_name(self, node, lines):
        pass
    
    def _check_call(self, node, lines):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            if len(node.args) == 0:
                self.issues.append(AuditIssue(
                    line=node.lineno,
                    column=node.col_offset,
                    severity="warning",
                    code="EMPTY_PRINT",
                    message="print() 调用没有参数",
                    suggestion="请添加要打印的内容"
                ))
    
    def _check_if(self, node, lines):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                self.issues.append(AuditIssue(
                    line=node.test.lineno,
                    column=node.test.col_offset,
                    severity="warning",
                    code="ALWAYS_TRUE",
                    message="条件永远为真",
                    suggestion="检查条件逻辑是否正确"
                ))
            elif node.test.value is False:
                self.issues.append(AuditIssue(
                    line=node.test.lineno,
                    column=node.test.col_offset,
                    severity="warning",
                    code="ALWAYS_FALSE",
                    message="条件永远为假",
                    suggestion="检查条件逻辑是否正确"
                ))
    
    def _check_for(self, node, lines):
        if isinstance(node.iter, ast.List) and len(node.iter.elts) == 0:
            self.issues.append(AuditIssue(
                line=node.iter.lineno,
                column=node.iter.col_offset,
                severity="warning",
                code="EMPTY_LOOP",
                message="循环遍历空列表",
                suggestion="确认列表是否应该有元素"
            ))
    
    def _check_while(self, node, lines):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                self.issues.append(AuditIssue(
                    line=node.test.lineno,
                    column=node.test.col_offset,
                    severity="warning",
                    code="INFINITE_LOOP",
                    message="无限循环（while True）",
                    suggestion="确保循环内部有 break 语句"
                ))
    
    def _check_common_python_issues(self, lines):
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if '=' in stripped and '==' not in stripped:
                if stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('while '):
                    if re.search(r'\bif\s+[\w\s]*=\s*', stripped):
                        self.issues.append(AuditIssue(
                            line=line_num,
                            column=0,
                            severity="error",
                            code="ASSIGN_IN_CONDITION",
                            message="在条件语句中使用赋值（=）而不是比较（==）",
                            suggestion="将 = 改为 == 以进行比较"
                        ))
            
            if 'import ' in line and 'from ' not in line:
                if line_num > 10:
                    self.issues.append(AuditIssue(
                        line=line_num,
                        column=0,
                        severity="info",
                        code="LATE_IMPORT",
                        message="import 语句应放在文件开头",
                        suggestion="将 import 语句移到文件顶部"
                    ))
            
            if len(line) > 120:
                self.issues.append(AuditIssue(
                    line=line_num,
                    column=120,
                    severity="warning",
                    code="LINE_TOO_LONG",
                    message=f"行长度超过120字符（当前{len(line)}字符）",
                    suggestion="考虑拆分长行以提高可读性"
                ))
            
            if 'pass' in stripped and stripped == 'pass':
                self.issues.append(AuditIssue(
                    line=line_num,
                    column=0,
                    severity="info",
                    code="EMPTY_BLOCK",
                    message="空代码块（pass）",
                    suggestion="添加实际代码或考虑移除"
                ))
    
    def _audit_c(self, code: str):
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.endswith('{') and not stripped.startswith('#'):
                if 'if' in stripped or 'else' in stripped or 'for' in stripped or 'while' in stripped:
                    self.issues.append(AuditIssue(
                        line=line_num,
                        column=0,
                        severity="info",
                        code="BRACE_STYLE",
                        message="花括号与语句同行",
                        suggestion="建议将左花括号放在下一行"
                    ))
            
            if '=' in stripped and '==' not in stripped:
                if stripped.startswith('if ') or stripped.startswith('else if ') or stripped.startswith('while '):
                    if re.search(r'\bif\s+[\w\s]*=\s*', stripped):
                        self.issues.append(AuditIssue(
                            line=line_num,
                            column=0,
                            severity="error",
                            code="ASSIGN_IN_CONDITION",
                            message="在条件语句中使用赋值（=）而不是比较（==）",
                            suggestion="将 = 改为 == 以进行比较"
                        ))
            
            if len(line) > 120:
                self.issues.append(AuditIssue(
                    line=line_num,
                    column=120,
                    severity="warning",
                    code="LINE_TOO_LONG",
                    message=f"行长度超过120字符（当前{len(line)}字符）",
                    suggestion="考虑拆分长行以提高可读性"
                ))
            
            if '//' in line and not stripped.startswith('//'):
                self.issues.append(AuditIssue(
                    line=line_num,
                    column=0,
                    severity="warning",
                    code="INLINE_COMMENT",
                    message="行内注释可能影响可读性",
                    suggestion="考虑将注释放在单独一行"
                ))
            
            if stripped.startswith('// TODO') or stripped.startswith('// FIXME'):
                self.issues.append(AuditIssue(
                    line=line_num,
                    column=0,
                    severity="info",
                    code="TODO_COMMENT",
                    message=f"待办事项注释: {stripped}",
                    suggestion="请处理此待办事项"
                ))
