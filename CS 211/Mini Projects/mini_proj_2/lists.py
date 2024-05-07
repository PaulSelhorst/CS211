def all_same(a_list:list)->bool:
    """A function that determines whether all the elements in a list are the same."""
    return len(set(a_list)) == 1 or len(a_list) == 0

def dedup(l: list) -> list:
    for i in l:
        if l.count(i) > 1:
            l.remove(i)
    return l

def max_run(a_list: list) -> list:
    if not a_list:
        return 0
    
    longest_run = 1
    current_run = 1
    list_of_matches = []
    current_matches = [a_list[0]]
    
    for i in range(1, len(a_list)):
        if a_list[i] == a_list[i-1]:
            current_run += 1
            current_matches.append(a_list[i])
        else:
            longest_run = max(longest_run, current_run)
            list_of_matches.append(current_matches)
            current_run = 1
            current_matches = [a_list[i]]
    
    # Check at the end of the loop
    longest_run = max(longest_run, current_run)
    list_of_matches.append(current_matches)
    
    return longest_run, list_of_matches