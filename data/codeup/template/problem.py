"""
Problem URL: {Please provide the problem url}
"""


from io import TextIOWrapper
from typing import Tuple


def read_input(file: TextIOWrapper) -> Tuple[int, int]:
    # You can use 'input()' to get inputs
    input = lambda: file.readline().rstrip()

    solution_arg1 = int(input())
    solution_arg2 = int(input())
    return solution_arg1, solution_arg2


def solution(arg1: int, arg2: int) -> int:
    return 0


def print_output(output: int) -> str:
    # You should convert output object to string
    return str(output)
