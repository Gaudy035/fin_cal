import PaymentBox from '../subcomponents/PaymentBox';
import { useState, useEffect } from 'react';
import type Transakcja from './Transakcja';

export default function RightPanel() {
  const [wydatki, setWydatki] = useState<Transakcja[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/wydatki')
      .then((response) => response.json())
      .then((data: Transakcja[]) => setWydatki(data))
      .catch((error) => console.log('Blad przy pobieraniu wydatkow: ', error));
  }, []);

  return (
    <div className='flex flex-1 max-w-1/2 border-2 border-white justify-start items-center flex-col min-h-full py-6'>
      {wydatki.map((item) => (
        <PaymentBox
          key={item.id_transakcji}
          kwota={item.kwota}
          typ={item.typ}
          tytul={item.tytul}
          data={item.data}
        />
      ))}
    </div>
  );
}
