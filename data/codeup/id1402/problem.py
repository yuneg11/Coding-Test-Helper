"""
Problem URL: https://codeup.kr/problem.php?id=1402
"""


from io import TextIOWrapper
from typing import Tuple, List


def read_input(file: TextIOWrapper) -> Tuple[int, List[int]]:
    input = lambda: file.readline().rstrip()

    n = int(input())
    numbers = list(map(int, input().split()))
    return n, numbers


def solution(n: int, numbers: List[int]) -> List[int]:
    answer = []
    return answer


def print_output(output: List[int]) -> str:
    return " ".join(map(str, output))
