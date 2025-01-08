# SimulationRunner.py
import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import socket

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# JSON 데이터 로드
json_path = os.path.join(os.path.dirname(__file__), 'data.json')
with open(json_path, 'r') as file:
    item_data = json.load(file)

def calculate_attribute_value(attribute_data):
    min_value = attribute_data['min']
    max_value = attribute_data['max']
    probability = attribute_data['probability']
    
    possible_values = [round(x, 1) for x in frange(min_value, max_value, 0.1)]
    return random.choices(possible_values, weights=[probability] * len(possible_values), k=1)[0]

def frange(start, stop, step):
    while start <= stop:
        yield start
        start += step

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    params = request.get_json()
    num_trials = params.get('numberOfTrials', 1000)
    rarity = params.get('rarity', 'common')  # 유저가 선택한 희귀도 (common, rare, epic, legendary)
    selected_option = params.get('selectedOption', 'none')

    results = { 'none': 0, 'one': 0, 'two': 0, 'three': 0, 'four': 0 }
    attribute_names = list(item_data[rarity].keys())
    base_probability = 9.0909  # 각 속성이 선택될 기본 확률 (%)

    num_slots = {'common': 1, 'rare': 2, 'epic': 3, 'legendary': 4}[rarity]

    for _ in range(num_trials):
        selected_attributes = []

        # 각 칸마다 속성을 선택하고 값을 결정합니다.
        for _ in range(num_slots):
            selected_attribute = random.choices(attribute_names, weights=[base_probability] * len(attribute_names), k=1)[0]
            selected_value = calculate_attribute_value(item_data[rarity][selected_attribute])
            selected_attributes.append(selected_attribute)

        # 원하는 옵션이 얼마나 나왔는지 확인합니다.
        count = selected_attributes.count(selected_option)
        if count == 0:
            results['none'] += 1
        elif count == 1:
            results['one'] += 1
        elif count == 2:
            results['two'] += 1
        elif count == 3:
            results['three'] += 1
        elif count == 4:
            results['four'] += 1

    return jsonify({
        'results': results
    })

if __name__ == '__main__':
    try:
        app.run(port=5001, debug=True)
    except OSError as e:
        print(f"Ignoring error: {e}")
        pass
