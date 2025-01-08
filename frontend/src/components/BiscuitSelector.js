import React, { useState } from 'react';
import optionsData from './data.json'; // 옵션 정보
import biscuitData from '../data.json'; // 나머지 정보

function BiscuitSelector({ onSubmit }) {
    const [biscuit_type, setBiscuitType] = useState('common');
    const [element_type, setElementType] = useState('none');
    const [option_type1, setOptionType1] = useState('');
    const [option_value1, setOptionValue1] = useState('');
    const [option_type2, setOptionType2] = useState('');
    const [option_value2, setOptionValue2] = useState('');
    const [option_type3, setOptionType3] = useState('');
    const [option_value3, setOptionValue3] = useState('');
    const [option_type4, setOptionType4] = useState('');
    const [option_value4, setOptionValue4] = useState('');

    const handleBiscuitChange = (type) => {
        setBiscuitType(type);
        // 옵션 값 초기화
        setOptionType1('');
        setOptionValue1('');
        setOptionType2('');
        setOptionValue2('');
        setOptionType3('');
        setOptionValue3('');
        setOptionType4('');
        setOptionValue4('');
    };

    const handleElementChange = (type) => {
        setElementType(type);
        setOptionType1('');
        setOptionValue1('');
        setOptionType2('');
        setOptionValue2('');
        setOptionType3('');
        setOptionValue3('');
        setOptionType4('');
        setOptionValue4('');
    };

    const handleOptionValueChange = (optionType, setOptionValue) => {
        let optionData;
        // 옵션 데이터가 비스킷 유형 또는 속성 유형에서 올바르게 참조되도록 수정
        if (biscuitData[biscuit_type]?.[optionType]) {
            optionData = biscuitData[biscuit_type][optionType];
        } else if (optionsData[element_type]?.[optionType]) {
            optionData = biscuitData[element_type][optionType];
        }

        if (optionData) {
            const { min, max } = optionData;
            setOptionValue(`${min} ~ ${max}`);
        }
    };

    const handleSubmit = () => {
        if (biscuit_type && option_type1 && option_value1) {
            const payload = {
                biscuit_type,
                option_type1,
                option_value1,
                element_type,
            };
            if ((biscuit_type === 'rare' || biscuit_type === 'epic' || biscuit_type === 'legendary') && option_type2 && option_value2) {
                payload.option_type2 = option_type2;
                payload.option_value2 = option_value2;
            }
            if ((biscuit_type === 'epic' || biscuit_type === 'legendary') && option_type3 && option_value3) {
                payload.option_type3 = option_type3;
                payload.option_value3 = option_value3;
            }
            if (biscuit_type === 'legendary' && option_type4 && option_value4) {
                payload.option_type4 = option_type4;
                payload.option_value4 = option_value4;
            }
            onSubmit(payload);
        } else {
            alert('모든 값을 입력해주세요.');
        }
    };

    const translateOptionName = (optionKey) => {
        const translations = {
            "attack": "공격력",
            "defense": "방어력",
            "hp": "체력",
            "attack_speed": "공격속도",
            "crit_rate": "치명타 확률",
            "cooldown": "쿨타임",
            "damage_reduction": "피해감소",
            "crit_damage_reduction": "치명타 피해감소",
            "beneficial_effect": "이로운 효과 증가",
            "harmful_effect": "해로운 효과 감소",
            "ignore_damage_reduction": "피해감소 무시",
            "electric": "전기 속성 피해증가",
            "dark": "어둠 속성 피해증가",
            "earth": "땅 속성 피해증가",
            "fire": "불 속성 피해증가"
        };
        return translations[optionKey] || optionKey;
    };

    const renderOptions = () => {
        const baseOptions = Object.keys(optionsData[biscuit_type] || {}).map((key) => (
            <option key={key} value={key}>{translateOptionName(key)}</option>
        ));

        // 속성에 따라 추가 옵션 추가
        if (element_type !== 'none') {
            baseOptions.push(
                <option key={element_type} value={element_type}>{translateOptionName(element_type)}</option>
            );
        }

        return baseOptions;
    };

    return (
        <div>
            <h3>비스킷 종류 선택</h3>
            <div className='option_box_div'>
                <input
                    type="checkbox"
                    checked={biscuit_type === 'common'}
                    onChange={() => handleBiscuitChange('common')}
                />
                <span style={{ color: "#996600" }}>커먼</span>
                <input
                    type="checkbox"
                    checked={biscuit_type === 'rare'}
                    onChange={() => handleBiscuitChange('rare')}
                />
                <span style={{ color: "#33ccff" }}>레어</span>
                <input
                    type="checkbox"
                    checked={biscuit_type === 'epic'}
                    onChange={() => handleBiscuitChange('epic')}
                />
                <span style={{ color: "#9933ff" }}>에픽</span>
                <input
                    type="checkbox"
                    checked={biscuit_type === 'legendary'}
                    onChange={() => handleBiscuitChange('legendary')}
                />
                <span style={{ color: "#eecc00" }}>전설</span>
            </div>

            <h3>속성 선택</h3>
            <div className='option_box_div'>
                <input
                    type="checkbox"
                    checked={element_type === 'none'}
                    onChange={() => handleElementChange('none')}
                />
                일반
                <input
                    type="checkbox"
                    checked={element_type === 'electric'}
                    onChange={() => handleElementChange('electric')}
                />
                전기
                <input
                    type="checkbox"
                    checked={element_type === 'dark'}
                    onChange={() => handleElementChange('dark')}
                />
                어둠
                <input
                    type="checkbox"
                    checked={element_type === 'earth'}
                    onChange={() => handleElementChange('earth')}
                />
                대지
                <input
                    type="checkbox"
                    checked={element_type === 'fire'}
                    onChange={() => handleElementChange('fire')}
                />
                화염
            </div>

            <div className="option_div">
                <h3>옵션 1 선택</h3>
                <select value={option_type1} onChange={(e) => {
                    setOptionType1(e.target.value);
                    handleOptionValueChange(e.target.value, setOptionValue1);
                }}>
                    <option value="">선택하세요</option>
                    {renderOptions()}
                </select>

                <h3>옵션 1 값 입력</h3>
                <input
                    type="text"
                    value={option_value1}
                    onChange={(e) => setOptionValue1(e.target.value)}
                />
            </div>

            {(biscuit_type === 'rare' || biscuit_type === 'epic' || biscuit_type === 'legendary') && (
                <div className="option_div">
                    <h3>옵션 2 선택</h3>
                    <select value={option_type2} onChange={(e) => {
                        setOptionType2(e.target.value);
                        handleOptionValueChange(e.target.value, setOptionValue2);
                    }}>
                        <option value="">선택하세요</option>
                        {renderOptions()}
                    </select>

                    <h3>옵션 2 값 입력</h3>
                    <input
                        type="text"
                        value={option_value2}
                        onChange={(e) => setOptionValue2(e.target.value)}
                    />
                </div>
            )}

            {(biscuit_type === 'epic' || biscuit_type === 'legendary') && (
                <div className="option_div">
                    <h3>옵션 3 선택</h3>
                    <select value={option_type3} onChange={(e) => {
                        setOptionType3(e.target.value);
                        handleOptionValueChange(e.target.value, setOptionValue3);
                    }}>
                        <option value="">선택하세요</option>
                        {renderOptions()}
                    </select>

                    <h3>옵션 3 값 입력</h3>
                    <input
                        type="text"
                        value={option_value3}
                        onChange={(e) => setOptionValue3(e.target.value)}
                    />
                </div>
            )}

            {(biscuit_type === 'legendary') && (
                <div className="option_div">
                    <h3>옵션 4 선택</h3>
                    <select value={option_type4} onChange={(e) => {
                        setOptionType4(e.target.value);
                        handleOptionValueChange(e.target.value, setOptionValue4);
                    }}>
                        <option value="">선택하세요</option>
                        {renderOptions()}
                    </select>

                    <h3>옵션 4 값 입력</h3>
                    <input
                        type="text"
                        value={option_value4}
                        onChange={(e) => setOptionValue4(e.target.value)}
                    />
                </div>
            )}

            <button onClick={handleSubmit}>결과 보기</button>
        </div>
    );
}

export default BiscuitSelector;