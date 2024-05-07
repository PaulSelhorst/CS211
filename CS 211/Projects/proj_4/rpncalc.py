"""Reverse Polish calculator.

This RPN calculator creates an expression tree from
the input.  It prints the expression in algebraic
notation and then prints the result of evaluating it.
"""

import expr
import io

def is_binop(op:str)-> bool:
    if op in "+-*/":
        return True
    return False
def is_unop(op:str)-> bool:
    if op in "~@":
        return True
    return False

def is_var(op:str)-> bool:
    if is_binop(op) or is_unop(op) or not op[0].isalpha():
        return False
    return True

def binop_class(op:str)-> "expr.BinOp":
    match op:
        case '+':
            return expr.Plus
        case '-':
            return expr.Minus
        case '*':
            return expr.Times
        case '/':
            return expr.Div
        case _:
            raise KeyError(f"Unknown binary operator {op}")
        
def unop_class(op:str)-> "expr.Unop":
    match op:
        case '~':
            return expr.Neg
        case '@':
            return expr.Abs
        case _:
            raise KeyError(f"Unknown binary operator {op}")


def calc(text: str):
    """Read and evaluate a single line formula."""
    stack = rpn_parse(text)
    if len(stack) == 0:
        print("(No expression)")
    else:
        for exp in stack:
            print(f"{exp} => {exp.eval()}")

def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")


def rpn_parse(text: str) -> list[expr.Expr]:
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input 
    """
    try:
        to_parse = text.split()
        stack = []
        for op in to_parse:
            if op.isdigit():
                stack.append(expr.IntConst(int(op)))
            elif is_binop(op):
                right = stack.pop()
                left = stack.pop()
                stack.append(binop_class(op)(left, right))
            elif is_unop(op):
                operand = stack.pop()
                stack.append(unop_class(op)(operand))
            elif is_var(op):
                stack.append(expr.Var(op))
            elif op == "=":
                right = stack.pop()
                left = stack.pop()
                stack.append(expr.Assign(right, left))
            else:
                raise ValueError(f"Unknown token {op}")
    except IndexError:
        raise ValueError("Imbalanced RPN expression, missing operand at")
    return stack


if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()