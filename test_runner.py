from dbms import DBMS, Parser

def run_test(input_file, output_file=None):
    dbms = DBMS()
    parser = Parser(dbms)

    if output_file:
        dbms.output_file = output_file
        open(output_file, 'w').close()

    with open(input_file, 'r') as f:
        content = f.read()

    commands = []
    current = ""
    in_quote = False

    # 세미콜론 기준으로 command 분리
    for char in content:
        if char == '"':
            in_quote = not in_quote

        current += char

        if char == ';' and not in_quote:
            commands.append(current.strip())
            current = ""

    # 실행
    for cmd in commands:
        if cmd:
            print(f"\n>>> {cmd}")
            try:
                parser.parse(cmd)
            except Exception as e:
                print(f"Error: {e}")

    dbms.output_file = None


if __name__ == "__main__":
    run_test(
        "sample-project-test-data.txt",
        "test_output1.txt"
    )