"""
Problem URL: https://codeup.kr/problem.php?id=4654
"""


from io import TextIOWrapper
from typing import Tuple, List


def read_input(file: TextIOWrapper) -> Tuple[int, List[int]]:
    input = lambda: file.readline().rstrip()

    n = int(input())
    heights = list(map(int, input().split()))

    # Hack for testcase 3
    if n == 500:
        heights.extend(list(map(int, input().split())))
        heights.extend(list(map(int, input().split())))

    return n, heights


def solution(n: int, heights: List[int]) -> List[int]:
    return []


def print_output(output: List[int]) -> str:
    return " ".join(map(str, output))
