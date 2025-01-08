import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from multiprocessing import Pool, cpu_count
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

# JSON 파일에서 확률 데이터 로드
def load_biscuit_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

biscuit_data = load_biscuit_data()

# 시뮬레이션 함수
def run_simulation_worker(params):
    num_trials, rarity, selected_option = params
    results = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0 }
    attribute_names = list(biscuit_data[rarity].keys())
    base_probability = 9.0909  # 각 속성이 선택될 기본 확률 (%)
    num_slots = {'common': 1, 'rare': 2, 'epic': 3, 'legendary': 4}[rarity]

    for _ in range(num_trials):
        selected_attributes = []
        for _ in range(num_slots):
            selected_attribute = random.choices(attribute_names, weights=[base_probability] * len(attribute_names), k=1)[0]
            selected_attributes.append(selected_attribute)
        count = selected_attributes.count(selected_option)
        results[str(count)] += 1

    return results

# 병렬 시뮬레이션 함수
def run_simulation_parallel(num_trials, rarity, selected_option):
    num_workers = min(cpu_count(), 4)
    trials_per_worker = num_trials // num_workers
    params = [(trials_per_worker, rarity, selected_option) for _ in range(num_workers)]

    with Pool(processes=num_workers) as pool:
        worker_results = pool.map(run_simulation_worker, params)

    # 모든 워커의 결과를 합산
    final_results = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0 }
    for result in worker_results:
        for key in final_results:
            final_results[key] += result[key]

    return final_results

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    params = request.get_json()
    num_trials = params.get('numberOfTrials', 1000)
    rarity = params.get('rarity', 'common')
    selected_option = params.get('selectedOption', 'none')

    # 병렬 처리로 시뮬레이션 실행
    results = run_simulation_parallel(num_trials, rarity, selected_option)

    return jsonify({
        'results': results
    })

# 속성 값을 계산하는 함수
def calculate_attribute_value(attribute_data):
    min_value = attribute_data['min']
    max_value = attribute_data['max']
    probability = attribute_data['probability']
    possible_values = np.arange(min_value, max_value + 0.1, 0.1)
    return np.random.choice(possible_values, p=[probability / 100] * len(possible_values))

