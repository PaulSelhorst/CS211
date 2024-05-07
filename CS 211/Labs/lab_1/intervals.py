class Interval:
    """An interval [m..n] represents the set of integers from m to n."""
    def __init__(self, low:int, high:int):
        self.low = low
        self.high = high

        if low > high:
            raise ValueError("The low value of the interval cannot be higher than the high value.")
        
    def contains(self, i:int) -> bool:
        """Integer i is within the closed interval"""
        return i in range(self.low, self.high + 1)
    
    def overlaps(self, other:"Interval") -> bool:
        """i.overlaps(j) if i and j have some elements in common."""
        return self.contains(other.low) or self.contains(other.high) or other.contains(self.low) or other.contains(self.high)
    
    def __eq__(self, other:"Interval") -> bool:
        """Intervals are equal if they have the same low and high bounds."""
        return self.low == other.low and self.high == other.high
    
    def join(self, other:"Interval") -> "Interval":
        """Create a new Interval that contains the union of elements in self and other.
        Precondition: self and other must overlap"""
        if not self.overlaps(other):
            raise ValueError("Intervals must overlap to be joined.")
        return Interval(min(self.low, other.low), max(self.high, other.high))
    
    def __str__(self)->str:
        """Changes the string returned when the print function is called so it returns the
        low and high values of the interval in the interval class object."""
        return f"[{self.low}..{self.high}]"

    def __repr__(self)->str:
        """Provide the string we would see when evaluating the Interval class object in the Python console."""
        return f"Interval({self.low}, {self.high})"
    

interval1 = Interval(1, 5)
interval2 = Interval(3, 7)

joined_interval = interval1.join(interval2)
print(joined_interval)