# Sample Input and Output

## Test 1
Puzzle displayed:
```text
7 - 1 = 2
```

Player input:
```text
1 + 1 = 2
```

Expected output:
```text
CORRECT!
Points awarded according to the remaining time.
NEXT LEVEL is enabled.
```

## Test 2
Puzzle displayed:
```text
7 - 1 = 2
```

Player input:
```text
7 - 1 = 2
```

Expected output:
```text
Not quite. Try another equation!
5 points are deducted (minimum score is zero).
```

## Test 3
Player does not answer within 60 seconds.

Expected output:
```text
TIME UP! GAME OVER
Final score is displayed and saved.
```
