import pathlib
import itertools
import sys

def cmp(a, b):
    # taken from https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
    return (a > b) - (a < b)

def flip(x):
    # transposes
    return [list(row) for row in zip(*x, strict=True)]

def factorial(n):
    for i in range(1, n):
        n *= i
    return max(n, 1)

def is_comment(line):
    return line.startswith("#") or line.startswith("REM ")

# read command line arguments
if len(sys.argv) < 2:
    print("Please pass filename of code", file=sys.stderr)
    sys.exit(1)
verbose_mode = "-v" in sys.argv or "--verbose" in sys.argv
filename = sys.argv[-1]
code = pathlib.Path(filename).read_text()

if verbose_mode:
    # enable logging to stderr
    log = lambda *a, **k: print(*a, **k, file=sys.stderr)
else:
    # disable logging
    log = lambda *a, **k: None

# read list of integers from stdin
data = [
    int(num)
    for num
    in input()
        .replace(",", " ")
        .strip("[ ]").split()
]

if not code.split("\n"):
    raise SyntaxError("Code has no lines")

# preprocessing
# replace all @ macros with the first line of the program
first_line = code.split("\n")[0]
if "@" in first_line:
    raise SyntaxError("`@` on first line of program")
code = code.replace("@", first_line)
# find first comment for the = command
for line in code.split("\n"):
    if is_comment(line):
        first_comment = line.lstrip("REM ").lstrip("#")
        break
    if "=" in line:
        raise SyntaxError("`=` before first comment")
else:
    first_comment = ""
# remove comments
code = "\n".join(
    line
    for line
    in code.split("\n")
    if not is_comment(line)
)
# insert macros from first comment
if "=" in code:
    code = code.replace("=", first_comment)
# insert newlines after endorsed commands
endorsed = {"+", "*", "/", "~", "|", ",", ".","]", ">", "!", "?"}
for endorsement in endorsed:
    # insert newlines automatically
    code = code.replace(endorsement, endorsement + "\n")

# get window size
window_size = 1
for line in code.split("\n"):
    if line.startswith("[") and line.endswith("]"):
        # found a [...] line
        # so can infer size of window
        window_size = len(line.strip("[ ]").split())
        break
# otherwise default to 1
log(f"{window_size = }")

stack = []
cache = None

ranges = [range(len(data)) for _ in range(window_size)]
for indices in itertools.product(*ranges):
    log(f"Iterating with {indices = }")
    for line in code.split("\n"):
        line = line.strip()
        log(f"  Runnning line: {line}")
        match line:
          case ",":
            # get input from array
            stack.append([data[i] for i in indices])
          case "*":
              # multiply
              top = stack.pop()
              second = stack.pop()
              match (top, second):
                case (int(), int()):
                    stack.append(top * second)
                case (list(), list()):
                    product = [x*y for x,y in zip(top, second, strict=True)]
                    stack.append(product)
                case _:
                    raise TypeError("Mixed-type multiplication is not supported")
          case "+":
              # add
              top = stack.pop()
              second = stack.pop()
              match (top, second):
                case (int(), int()):
                    stack.append(top + second)
                case (list(), list()):
                    summation = [x+y for x,y in zip(top, second, strict=True)]
                    stack.append(summation)
                case _:
                    raise TypeError("Mixed-type addition is not supported")
          case "?":
              # factorial
              top = stack.pop()
              if isinstance(top, int):
                  if top < 0:
                      raise ValueError("Attempted factorial on negative number")
                  product = factorial(top)
                  stack.append(product)
              else:
                  raise TypeError("Factorial on something other than an integer")
          case "-":
              # get max/min of two ints or elementwise get sign
              top = stack.pop()
              if isinstance(top, int):
                  second = stack.pop()
                  stack.append(max(top, second))
                  stack.append(-min(top, second), key=abs)
              else:
                  sign = [cmp(x, 0) for x in top]
                  stack.append(sign)
          case "|":
              # save/load memory
              if cache is None:
                  cache = stack[-1]
                  log(f" -cache set to {cache}")
              else:
                  stack.pop()
                  stack.append(cache)
          case "~":
              # flip about main diagonal
              rows = [stack.pop() for col in range(window_size)]
              cols = flip(rows)
              cols.reverse()
              stack.extend(cols)
          case "0":
              # push 0
              if indices == (0,) * window_size:
                  raise ValueError("Tried to execute `0` when index tuple was all zeros")
              elif len(data) == 0 and window_size == 0:
                  raise ValueError("Tried to execute `0` when window size and input size were both 0. Very dangerous!")
              else:
                  stack.append(0)
          case "$":
              # pack integers into list and push
              integers = []
              while stack:
                  next_integer = stack.pop()
                  if not isinstance(next_integer, int):
                      raise TypeError("Tried to pack non-integer into list of integers")
                  integers.append(next_integer)
              if len(integers) != window_size:
                  raise ValueError("Wrong number of popped integers")
              stack.append(integers)
          case "!":
              # conditional jump
              basic_count = code.replace(" ", "").replace("\t", "").count("\n!\n")
              if code.startswith("!") != code.endswith("!"):
                  basic_count += 1
              if basic_count % 2 == 1:
                  raise SyntaxError("Odd number of `!`")
              if isinstance(stack[-1], int):
                  # this code path shouldn't happen
                  raise NotImplementedError()
          case "^":
              # eval
              eval_code = stack.pop()
              if isinstance(code, str):
                  for eval_line in eval_code.split("\n"):
                      if eval_line == "":
                          continue
                      if eval_line.strip() == ".":
                          raise ValueError("Tried to execute a `.` within a `^` evaluation")
                      # this code path shouldn't happen
                      raise NotImplementedError()
              else:
                  raise TypeError("Tried to execute something other than a string")
          case "/":
              # divide
              top = stack.pop()
              quotient = [num // window_size for num in top]
              stack.append(quotient)
          case "%":
              # randomise
              top = stack.pop()
              match top:
                case int():
                    if top < 0:
                        raise ValueError("Random integer from empty set")
                    stack.append(random.randrange(0, top + 1))
                case list():
                    top = list(top)
                    random.shuffle(top)
                    stack.append(top)
          case x if x.startswith("[") and x.endswith("]"):
              # push literal
              values = [
                  int(num)
                  for num
                  in x.strip("[ ]").split()
              ]
              if len(values) != window_size:
                  raise SyntaxError("Literal does not match window size")
              stack.append(values)
          case x if x.startswith("<") and x.endswith(">"):
              # increment indices of array
              if "-" in x:
                  raise ValueError("Negative integer in indices to increment")
              values = [int(num) for num in x.strip("< >").split()]
              for index in values:
                  data[index] += 1
          case ".":
              # end program
              break
          #case ":":
          #    # deprecated duplicate
          #    top = stack.pop()
          #    stack.append(top)
          #    stack.append(top)
          #case ";":
          #    # deprecated swap
          #    top = stack.pop()
          #    second = stack.pop()
          #    stack.append(top)
          #    stack.append(second)
          case "":
              # empty line
              continue
          case _:
              raise SyntaxError(f"Got malformed line: {line}")
        log(f"  {stack = } <-TOS")
    else:
        # program didn't end with "."
        raise SyntaxError("Program does not contain a `.` instruction")
    # this iteration, we replace all chosen values
    # with new values calculated by the program
    new_values = stack.pop()
    log(f"Replacing values at indices {indices} with {new_values}")
    for index, value in zip(indices, new_values, strict=True):
        data[index] = value
    log(f"{cache = }")
    log(f"{data = }")
    log()

print(data)
log()
log("---")
log("Program terminated successfully.")
