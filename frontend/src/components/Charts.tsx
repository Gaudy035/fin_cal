import Wip from './Wip';

export default function Charts() {
  const token = localStorage.getItem('token');

  if (!token) {
    return (
      <div className='flex flex-1 flex-col items-center py-4 justify-start w-screen'>
        Zaloguj sie by wyswietlic wykresy
      </div>
    );
  } else {
    return <Wip />;
  }
}
