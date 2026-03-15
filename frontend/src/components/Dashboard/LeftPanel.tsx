import { useState, useEffect } from 'react';
import PaymentBox from '../subcomponents/PaymentBox';
import type Transakcja from './Transakcja';

export default function LeftPanel() {
  const token = localStorage.getItem('token');
  const [wplywy, setWplywy] = useState<Transakcja[]>([]);

  useEffect(() => {
    if (!token) {
      setWplywy([]);
      return;
    }

    fetch('http://127.0.0.1:8000/wplywy', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data: Transakcja[]) => setWplywy(data))
      .catch((error) => console.log('Blad przy pobieraniu wplywow: ', error));
  }, [token]);

  return (
    <div className='flex flex-1 max-w-1/2 border-2 border-white justify-start items-center flex-col min-h-full py-6'>
      {token
        ? wplywy.map((item) => (
            <PaymentBox
              key={item.id_transakcji}
              kwota={item.kwota}
              typ={item.typ}
              tytul={item.tytul}
              data={item.data}
            />
          ))
        : 'Zaloguj sie by wyswietlic wplywy'}
    </div>
  );
}
