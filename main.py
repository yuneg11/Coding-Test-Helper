import os
import sys
import inspect
import argparse
from importlib import import_module
from importlib.util import (
    spec_from_file_location,
    module_from_spec,
)
from io import TextIOWrapper

def solution_raw(file: TextIOWrapper) -> str:
    input_lines = file.readlines()
    answer = ""
    return answer


def get_cases(case_dir):
    case_files = os.listdir(case_dir)
    cases = {}

    for filename in case_files:
        ids, _ = filename.split(".")
        number, in_out = int(ids[:-1]), ids[-1]

        if number in cases:
            cases[number][in_out] = case_dir + filename
        else:
            cases[number] = {in_out: case_dir + filename}

    return cases


def eval_cases(solution_pipeline, cases, prefix="", max_output_len=80):
    correct, wrong = 0, 0

    for case_number, case_set in sorted(cases.items()):
        if "i" in case_set and "o" in case_set:
            with open(case_set["i"]) as input_file:
                solution_output = solution_pipeline(input_file).rstrip()

            with open(case_set["o"]) as output_file:
                expected_output = output_file.read().rstrip()

                if solution_output == expected_output:
                    correct += 1
                    print(f"{prefix}#{case_number}: Pass")
                else:
                    wrong += 1

                    trimmed_expected = expected_output[:max_output_len]
                    trimmed_solution = solution_output[:max_output_len]

                    if len(expected_output) > max_output_len:
                        expected_ellipsis = "..."
                    else:
                        expected_ellipsis = ""

                    if len(solution_output) > max_output_len:
                        solution_ellipsis = "..."
                    else:
                        solution_ellipsis = ""

                    print(f"{prefix}#{case_number}: Fail")
                    print(f"    Expected: {trimmed_expected}{expected_ellipsis}")
                    print(f"    Actual  : {trimmed_solution}{solution_ellipsis}")

    return correct, wrong


def eval_solution(pipeline, problem_dir, max_output_len=80):
    sample_cases = get_cases(problem_dir + "/sample/")
    test_cases = get_cases(problem_dir + "/test/")

    sample_eval = eval_cases(pipeline, sample_cases, "Sample case ", max_output_len)
    print()
    test_eval = eval_cases(pipeline, test_cases, "Test case ", max_output_len)
    print()

    print(f"Sample cases: {sample_eval[0]} / {sample_eval[0] + sample_eval[1]}")
    print(f"Test cases: {test_eval[0]} / {test_eval[0] + test_eval[1]}")

    pass_all = (sample_eval[1] + test_eval[1] == 0)
    return pass_all


def get_function_annotations(function):
    annotations = function.__annotations__

    # TODO: Modify type annotation (t)
    annotation_doc = "\n".join([f"# {n}: {t}" for n, t in annotations.items()])
    return annotation_doc


def get_function_head(function):
    name = function.__name__
    signature = inspect.signature(function)
    parameters = ", ".join(signature.parameters.keys())
    return f"def {name}({parameters}):"


def getsource(function):
    head = get_function_head(function)
    body = "\n".join(inspect.getsource(function).split("\n")[1:])
    return head + "\n" + body


def get_submit_code(
    solution_raw=None,
    read_input=None,
    solution=None,
    print_output=None,
):
    if solution_raw:
        solution_raw_source = getsource(solution_raw)
        submit_code = "import sys\n\n" \
            + solution_raw_source + "\n" \
            + "print(solution_raw(sys.stdin))"
    elif read_input and solution and print_output:
        read_input_source = getsource(read_input)
        solution_source = getsource(solution)
        print_output_source = getsource(print_output)

        submit_code = "import sys\n\n" \
            + read_input_source + "\n" \
            + solution_source + "\n" \
            + print_output_source + "\n" \
            + "print(print_output(solution(*read_input(sys.stdin))))"
    else:
        raise ValueError("Arguments are invalid. Give 'solution_raw' "
                         "or ('read_input', 'solution', 'print_output')")

    return submit_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_id", metavar="<Problem-ID>")
    parser.add_argument("-s", "--solution")
    parser.add_argument("-c", "--submit-code")
    parser.add_argument("-m", "--max-output-len", type=int, default=80)
    args = parser.parse_args(sys.argv[1:])

    site, problem_num = args.problem_id.split(":")

    if site == "codeup":
        if os.path.exists(f"data/codeup/id{problem_num}"):
            site_cased = "CodeUp"
            problem_dir = f"data/codeup/id{problem_num}"
            problem_module = import_module(f"data.codeup.id{problem_num}.problem")
        else:
            raise ValueError(f"Problem '{problem_num}' is not in codeup.")
    else:
        raise ValueError(f"Site '{site}' is not supported.")

    if args.solution:
        if os.path.exists(args.solution):
            solution_path = "".join(args.solution.split("/")[-1].split(".")[:-1])
            solution_spec = spec_from_file_location(solution_path, args.solution)
            solution_module = module_from_spec(solution_spec)
            solution_spec.loader.exec_module(solution_module)

            if "solution_raw" in dir(solution_module):
                pipeline = solution_module.solution_raw
                pass_all = eval_solution(pipeline, problem_dir, args.max_output_len)

                submit_code = get_submit_code(solution_raw=solution_module.solution_raw)
            elif "solution" in dir(solution_module):
                def pipeline(input_file):
                    input_args = problem_module.read_input(input_file)
                    output = solution_module.solution(*input_args)
                    answer = problem_module.print_output(output)
                    return answer

                pass_all = eval_solution(pipeline, problem_dir, args.max_output_len)

                submit_code = get_submit_code(
                    read_input=problem_module.read_input,
                    solution=solution_module.solution,
                    print_output=problem_module.print_output)
            else:
                raise ValueError(f"One of 'solution' or 'solution_raw' "
                                 f"function not exists in '{args.solution}'")

            if args.submit_code:
                with open(args.submit_code, "w") as submit_file:
                    submit_file.write(submit_code)
            elif pass_all:
                print_code = input("Show submit code (y/n): ")
                if print_code.lower() == "y":
                    print("\nSubmit code:\n")
                    print(submit_code)

        else:
            raise ValueError(f"Solution file '{args.solution}' not exists.")
    else:
        if "solution" in dir(problem_module):
            print(f"Skeleton code for {site_cased}:{problem_num}\n")
            print(get_function_annotations(problem_module.solution))
            print(getsource(problem_module.solution))

        print(f"Skeleton code for general problems\n")
        print(get_function_annotations(solution_raw))
        print(getsource(solution_raw))
