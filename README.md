<!--Please note that this specification is written in PLAIN TEXT as per the Esolang Buffet rules-->

# Rabbitsfoot
> “I think that someone will remember us in another time.”  
> — Sappho of Lesbos (Lobel & Page, Fragment 147)

The Rabbitsfoot language employs the revolutionary new "rabbitsfoot" paradigm, which some liken to the sweet-spot between blockchain, quantum computing, and big data. It also employs the imperative paradigm, which is counter-revolutionary and old.

It was designed by IFcoltransG in 2022 for the first inaugural Esolangs Buffet event on the Unofficial Esolangs Discord Server. (The first inaugural one, not for any other inaugural ones after that.)

Rabbitsfoot's file extension is `.rtf` for programs, or `.rtfm` for Rabbitsfoot library modules.

## Context
For the event, participants had to design an esolang and secretly write a 100 byte sorting program in it. Then competitors had to work out how to create a sorting program in everybody else's languages, only without the size restriction. Three people (other than yours truly) successfully created a sorting algorithm in Rabbitsfoot, out of seven.

## Usage
Run the interpreter on your program from the command line.
```sh
# regular mode
python ./rabbitsfoot.py FILENAME
# verbose mode:
python ./rabbitsfoot.py -v FILENAME
python ./rabbitsfoot.py --verbose FILENAME
```

The interpreter will read from standard input a list of integers.
The integers are separated by whitespace and/or commas, and can have optional `[` and `]` on each end. The list is terminated by a newline.

Output is written like a Python list.

### Example inputs
`1 2 3 4 5`
`[1, 2, 3, 4, 5]`

### Example program
```rabbitsfoot
# cat
,
.
```

### Example output for example inputs into example program
`[1, 2, 3, 4, 5]`

## Execution
The interpreter stores a tuple of W indices called the index tuple, where W is the window size.
The interpreter stores an array of size N called the array, where N is the number of integers in the program input.
The interpreter stores a stack, called the stack.
The interpreter optionally stores a single value, called the cache.

Initially, the array is set to the program input.
Initially, the index tuple is set to (0, ..., 0).
Initially, the stack is empty.

If N is ever 0, the program terminates immediately and outputs its results.

### Input
Whenever input is requested, a list V of size W is pushed onto the stack. The i-th element of V is taken from the array at index j, where j is the i-th element of the index tuple.

For instance, if W=N and the index tuple is (0, 1, ..., N-1), then V has the exact same elements as the array. If W=2, N>0 and the index tuple is (0, 0), then V will be [X, X], where X is the first element of the array.

After the array is initialised, the program input itself is treated as compromised and must no longer be trusted. Subsequent requests for input will treat the array as the only source of truth.

### Basic Loop
The user's program is run, line by line, from the first line, until any control flow statements are reached.

### Stack
The stack can contain integers, lists of integers or strings. However, the stack cannot contain its excitement whenever it sees a bunny rabbit.

If a value is popped from an empty stack, that is undefined behaviour. So don't pop from an empty stack.

### Window size
W is equal to 1 if the program contains no `[`...`]` instructions. Otherwise, it is inferred so that it fits with a `[`...`]` instruction.

## Instructions
All lines must exactly comport to one or more of the following standards.
Except where otherwise noted, commands must take up between 0 and 2 lines (exclusive) with only whitespace left over.

Punctuation that corresponds with endorsed operations have a newline automatically inserted after them, unless they are part of a comment.

### Comments
Any line containing only whitespace is ignored.
Any line beginning with `#` or `REM ` is ignored.
It's nothing personal, and the interpreter ignoring your code doesn't reflect on your value as a person.

### Loop
The `.` command pops a list from top-of-stack, then iterates through each index i in it, storing the i-th value of the list into the array index given by the i-th element of the index tuple. If the value at top-of-stack is not a list, that is undefined behaviour.

(If it helps, imagine the list is a list of rabbits. Then the `.` command pops the list off the stack, and lets all of the rabbits loose, so that they find the value in the index tuple that was at the same position as them, and gnaw at the index in the array given by the value they found, until that array location becomes the value corresponding to that rabbit.)

Then the interpreter increments that the index tuple and then jumps to the start of the program. (Implementations must preserve the stack.)

All programs must contain at least one `.`. Programs that contain only comments are undefined behaviour.

To increment the index tuple, add one to its rightmost value.
Then until no elements of the tuple equal N, pick any element that equals N, set it to exactly 0, then add one to the element to its left in the tuple. If no such element exists, the program terminates immediately and outputs its results.

### Literal
The `[`...`]` command pushes a given list of integers onto the stack. Between the `[` and the `]` are a sequence with length W of whitespace separated integers.

Patent pending.

### Zilch
The `0` command pushes a 0 to the stack.

If both N and W equal 0, or if the index tuple is (0, ..., 0), then it is undefined behaviour to run `0`. That would be too many zeros. It's safer this way.

### Memory
The first time `|` is executed, it peeks at the top value of the stack and saves it to the cache. Any subsequent time it is run, it pops the top-of-stack and pushes a copy of the value saved in the cache.

