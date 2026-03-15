import PaymentBox from './subcomponents/PaymentBox';
import { useEffect, useState } from 'react';
import NavbarLink from './subcomponents/NavbarLink';
import type Transakcja from './Dashboard/Transakcja';

export default function Calendar() {
  const [view, setView] = useState<'przeszle' | 'nadchodzace'>('przeszle');
  const token = localStorage.getItem('token');
  const [transakcje, setTransakcje] = useState<Transakcja[]>([]);

  useEffect(() => {
    if (!token) {
      setTransakcje([]);
      return;
    }

    fetch('http://127.0.0.1:8000/transakcje', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data: Transakcja[]) => setTransakcje(data))
      .catch((error) => console.log('Blad polaczenia z API', error));
  }, [token]);

  const renderView = () => {
    switch (view) {
      case 'przeszle':
        return (
          <div className='flex flex-col justify-center items-center w-1/2'>
            {transakcje.map((item) => (
              <PaymentBox
                key={item.id_transakcji}
                kwota={item.kwota}
                typ={item.typ}
                tytul={item.tytul}
                data={item.data}
                konto={item.konto}
                metoda={item.metoda}
                wlasciciel_konta={item.wlasciciel_konta}
                opis={item.opis}
              />
            ))}
          </div>
        );
      case 'nadchodzace':
        return <div>Nadchodzące</div>;
    }
  };

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
            linkClick={() => setView('przeszle')}
            linkText='Przeszle'
          />
          <NavbarLink
            linkClick={() => setView('nadchodzace')}
            linkText='Nadchodzace'
          />
        </div>
        <div className='flex flex-1 justify-center items-center w-screen'>
          {renderView()}
        </div>
      </div>
    );
  }
}
