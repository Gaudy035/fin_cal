import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  plugins,
} from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { useEffect, useState } from 'react';

interface Stat {
  kategoria: string;
  kwota: number;
}

ChartJS.register(ArcElement, Tooltip, Legend, plugins);

export default function PieChart() {
  const token = localStorage.getItem('token');
  const [stats, setStats] = useState<Stat[]>([]);

  useEffect(() => {
    if (!token) {
      setStats([]);
      return;
    }

    fetch('http://127.0.0.1:8000/get_stats', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data: Stat[]) => setStats(data))
      .catch((error) => console.log('Blad polaczenia z API', error));
  }, [token]);
  // console.log(stats);

  const options = {
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          color: 'white' as const,
          font: {
            size: 16,
          },
        },
      },
    },
  };

  const chartData = {
    labels: stats.map((item) => item.kategoria),
    datasets: [
      {
        label: 'Wydatki',
        data: stats.map((item) => item.kwota),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className='flex justify-start flex-col items-center w-full max-h-screen flex-1'>
      <div className='flex flex-1 justify-start flex-col py-6 w-1/3 items-center h-full'>
        <Pie data={chartData} options={options} />
      </div>
    </div>
  );
}
