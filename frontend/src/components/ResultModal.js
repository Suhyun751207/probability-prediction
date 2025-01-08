import React from 'react';
import './ResultModal.css';

function ResultModal({ isOpen, result, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>결과</h2>
        <p>예상 시도 횟수: {Number(result.expected_attempts).toLocaleString()} 회</p>
        <p>필요한 비스킷 도우: {Number(result.required_dough).toLocaleString()} 개</p>
        <p>나올 확률: {Number(result.probability).toFixed(17)} %</p>
        <button onClick={onClose}>닫기</button>
      </div>
    </div>
  );
}

export default ResultModal;
