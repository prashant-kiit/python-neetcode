# How do you find the longest common prefix in a list of strings?

def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
    return prefix

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
    result = longest_common_prefix(test_case[0])
    if result == test_case[1]:
        print(result, test_case[1], "Pass")
    else:
        print(result, test_case[1], "Fail")