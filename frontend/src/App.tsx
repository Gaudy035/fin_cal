import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import PaymentForm from './components/PaymentForm';
import Calendar from './components/Calendar';
import Charts from './components/Charts';

function App() {
  return (
    <div className='min-h-screen flex flex-col bg-neutral-800 text-white font-mono justify-start'>
      <Navbar />
      <Routes>
        <Route path='/' element={<Dashboard />} />
        <Route path='/login' element={<LoginForm />} />
        <Route path='/rejestracja' element={<RegisterForm />} />
        <Route path='/nowy' element={<PaymentForm />} />
        <Route path='/kalendarz' element={<Calendar />} />
        <Route path='/wykresy' element={<Charts />} />
      </Routes>
    </div>
  );
}

export default App;
