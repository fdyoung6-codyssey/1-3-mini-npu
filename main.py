# Mini NPU Simulator
# MAC 연산으로 패턴이 십자가(Cross)인지 X인지 판별하는 프로그램


def run_user_input_mode():
    """모드 1: 사용자가 3x3 필터와 패턴을 직접 입력하는 모드"""
    print("\n[모드 1] 사용자 입력 모드입니다. (준비 중)")


def run_json_mode():
    """모드 2: data.json 파일을 읽어서 분석하는 모드"""
    print("\n[모드 2] data.json 분석 모드입니다. (준비 중)")


def main():
    """프로그램 시작: 모드를 선택받는다"""
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    # 올바른 번호를 입력할 때까지 계속 반복
    while True:
        choice = input("선택: ").strip()

        if choice == "1":
            run_user_input_mode()
            break
        elif choice == "2":
            run_json_mode()
            break
        else:
            print("잘못된 입력입니다. 1 또는 2를 입력하세요.")


# 이 파일을 직접 실행했을 때만 main()을 시작
if __name__ == "__main__":
    main()