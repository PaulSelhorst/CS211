class Solution:
    def removeStars(self, s: str) -> str:
        stack = []
        for i in len(str):
            if s[i] == "*":
                stack.pop()
            else:
                stack.append(s[i])
        return "".join(stack)
        
class Add:
    def __init__(self, x, y, z):
        self.sum = x+y+z

# x = Add(1, 2, 3)
# y = x.sum
# x.sum = y + 1
# print(x.sum)

class A:
    def test(self):
        print("A.test")
class B(A):
    def test(self):
        print("B.test")
        super().test()
a_B = B()
a_B.test()

def count_nodes(expr):
    """
    Count the number of nodes in the expression.
    
    Args:
        expr: An expression object.
        
    Returns:
        int: The number of nodes in the expression.
    """
    if expr is None:
        return 0
    else:
        count = 1
        for arg in expr.args:
            count += count_nodes(arg)
        return count