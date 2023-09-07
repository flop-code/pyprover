from prover import prove, ProverError
from typing import NoReturn


def main() -> NoReturn:
    while True:
        user_input = input(":: ")
        if not user_input:
            continue

        try:
            result, falls_on = prove(user_input)
        except ProverError as err:
            print("Error: " + str(err))
            continue

        falls_on_string = ""
        for key, value in falls_on.items():
            falls_on_string += f"; {key}={value}"
        falls_on_string = falls_on_string[2:]

        print(result, f"({falls_on_string})" if (not result) and falls_on else "")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
