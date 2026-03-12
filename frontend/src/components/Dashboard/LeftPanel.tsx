import { useState, useEffect } from 'react';
import PaymentBox from '../subcomponents/PaymentBox';

export interface Transakcja {
  id_transakcji: number;
  id_uzytkownika: number;
  id_kategorii: number | null;
  typ: 'wplyw' | 'wydatek';
  tytul: string;
  opis: string | null;
  kwota: number;
  metoda: string;
  konto: string | null;
  wlasciciel_konta: string | null;
  data: string;
}

export default function LeftPanel() {
  const [wplywy, setWplywy] = useState<Transakcja[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/wplywy')
      .then((response) => response.json())
      .then((data: Transakcja[]) => setWplywy(data))
      .catch((error) => console.log('Blad przy pobieraniu wplywow: ', error));
  }, []);

  return (
    <div className='flex flex-1 max-w-1/2 border-2 border-white justify-start items-center flex-col min-h-full py-6'>
      {wplywy.map((item) => (
        <PaymentBox
          key={item.id_transakcji}
          kwota={item.kwota}
          typ={item.typ}
          tytul={item.tytul}
          data={item.data}
        />
      ))}
      {/* <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' />
      <PaymentBox kwota={1000.0} typ='wplyw' tytul='test' data='00-00-0000' /> */}
    </div>
  );
}
