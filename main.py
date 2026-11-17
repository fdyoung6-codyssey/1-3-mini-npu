# Mini NPU Simulator
# MAC 연산으로 패턴이 십자가(Cross)인지 X인지 판별하는 프로그램

import time  # 시간 측정용 표준 라이브러리
import json  # ★ 새로 추가: JSON 파일 읽기용 표준 라이브러리

# 점수를 같다고 볼 허용 오차
EPSILON = 1e-9

# 시간 측정 반복 횟수
REPEAT = 10

# ★ 새로 추가: 읽어올 데이터 파일 이름
DATA_FILE = "data.json"

# ★ 새로 추가: 여러 모양의 라벨을 표준 라벨로 바꾸는 표
LABEL_MAP = {
    "+": "Cross",
    "cross": "Cross",
    "x": "X",
}


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

# ★ 새로 추가: 두 점수를 비교해서 판정하는 함수
def judge(score_a, score_b):
    """점수 차이가 EPSILON보다 작으면 동점, 아니면 더 큰 쪽을 고른다"""
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"   # 동점 → 판정 불가
    elif score_a > score_b:
        return "A"
    else:
        return "B"

# ★ 새로 추가: MAC 연산 평균 시간 측정 함수
def measure_mac_time(pattern, filter_matrix):
    """MAC 연산을 REPEAT번 반복해서 1회 평균 시간(ms)을 돌려준다"""
    start = time.perf_counter()          # 시작 시각 기록

    for _ in range(REPEAT):              # REPEAT번 반복
        mac(pattern, filter_matrix)

    end = time.perf_counter()            # 끝난 시각 기록

    total_seconds = end - start                  # 걸린 전체 시간(초)
    average_ms = total_seconds / REPEAT * 1000   # 1회 평균, 초 → ms
    return average_ms

# ★ 새로 추가: 라벨 정규화 함수
def normalize_label(label):
    """'+', 'cross', 'x' 같은 라벨을 표준 라벨 'Cross' 또는 'X'로 바꾼다"""
    key = str(label).strip().lower()   # 앞뒤 공백 제거 + 소문자로 통일
    return LABEL_MAP.get(key)          # 표에 없는 라벨이면 None을 돌려줌


# ★ 새로 추가: JSON 파일 읽기 함수
def load_json(path):
    """JSON 파일을 읽어 딕셔너리로 돌려준다. 실패하면 None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: '{path}' 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        print(f"오류: '{path}' 파일의 JSON 형식이 올바르지 않습니다.")
    return None


# ★ 새로 추가: 필터 불러오기 함수
def load_filters(data):
    """filters 부분을 {크기: {"Cross": 배열, "X": 배열}} 모양으로 정리한다"""
    filters = {}

    for key, value in data.get("filters", {}).items():
        # "size_5" → 밑줄(_)로 잘라서 뒤쪽 "5"를 숫자로 바꾸기
        try:
            size = int(key.split("_")[1])
        except (IndexError, ValueError):
            print(f"경고: 필터 키 '{key}'에서 크기를 알 수 없어 건너뜁니다.")
            continue

        filters[size] = {}
        for label, matrix in value.items():
            std_label = normalize_label(label)
            if std_label is None:
                print(f"경고: {key}의 알 수 없는 라벨 '{label}'은 건너뜁니다.")
                continue
            filters[size][std_label] = matrix

        loaded = ", ".join(filters[size].keys())
        print(f"✓ {key} 필터 로드 완료 ({loaded})")

    return filters

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

    # 연산 시간 측정 (입력/출력 시간은 제외하고 MAC 연산만 측정)
    avg_ms = measure_mac_time(pattern, filter_a)
    print(f"연산 시간(평균/{REPEAT}회): {avg_ms:.3f} ms")

    # 판정
    result = judge(score_a, score_b)
    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {result}")


def run_json_mode():
    """모드 2: data.json 파일을 읽어서 분석하는 모드"""
    data = load_json(DATA_FILE)
    if data is None:
        return   # 파일을 못 읽으면 모드 2를 끝냄

    print_section("[1] 필터 로드")
    filters = load_filters(data)


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