import ast


class BugPatternVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def add_issue(self, node, code, severity, message, suggestion):
        self.issues.append({
            "code": code,
            "severity": severity,
            "message": message,
            "suggestion": suggestion,
            "line": getattr(node, "lineno", None)
        })

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            if (
                isinstance(node.right, ast.Constant)
                and isinstance(node.right.value, (int, float))
                and not isinstance(node.right.value, bool)
                and node.right.value == 0
            ):
                self.add_issue(
                    node,
                    "DIV001",
                    "error",
                    "Division or modulo by zero detected.",
                    "Check that the denominator is not zero."
                )

        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                self.add_issue(
                    node,
                    "SEC001",
                    "warning",
                    "Use of eval() can execute untrusted code.",
                    "Avoid eval(); use safer alternatives such as ast.literal_eval() when appropriate."
                )

            elif node.func.id == "exec":
                self.add_issue(
                    node,
                    "SEC002",
                    "warning",
                    "Use of exec() can execute arbitrary code.",
                    "Avoid exec() and use explicit functions or safer alternatives."
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._check_mutable_defaults(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_mutable_defaults(node)
        self.generic_visit(node)

    def _check_mutable_defaults(self, node):
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.add_issue(
                    default,
                    "BUG001",
                    "warning",
                    f"Mutable default argument in function '{node.name}'.",
                    "Use None as the default and create a new collection inside the function."
                )

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.add_issue(
                node,
                "BUG002",
                "warning",
                "Bare except clause catches all exceptions.",
                "Catch only the specific exception types you expect."
            )

        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.add_issue(
                node,
                "BUG003",
                "warning",
                "Exception handler silently ignores errors.",
                "Handle the exception or log useful information."
            )

        self.generic_visit(node)


def analyze_bug_patterns(code: str) -> dict:
    """
    Detect common Python bug patterns without executing submitted code.
    """

    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, TypeError):
        return {
            "status": "skipped",
            "issues": []
        }

    visitor = BugPatternVisitor()
    visitor.visit(tree)

    return {
        "status": "completed",
        "total_issues": len(visitor.issues),
        "issues": visitor.issues
    }
