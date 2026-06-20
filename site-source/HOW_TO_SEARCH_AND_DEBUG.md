# How to Search and Debug

Engineering is not knowing everything. Engineering is learning how to find, test, and verify.

## Search pattern

Use this pattern:

```text
<tool/language> + <exact error message> + <what you were trying to do>
```

Examples:

```text
python address already in use port 8000
fastapi post json body example
git rejected non fast forward
localhost not accessible from phone same wifi
sqlite database file not found python
```

## Debugging report format

For every real problem, write:

```text
Problem:
Evidence:
What I searched:
Reference I used:
What I tried:
Root cause:
Fix:
How to prevent next time:
```

## Important habit

Do not randomly change many things at once. Change one thing, test, then document the result.
