# PyProver
#### PyProver is a simple utility that allows you to check the truth of mathematical expressions with the possibility of substituting variables on specified intervals.
This can help you in case you need to quickly check the equality of some mathematical expressions or find a counter-example by brute-force method.

## Usage
1. Install and run the program (see Installation);
2. Specify the command in the following format:
* First comes the math expression itself, written using ASCII characters.
* If your expression contains variables, you must specify their value or the interval for enumerating them. To do this, use "$" to separate the expression and the variable values. after the dollar sign, through a space, specify the values in the following form: "`{variable name}@{start};{stop}`" to specify an interval, and "`{variable name}={value}`" to specify a constant value.
* Spaces in expressions are completely optional. You can use them as decoration.
3. After entering, press Enter and wait for the result. If the entered expression is true, you will see "True" on the screen, if not, you will see "False", as well as an indication of the variable values for which the expression was false.
**Also See. "Examples" for sample expressions.**

## Examples
Expression:
```
2^3 = 8
```
Result:
```
True
```

---

Expression:
```
a+2 = 2+a $ a@1;100
```
_"Check if `a+2 = 2+a`, where `a` is a variable in range from 1 to 100"_

Result:
```
True
```
_Because `a+2` and `2+a` are the same expressions, so they are equal._

---

Expression:
```
a*a = a^2 $ a@-10;10
```
_Check are `a*a` and `a^2` the same, if a is a variable in range from -10 to 10_

Result:
```
True
```

---

Expression:
```
(a+b)^2 = a^2 + 2ab + b^2 $ a@1;100 b@1;100
```

_**Squared sum** formula, where `a`  is between 1 and 100, and `b` is between 1 and 100_

Result:
```
True
```

_Because this formula is true._

---

Expression:
```
a^2 + b^2 != c^2 $ a@1;10 b@1;10 c@1;10
```

_Anti-Pythagorean triple, so it will return false, when such triple will be found._

Result:
```
False (a=3; b=4; c=5)
```

_One of such triple._

## Installation
You can clone the repository and run "main.py", or use one of the files from the "Release" tab.
