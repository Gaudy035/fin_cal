import { Routes, Route } from 'react-router-dom';
import Test from './components/Test';

function App() {
  return (
    <div className='min-h-screen flex bg-neutral-800 text-white font-mono justify-center items-center'>
      <Routes>
        <Route path='/' element={<Test />} />
      </Routes>
    </div>
  );
}

export default App;
