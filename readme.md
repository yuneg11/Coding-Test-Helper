# Coding Test Helper

Code Test Helper is the tool to help online coding test.
Some sites uses an input file and an output file to evaluate the code.
This tool converts that io-type into the function-type.

For example (The sum of input numbers):

Converts

```text
# input      # output
5            15
1 2 3 4 5
```

```python
n = int(input())
numbers = list(map(int, input().split()))
print(sum(numbers))
```

into

```text
# input                      # output
n = 5                        return 15
numbers = [1, 2, 3, 4, 5]
```

```python
def solution(n, numbers):
    return sum(numbers)
```

## Getting Started

```bash
git clone https://github.com/yuneg11/CodingTestHelper.git
cd CodingTestHelper
```

## Usage

Example problem: [CodeUp:4654](https://codeup.kr/problem.php?id=4654)

### Get the skeleton code

```bash
python3 main.py {site}:{problem-number}

# Example
python3 main.py codeup:4654
```

If you want the function-type skeleton code, use "solution" function.

```python
# n: <class 'int'>
# heights: typing.List[int]
# return: typing.List[int]
def solution(n, heights):
    answer = []
    return answer
```

If you want the io-type skeleton code, use "solution_raw" function. \
You should handle the input and the output process as before.

```python
# file: <class '_io.TextIOWrapper'>
# return: <class 'str'>
def solution_raw(file):
    input_lines = file.readlines()
    answer = ""
    return answer
```

### Test the solution code

```bash
python3 main.py {site}:{problem-number} -s {solution-file-path}

# Example
python3 main.py codeup:4654 -s solution/codeup4654.py

# If you want to save the solution code for submit
python3 main.py codeup:4654 -s solution/codeup4654.py -o submit.py
```

If you pass all the test cases, you can submit the generated submit code.

## Add problems

For now, the only supported site is [CodeUp](https://codeup.kr) \
To add more problems, follow steps below.

### 1. Copy the template folder

Copy `data/codeup/template` folder to `data/codeup/id{problem-num}`. \
Just copy and paste the folder or use the below command.

```bash
cp -r data/codeup/template data/codeup/id{problem-num}

# Example (Problem num: 1234)
cp -r data/codeup/template data/codeup/id1234
```

### 2. Modify `problem.py` file

If you want to provide function-type skeleton code, you should modify three functions. \
Even if not, users can still use io-type skeleton code.

#### 2.1. Modify `read_input` function

The `read_input` function should receive only `file` as an argument and return arguments for `solution` function.

```python
def read_input(file: TextIOWrapper) -> Tuple[int, int]:
    # You can use 'input()' to get inputs
    input = lambda: file.readline().rstrip()

    solution_arg1 = int(input())
    solution_arg2 = int(input())
    return solution_arg1, solution_arg2
```

#### 2.2. Modify `solution` function

The `solution` function should receive arguments that `read_input` returns and return the answer. \
You only need to write the skeleton of it.

```python
def solution(arg1: int, arg2: int) -> int:
    # You should provide skeleton code of solution
    answer = 0
    return answer
```

#### 2.3. Modify `print_output` function

The `print_output` function should receive the answer that `solution` function returns and return the string version of it.

```python
def print_output(output: int) -> str:
    # You should convert output object to string
    return str(output)
```

### 3. Add sample cases and test cases

The sample case is that the provided test case for example, and the test case is that the hidden test case for evaluating the score. \
If you don't have that cases, just delete the `sample` folder or the `test` folder.

The name of the file should follow rules below.

```text
# input
{case-number}i.txt

# output
{case-number}o.txt
```

The 0s in front of the number are just placeholders. \
You can ignore it.

For example,

```text
# Test case #1
1i.txt = 01i.txt = 001i.txt
1o.txt = 01o.txt = 001o.txt
```
