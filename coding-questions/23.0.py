# How do you find the longest common prefix in a list of strings?

def get_longest_prefix(strs):
    max_size = 0
    base_str = strs[0]

    for i in range(len(base_str)):
        base_char = base_str[i]

        for other_str in strs[1:]:
            if i >= len(other_str) or other_str[i] != base_char:
                return base_str[:max_size]

        max_size += 1

    return base_str[:max_size]


test_cases = [
    # Basic
    (["flower", "flow", "flight"], "fl"),
    # No common prefix
    (["dog", "racecar", "car"], ""),
    # One string
    (["hello"], "hello"),
    # All strings same
    (["test", "test", "test"], "test"),
    # One string is a prefix of another
    (["flower", "flow", "flowing"], "flow"),
    # Empty string
    (["", "abc", "abcd"], ""),
    # Common single character
    (["apple", "ant", "axe"], "a"),
    # Case sensitive
    (["Apple", "Application", "App"], "App"),
    # Completely identical first characters
    (["abc", "abd", "abe"], "ab"),
    # Common prefix with different lengths
    (["interspecies", "interstellar", "interstate"], "inters"),
]

for test_case in test_cases:
    result = get_longest_prefix(test_case[0])
    if result == test_case[1]:
        print(result, test_case[1], "Pass")
    else:
        print(result, test_case[1], "Fail")
