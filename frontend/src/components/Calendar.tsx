import { useState } from 'react';
import NavbarLink from './subcomponents/NavbarLink';
import Past from './Calendar/Past';
import Upcoming from './Calendar/Upcoming';

export default function Calendar() {
  const [view, setView] = useState<'przeszle' | 'nadchodzace'>('nadchodzace');
  const token = localStorage.getItem('token');

  if (!token) {
    return (
      <div className='flex flex-1 flex-col items-center py-4 justify-start w-screen'>
        Zaloguj sie by wyswietlic kalendarz
      </div>
    );
  } else {
    return (
      <div className='flex flex-1 flex-col justify-start w-screen'>
        <div className='flex justify-center gap-12 py-4'>
          <NavbarLink
            linkClick={() => setView('nadchodzace')}
            linkText='Nadchodzace'
          />
          <NavbarLink
            linkClick={() => setView('przeszle')}
            linkText='Przeszle'
          />
        </div>
        <div className='flex flex-1 justify-center items-start w-screen'>
          {view == 'przeszle' ? <Past /> : <Upcoming />}
        </div>
      </div>
    );
  }
}
