# Pyscheme

A Scheme interpreter written in Python.

## Running the interpreter
### Normal mode

```
python pyscheme.py
```
### Debugging mode
Uses normal Python handling of exceptions

```
python pyscheme.py debug
```

## Meta-Options
### Pretty-print
To turn pretty-print of numbers on and off, set the environment variable
```
pretty-print
```

Example:

```
pyscheme > (define pretty-print #t)
okay
pyscheme > 1000
1,000
```
