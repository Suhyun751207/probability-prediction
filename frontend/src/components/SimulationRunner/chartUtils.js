// chartUtils.js
import { Chart, registerables } from 'chart.js';

// Chart.js 버전 3 이상에서는 등록이 필요합니다.
Chart.register(...registerables);

let chartInstance = null;

export function renderChart(ctx, data, rarity) {
    // 기존 차트 인스턴스가 있으면 먼저 파괴합니다.
    if (chartInstance) {
        chartInstance.destroy();
    }

    // 희귀도에 따라 라벨과 값의 수를 조정합니다.
    let labels = [];
    let values = [];

    switch (rarity) {
        case 'legendary':
            labels = ['0', '1', '2', '3', '4'];
            values = [
                data['0'] || 0,
                data['1'] || 0,
                data['2'] || 0,
                data['3'] || 0,
                data['4'] || 0
            ];
            break;
        case 'epic':
            labels = ['0', '1', '2', '3'];
            values = [
                data['0'] || 0,
                data['1'] || 0,
                data['2'] || 0,
                data['3'] || 0
            ];
            break;
        case 'rare':
            labels = ['0', '1', '2'];
            values = [
                data['0'] || 0,
                data['1'] || 0,
                data['2'] || 0
            ];
            break;
        case 'common':
            labels = ['0', '1'];
            values = [
                data['0'] || 0,
                data['1'] || 0
            ];
            break;
        default:
            labels = ['0'];
            values = [data['0'] || 0];
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Option Occurrence',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.raw;
                            return label;
                        }
                    }
                },
                datalabels: {
                    anchor: 'end',
                    align: 'top',
                    formatter: (value) => {
                        return value;
                    },
                    color: 'black',
                    font: {
                        weight: 'bold'
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index) {
                            return labels[index] + ' (' + values[index] + ')';
                        }
                    }
                },
                y: {
                    type: 'linear',
                    beginAtZero: true,
                    suggestedMax: Math.max(...values) + 10  // 고정된 높이를 위해 최대값에 여유를 추가
                }
            }
        }
    });
}
