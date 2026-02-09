from functions.get_file_content import get_file_content
from config import MAX_CHARS

def test_lorem_truncation():
    content = get_file_content("calculator", "lorem.txt")

    if f'truncated at {MAX_CHARS} characters' in content:
        print("PASS: File was truncated correctly")
    else:
        print("FAIL: File was NOT truncated")

    print("Returned content length:", len(content))


def run_manual_tests():
    print("\n--- main.py ---")
    print(get_file_content("calculator", "main.py"))

    print("\n--- pkg/calculator.py ---")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n--- /bin/cat (should error) ---")
    print(get_file_content("calculator", "/bin/cat"))

    print("\n--- does_not_exist.py (should error) ---")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))



if __name__ == "__main__":
    test_lorem_truncation()
    run_manual_tests()