// SimulationRunner.js
import React, { useState } from 'react';
import { renderChart } from './chartUtils';

function SimulationRunner() {
    const [numberOfTrials, setNumberOfTrials] = useState(1000);
    const [rarity, setRarity] = useState('common');
    const [selectedOption, setSelectedOption] = useState('none');
    const [simulationData, setSimulationData] = useState(null);
    const chartRef = React.useRef(null);

    const runSimulation = async () => {
        try {
            const response = await fetch('http://localhost:5000/run-simulation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ numberOfTrials, rarity, selectedOption })
            });
            const data = await response.json();
            setSimulationData(data.results);
        } catch (error) {
            console.error("시뮬레이션 실패", error);
        }
    };

    React.useEffect(() => {
        if (simulationData && chartRef.current) {
            renderChart(chartRef.current.getContext('2d'), simulationData, rarity);
        }
    }, [simulationData, rarity]);

    return (
        <div>
            <h1>비스킷 시뮬레이션</h1>
            <div>
                <label>시도 횟수 (최대 500,000): </label>
                <input
                    type="number"
                    value={numberOfTrials}
                    onChange={(e) => setNumberOfTrials(Math.min(5000000, Math.max(1, e.target.value)))}
                />
            </div>
            <div>
                <label>희귀도: </label>
                <select value={rarity} onChange={(e) => setRarity(e.target.value)}>
                    <option value="common">커먼</option>
                    <option value="rare">레어</option>
                    <option value="epic">에픽</option>
                    <option value="legendary">전설</option>
                </select>
            </div>
            <div>
                <label>옵션: </label>
                <select value={selectedOption} onChange={(e) => setSelectedOption(e.target.value)}>
                    <option value="none">없음</option>
                    <option value="attack">공격력</option>
                    <option value="defense">방어력</option>
                    <option value="hp">HP</option>
                    <option value="attack_speed">공격 속도</option>
                    <option value="crit_rate">치명타 확률</option>
                    <option value="cooldown">쿨다운</option>
                    <option value="damage_reduction">피해 감소</option>
                    <option value="crit_damage_reduction">치명타 피해 감소</option>
                    <option value="beneficial_effect">유익한 효과</option>
                    <option value="harmful_effect">해로운 효과</option>
                    <option value="ignore_damage_reduction">피해 감소 무시</option>
                </select>
            </div>
            <button onClick={runSimulation}>시뮬레이션 실행</button>
            <canvas ref={chartRef} id="simulationChart"></canvas>
        </div>
    );
}

export default SimulationRunner;