It is undefined behaviour for `|` to be executed when the stack is empty.

### Addition
The `+` command pops two integers or two lists of integers from the stack, adds them (elementwise in the case of two lists), then pushes the result.

Implementations are free to add the values in any order they choose. However, they should be forewarned that addition is commutative, meaning the implementator's choice is just as meaningless as every other choice they make in their lives.

### Reverse Factorisation
The `*` pops integers or two lists of integers from the stack, and pushes their product or elementwise product, respectively.

Again, implementations may left-multiply or right-multiply. It's their prerogative. Commutativity of multiplication is left as an exercise to the reader.

### Bounce
When the `!` command is run, if the value at top-of-stack is an integer, the interpreter jumps to the next `!`. Otherwise, if the value at top-of-stack is a list or a string, the command is treated as a no-op. It is undefined behaviour for a program to have an odd number of `!`.

The value at top-of-stack is not popped. It is undefined behaviour to run `!` if the stack is empty, or for the interpreter to try to jump to the next `!` when there are not more left.

### Compare
The `-` command pops two integers from the stack and pushes the max of the two integes, then pushes the negative of the min of the two integers. If the first value popped is a list rather than an integer, no second value is popped. Instead, every integer in the list is replaced with 1, 0 or -1 corresponding to if it is positive, zero, or negative, respectively, then the resulting list is pushed again.

Maximum picks closest to ∞ and minimum picks closest to 0.

### Factorial
The `?` command performs a factorial operation on the integer at top-of-stack. If you are wondering why the symbol isn't `!`, it's because that symbol was taken.

It is undefined behaviour for `?` to be run on a string or list, or for the integer to be negative.

### Pack
The `$` command checks if there are exactly W integers on the stack. If so, it pops those integers and pushes a list containing them. If not, that is undefined behaviour.

You can imagine it like having a stack filled with rabbits at nighttime, then when day breaks the rabbits go back to the warren (as long as there are exactly the right amount of rabbits) and the warren is pushed to the stack. It's like that.

### Division
The `/` command elementwise divides the list at top-of-stack by W, rounding down.

If the value at top-of-stack is a string or an integer rather than a list of integers, that is undefined behaviour.

### Input Request
To request input data to process, the programmer needs only leave a line with a lone `,` in it, which strikes me as awfully convenient. Don't you think?

### Eval
The `^` command pops a string from the stack, splits it by newlines, then runs each line of code sequentially. It is illegal for the string to contain a `.` instruction (though it may contain further `^` instructions).

Trying to execute an integer or a list is undefined behaviour.

Imagine that your string is actually a rabbit. Then running `^` causes that rabbit to be popped from the stack and executed. Poor rabbit.

### Exec
The `@` command executes the commands from the first line of the source code. Note that many instructions may be executed in this way if they didn't have newlines following them pre-endorsement.

It is undefined behaviour for `@` to be placed on the first line of the source code.

### Transmogrification
The `~` command pops W lists from the stack and assembles a 2-d grid of integers, where if an integer is at position x of the y-th popped list, it is put at position (x, y-1). Then for each x coordinate χ starting from 0, the interpreter pushes a list of every integer on a grid point that satisfies x=χ, starting from y=0.

It may help understanding if you imagine that there are rabbits arranged in a little grid. (The rabbits are the contents of the popped lists.) Then the rabbits do a dance, and end up in the positions described above. Then the lines of rabbits are pushed onto the stack.

If any value pushed is not a list of integers, that is undefined behaviour.

### Random
The `%` command pops an integer or a list. If an integer is popped, a uniform random integer between 0 and that integer (inclusive) is pushed. If a list is popped, it is pushed shuffled.

Should a negative integer be popped this way, the behaviour is undefined.

### Increment
The `<`...`>` command increments a series of indices. Between the `<` and `>` are a sequence of whitespace-separated non-negative integers. For each number from left to right, the corresponding array element at that index is increased by 1.

### Semantic comments
The `=` command is a little like a macro. It inserts the text of the first comment in the source code into the program at the position of the `=`, uncommented.

It is undefined behaviour for `=` to come before the first comment in the program.

Fun animal fact: the `=` sign looks like two rabbit ears!

## Endorsements and Awards
The following instructions are certified and endorsed by the Rabbitsfoot Lucky-Paw Seal of Approval (RLPoA):
### Arithmetic operators
These symbols deserve respect for their longstanding contribution to the buttons on calculators.
- `+`
- `*`
- `/`
### Other brainfuck symbols
These symbols have contributed meaningfully to the history of esolangs.
- `,`
- `.`
- `[`...`]`
- `<`...`>`
### Who knows really
These symbols are financial benefactors of the Rabbitsfoot programming language.
- `~`
- `|`
- `!`
- `?`

The symbol `-` has received an *honorary* endorsement in appreciation of its substantial contributions to `[`...`]` and to arithmetic. Due to a technicality, `-` alas cannot receive implicit newline privileges, but was awarded a small cash koha instead.

## Rabbitsfoot library modules
Files with the `.rtfm` extension are treated as Rabbitsfoot library modules rather than programs. Rabbitsfoot library modules are executed as if they were programs.