# 시도 횟수 계산 함수
def calculate_attempts(probability):
    return 1 / (probability / 100)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # 데이터가 비어있는지 확인
    if not data:
        return jsonify({"error": "요청 데이터가 없습니다."}), 400

    try:
        biscuit_type = data['biscuit_type']
        option_type1 = data['option_type1']
        option_value1 = float(data['option_value1'])
        element_type = data.get('element_type', 'none')
        option_type2 = data.get('option_type2')
        option_value2 = float(data.get('option_value2')) if option_type2 else None
        option_type3 = data.get('option_type3')
        option_value3 = float(data.get('option_value3')) if option_type3 else None
        option_type4 = data.get('option_type4')
        option_value4 = float(data.get('option_value4')) if option_type4 else None
    except KeyError as e:
        return jsonify({"error": f"필요한 키가 없습니다: {str(e)}"}), 400
    except ValueError:
        return jsonify({"error": "옵션 값이 유효한 숫자가 아닙니다."}), 400

    # 비스킷 데이터 유효성 검사 및 계산
    total_attempts = 1
    required_dough = 0
    total_probability = 1

    base_probability = 8.3333 if element_type != 'none' else 9.0909

    # 속성 옵션의 경우에도 데이터 참조 가능하도록 수정
    if element_type != 'none' and element_type in biscuit_data:
        if option_type1 == element_type:
            option_data1 = biscuit_data[element_type]
        elif option_type2 == element_type:
            option_data2 = biscuit_data[element_type]
        elif option_type3 == element_type:
            option_data3 = biscuit_data[element_type]
        elif option_type4 == element_type:
            option_data4 = biscuit_data[element_type]


    if biscuit_type == 'common':
        # 커먼 비스킷일 경우 기존 계산 방식 사용
        for option_type, option_value in [(option_type1, option_value1)]:
            if option_type:
                if biscuit_type in biscuit_data and option_type in biscuit_data[biscuit_type]:
                    option_data = biscuit_data[biscuit_type][option_type]
                    if option_value < option_data['min'] or option_value > option_data['max']:
                        return jsonify({"error": "값이 유효하지 않습니다."}), 400

                  # 각 옵션이 선택될 확률 (예: 공격력, 방어력 등)
                    option_probability = option_data['probability']

                    # 원하는 값 이상이 나올 확률 계산 (더 정확하게 범위를 고려)
                    desired_value_probability = 0
                    if option_value >= option_data['min'] and option_value <= option_data['max']:
                        steps = ((option_data['max'] - option_value) / 0.1) + 1
                        desired_value_probability = steps * (option_probability / 100)
                        desired_value_probability = min(desired_value_probability, 1.0)  # 확률은 최대 100%

                    # 선택된 옵션이 나올 확률과 원하는 값이 나올 확률을 곱하여 계산
                    attempts_for_option = calculate_attempts(base_probability) * calculate_attempts(desired_value_probability * 100)
                    total_attempts *= attempts_for_option

                    required_dough += int(total_attempts) * 10
                    total_probability *= (base_probability / 100) * (desired_value_probability)
    elif biscuit_type == 'rare':
        # 레어 비스킷일 경우 옵션 1과 옵션 2의 확률을 각각 구하고 곱한 후 추가 연산 수행
        if option_type1 and option_type2:
            if biscuit_type in biscuit_data and option_type1 in biscuit_data[biscuit_type] and option_type2 in biscuit_data[biscuit_type]:
                # 옵션 1 계산
                option_data1 = biscuit_data[biscuit_type][option_type1]
                if option_value1 < option_data1['min'] or option_value1 > option_data1['max']:
                    return jsonify({"error": "옵션 1 값이 유효하지 않습니다."}), 400

                
                option_probability1 = option_data1['probability']

                desired_value_probability1 = 0
                if option_value1 >= option_data1['min'] and option_value1 <= option_data1['max']:
                    steps1 = ((option_data1['max'] - option_value1) / 0.1) + 1
                    desired_value_probability1 = steps1 * (option_probability1 / 100)
                    desired_value_probability1 = min(desired_value_probability1, 1.0)

                # 옵션 2 계산
                option_data2 = biscuit_data[biscuit_type][option_type2]
                if option_value2 < option_data2['min'] or option_value2 > option_data2['max']:
                    return jsonify({"error": "옵션 2 값이 유효하지 않습니다."}), 400

                
                option_probability2 = option_data2['probability']

                desired_value_probability2 = 0
                if option_value2 >= option_data2['min'] and option_value2 <= option_data2['max']:
                    steps2 = ((option_data2['max'] - option_value2) / 0.1) + 1
                    desired_value_probability2 = steps2 * (option_probability2 / 100)
                    desired_value_probability2 = min(desired_value_probability2, 1.0)

                # 옵션 1과 옵션 2의 확률을 곱하고 0.01을 곱한 다음 곱하고 100을 곱함
                total_probability = ((base_probability / 100) * (desired_value_probability1)) * ((base_probability / 100) * (desired_value_probability2))

                # 시도 횟수 및 도우 계산
                total_attempts = calculate_attempts(total_probability * 100)
                required_dough = int(total_attempts) * 15
        else:
            return jsonify({"error": "레어 비스킷의 경우 옵션 2도 입력해야 합니다."}), 400
    elif biscuit_type == 'epic':
        # 에픽 비스킷일 경우 옵션 1, 옵션 2, 옵션 3의 확률을 각각 구하고 곱한 후 추가 연산 수행
        if option_type1 and option_type2 and option_type3:
            if biscuit_type in biscuit_data and option_type1 in biscuit_data[biscuit_type] and option_type2 in biscuit_data[biscuit_type] and option_type3 in biscuit_data[biscuit_type]:
                # 옵션 1 계산
                option_data1 = biscuit_data[biscuit_type][option_type1]
                if option_value1 < option_data1['min'] or option_value1 > option_data1['max']:
                    return jsonify({"error": "옵션 1 값이 유효하지 않습니다."}), 400

                
                option_probability1 = option_data1['probability']

                desired_value_probability1 = 0
                if option_value1 >= option_data1['min'] and option_value1 <= option_data1['max']:
                    steps1 = ((option_data1['max'] - option_value1) / 0.1) + 1
                    desired_value_probability1 = steps1 * (option_probability1 / 100)
                    desired_value_probability1 = min(desired_value_probability1, 1.0)

                # 옵션 2 계산
                option_data2 = biscuit_data[biscuit_type][option_type2]
                if option_value2 < option_data2['min'] or option_value2 > option_data2['max']:
                    return jsonify({"error": "옵션 2 값이 유효하지 않습니다."}), 400

                
                option_probability2 = option_data2['probability']

                desired_value_probability2 = 0
                if option_value2 >= option_data2['min'] and option_value2 <= option_data2['max']:
                    steps2 = ((option_data2['max'] - option_value2) / 0.1) + 1
                    desired_value_probability2 = steps2 * (option_probability2 / 100)
                    desired_value_probability2 = min(desired_value_probability2, 1.0)

                # 옵션 3 계산
                option_data3 = biscuit_data[biscuit_type][option_type3]
                if option_value3 < option_data3['min'] or option_value3 > option_data3['max']:
                    return jsonify({"error": "옵션 3 값이 유효하지 않습니다."}), 400

                
                option_probability3 = option_data3['probability']

                desired_value_probability3 = 0
                if option_value3 >= option_data3['min'] and option_value3 <= option_data3['max']:
                    steps3 = ((option_data3['max'] - option_value3) / 0.1) + 1
                    desired_value_probability3 = steps3 * (option_probability3 / 100)
                    desired_value_probability3 = min(desired_value_probability3, 1.0)

                # 옵션 1, 옵션 2, 옵션 3의 확률을 모두 곱함
                total_probability = ((base_probability / 100) * (desired_value_probability1)) * ((base_probability / 100) * (desired_value_probability2)) * ((base_probability / 100) * (desired_value_probability3))

                # 시도 횟수 및 도우 계산
                total_attempts = calculate_attempts(total_probability * 100)
                required_dough = int(total_attempts) * 20
        else:
            return jsonify({"error": "에픽 비스킷의 경우 옵션 3도 입력해야 합니다."}), 400
    elif biscuit_type == 'legendary':
        # 전설 비스킷일 경우 옵션 1, 2, 3, 4의 확률을 각각 구하고 곱한 후 추가 연산 수행
        if option_type1 and option_type2 and option_type3 and option_type4:
            if biscuit_type in biscuit_data and option_type1 in biscuit_data[biscuit_type] and option_type2 in biscuit_data[biscuit_type] and option_type3 in biscuit_data[biscuit_type] and option_type4 in biscuit_data[biscuit_type]:
                # 옵션 1 계산
                option_data1 = biscuit_data[biscuit_type][option_type1]
                if option_value1 < option_data1['min'] or option_value1 > option_data1['max']:
                    return jsonify({"error": "옵션 1 값이 유효하지 않습니다."}), 400

                
                option_probability1 = option_data1['probability']
                steps1 = ((option_data1['max'] - option_value1) / 0.1) + 1
                desired_value_probability1 = steps1 * (option_probability1 / 100)
                desired_value_probability1 = min(desired_value_probability1, 1.0)

                # 옵션 2 계산
                option_data2 = biscuit_data[biscuit_type][option_type2]
                if option_value2 < option_data2['min'] or option_value2 > option_data2['max']:
                    return jsonify({"error": "옵션 2 값이 유효하지 않습니다."}), 400

                
                option_probability2 = option_data2['probability']
                steps2 = ((option_data2['max'] - option_value2) / 0.1) + 1
                desired_value_probability2 = steps2 * (option_probability2 / 100)
                desired_value_probability2 = min(desired_value_probability2, 1.0)

                # 옵션 3 계산
                option_data3 = biscuit_data[biscuit_type][option_type3]
                if option_value3 < option_data3['min'] or option_value3 > option_data3['max']:
                    return jsonify({"error": "옵션 3 값이 유효하지 않습니다."}), 400

                
                option_probability3 = option_data3['probability']
                steps3 = ((option_data3['max'] - option_value3) / 0.1) + 1
                desired_value_probability3 = steps3 * (option_probability3 / 100)
                desired_value_probability3 = min(desired_value_probability3, 1.0)

                # 옵션 4 계산
                option_data4 = biscuit_data[biscuit_type][option_type4]
                if option_value4 < option_data4['min'] or option_value4 > option_data4['max']:
                    return jsonify({"error": "옵션 4 값이 유효하지 않습니다."}), 400

                
                option_probability4 = option_data4['probability']
                steps4 = ((option_data4['max'] - option_value4) / 0.1) + 1
                desired_value_probability4 = steps4 * (option_probability4 / 100)
                desired_value_probability4 = min(desired_value_probability4, 1.0)

                # 옵션 1, 옵션 2, 옵션 3, 옵션 4의 확률을 모두 곱함
                total_probability = ((base_probability / 100) * (desired_value_probability1)) * ((base_probability / 100) * (desired_value_probability2)) * ((base_probability / 100) * (desired_value_probability3)) * ((base_probability / 100) * (desired_value_probability4))

                # 시도 횟수 및 도우 계산
                total_attempts = int(calculate_attempts(total_probability * 100))
                required_dough = total_attempts * 30
        else:
            return jsonify({"error": "전설 비스킷의 경우 옵션 4까지 입력해야 합니다."}), 400
    else:
        return jsonify({"error": "비스킷 유형이 유효하지 않습니다."}), 400

    return jsonify({"expected_attempts": f"{total_attempts}", "required_dough": required_dough, "probability": f"{total_probability * 100:.17f}"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except OSError as e:
        print(f"Ignoring error: {e}")
        pass
