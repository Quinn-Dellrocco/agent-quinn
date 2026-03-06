from functions.get_files_info import get_files_info

def print_result(title, result):
    print(title)

    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.splitlines():
            print(f"  {line}")

    print() 

if __name__ == "__main__":
    print_result(
        "Result for current directory:",
        get_files_info("calculator", "."),
    )
    print_result(
        "Result for 'pkg' directory:",
        get_files_info("calculator", "pkg"),
    )
    print_result(
        "Result for '/bin' directory:",
        get_files_info("calculator", "/bin"),
    )
    print_result(
        "Result for '../' directory:",
        get_files_info("calculator", "../"),
    )