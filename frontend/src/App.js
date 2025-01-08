import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import BiscuitSelector from './components/BiscuitSelector';
import ResultModal from './components/ResultModal';
import SimulationRunner from './components/SimulationRunner/SimulationRunner';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleBiscuitSubmit = async (data) => {
    try {
      const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (response.ok) {
        setResult(result);
        setIsModalOpen(true);
      } else {
        console.error('Server Error:', result.error);
        alert(result.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('서버 오류가 발생했습니다.');
    }
  };

  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li><Link to="/check">Biscuit Selector</Link></li>
            <li><Link to="/SimulationRunner">Simulation Runner</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/check" element={<BiscuitSelector onSubmit={handleBiscuitSubmit} />} />
          <Route path="/SimulationRunner" element={<SimulationRunner />} />
        </Routes>
        <ResultModal isOpen={isModalOpen} result={result} onClose={() => setIsModalOpen(false)} />
      </div>
    </Router>
  );
}

export default App;
