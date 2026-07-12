The difference is that `nums` and `nums[:]` are **different lists**.

### Case 1: Iterate over the original list (unsafe)

```python
nums = [1, 2, 3, 4]

for n in nums:
    if n % 2 == 0:
        nums.remove(n)
```

The loop is reading from the **same list** that you're modifying.

Example with a bigger list:

```python
nums = [2, 4, 6, 8]

for n in nums:
    nums.remove(n)

print(nums)    # [4, 8]
```

Why?

```text
Start: [2, 4, 6, 8]
       ^

Remove 2
List becomes: [4, 6, 8]
Iterator moves to index 1 → 6
             ↑
4 is skipped!
```

Removing an element shifts all later elements left, but the iterator's index keeps advancing, causing elements to be skipped.

---

### Case 2: Iterate over a copy (safe)

```python
nums = [2, 4, 6, 8]

for n in nums[:]:
    nums.remove(n)

print(nums)    # []
```

`nums[:]` creates a **shallow copy**:

```text
Iterator → [2, 4, 6, 8]   (copy)
Original → [2, 4, 6, 8]
```

The iterator walks over the **copy**, while removals happen in the **original** list. Since the list being iterated over never changes, nothing gets skipped.

### Rule of thumb

* `for x in nums:` → ❌ Don't modify `nums` while iterating.
* `for x in nums[:]:` → ✅ Safe, because you iterate over a copy.
* Even better, build a new list when appropriate:

```python
nums = [n for n in nums if n % 2 != 0]
```

----
### Can iter() solve this problem?

**No.** Using `iter()` alone does **not** solve the problem.

```python
nums = [2, 4, 6, 8]
it = iter(nums)

for x in it:
    nums.remove(x)

print(nums)   # [4, 8]
```

This has the **same issue** because `iter(nums)` creates an iterator over the **original list**, not a copy.

If you want to use `iter()`, use it on a copy:

```python
for x in iter(nums[:]):
    nums.remove(x)
```

or simply:

```python
for x in nums[:]:
    nums.remove(x)
```

which is equivalent and more idiomatic.

**Rule:** `iter()` creates an iterator; it **does not** make a copy of the container. Modifying the underlying list while iterating can still cause elements to be skipped.
