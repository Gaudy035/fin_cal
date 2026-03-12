import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';
// placeholder
// import Wip from './components/Wip';

function App() {
  return (
    <div className='min-h-screen flex flex-col bg-neutral-800 text-white font-mono justify-start'>
      <Navbar />
      <Routes>
        <Route path='/' element={<Dashboard />} />
        <Route path='/login' element={<LoginForm />} />
      </Routes>
    </div>
  );
}

export default App;
