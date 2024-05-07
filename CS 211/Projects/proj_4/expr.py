"""Sample solution for calculator project, expr.py"""

# One global environment (scope) for
# the calculator


# One global environment variable
from typing import Dict

ENV: Dict[str, "IntConst"] = {}

class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that
    is not in ENV
    """
    pass

class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")

class IntConst(Expr):
    """Integer constant"""
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"IntConst({self.value})"

    def __eq__(self, other: Expr) -> bool:
        return isinstance(other, Expr) and (self.value == other.value)

    def eval(self) -> "IntConst":
        return self


class BinOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, left: Expr, right: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.left} {self.symbol} {self.right})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.left)}, {repr(self.right)})"

    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Evaluate using the concrete _apply method"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))


class Plus(BinOp):
    """Represents left + right"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol='+')

    def _apply(self, left: int, right: int) -> int:
        return left + right


class Times(BinOp):
    """left * right"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol='*')

    def _apply(self, left_val: int, right_val: int) -> int:
        return left_val * right_val


class Div(BinOp):
    """left / right"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol='%')

    def _apply(self, left: int, right: int) -> int:
        return left % right


class Minus(BinOp):
    """left - right"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol='-')

    def _apply(self, left: int, right: int) -> int:
        return left - right


class UnOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, left: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.symbol} {str(self.left)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left.__repr__()})"

    def _apply(self, left_val: int) -> int:
        """Each concrete UnOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete UnOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Evaluate using the concrete _apply method"""
        left_val = self.left.eval()
        return IntConst(self._apply(left_val.value))

class Neg(UnOp):
    """- left, written as ~ left"""
    def __init__(self, left: Expr):
        super().__init__(left, symbol="~")

    def _apply(self, left: int) -> int:
        return (- left)

class Abs(UnOp):
    """|left|, written as @left"""
    def __init__(self, left: Expr, symbol: str = "?Operation symbol undefined"):
        super().__init__(left, symbol="@")

    def _apply(self, left: int) -> int:
        return abs(left)


class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")

    def assign(self, value: IntConst):
        global ENV
        ENV[self.name] = value


class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""

    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self) -> str:
        return f"({str(self.left)} = {str(self.right)})"

    def __repr__(self) -> str:
        return f"Assign({self.left.__repr__()}, {self.right.__repr()})"
