# Mini NPU Simulator
# MAC 연산으로 패턴이 십자가(Cross)인지 X인지 판별하는 프로그램


# ★ 새로 추가: n x n 배열을 한 줄씩 입력받는 함수
def read_matrix(name, size):
    """size x size 배열을 한 줄씩 입력받아 2차원 리스트로 돌려준다"""
    print(f"{name} ({size}줄 입력, 공백 구분)")
    matrix = []  # 입력받은 줄들을 모아둘 빈 리스트

    # 줄 수가 size개가 될 때까지 반복
    while len(matrix) < size:
        line = input().strip()
        parts = line.split()  # 공백 기준으로 자르기: "0 1 0" → ["0", "1", "0"]

        # 검증 1: 숫자 개수가 맞는지
        if len(parts) != size:
            print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
            continue  # 이 줄을 다시 입력받기

        # 검증 2: 전부 숫자인지
        row = []
        try:
            for p in parts:
                row.append(float(p))  # 글자 "1" → 숫자 1.0
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue  # 이 줄을 다시 입력받기

        matrix.append(row)  # 검증을 통과한 줄만 저장

    return matrix


def print_section(title):
    """구역 제목을 보기 좋게 출력한다"""
    print()
    print("#---------------------------------------")
    print(f"# {title}")
    print("#---------------------------------------")


# ★ 새로 추가: MAC 연산 함수
def mac(pattern, filter_matrix):
    """패턴과 필터의 같은 위치끼리 곱하고(Multiply), 모두 더한다(Accumulate)"""
    size = len(pattern)  # 배열 크기 (3x3이면 3)
    total = 0.0          # 곱한 값을 계속 더해갈 변수

    for i in range(size):          # i: 줄 번호 (0, 1, 2)
        for j in range(size):      # j: 칸 번호 (0, 1, 2)
            total += pattern[i][j] * filter_matrix[i][j]

    return total

# ★ 수정: 모드 1에서 필터와 패턴을 입력받도록 변경
def run_user_input_mode():
    """모드 1: 사용자가 3x3 필터와 패턴을 직접 입력하는 모드"""
    print_section("[1] 필터 입력")
    filter_a = read_matrix("필터 A", 3)
    print()
    filter_b = read_matrix("필터 B", 3)
    print("\n필터 A, B 저장 완료!")

    print_section("[2] 패턴 입력")
    pattern = read_matrix("패턴", 3)

    # MAC 연산으로 점수 계산
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    print_section("[3] MAC 결과")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")


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