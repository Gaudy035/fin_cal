import { useState, useEffect } from 'react';
import PaymentBox from '../subcomponents/PaymentBox';
import type Transakcja from './Transakcja';
import api from '../../api';

export default function LeftPanel() {
  const token = localStorage.getItem('token');
  const [wplywy, setWplywy] = useState<Transakcja[]>([]);

  useEffect(() => {
    if (!token) {
      setWplywy([]);
      return;
    }

api
      .get('/transactions/income')
      .then((response) => setWplywy(response.data))
      .catch((error) => console.log('Blad przy pobieraniu wplywow', error));
  }, [token]);

  return (
    <div className='flex flex-1 max-w-1/2 border-2 border-white justify-start items-center flex-col min-h-full py-6 relative'>
      <h1 className='absolute text-lg -top-3.5 left-48 px-2 bg-neutral-800'>
        Wplywy
      </h1>
      {token
        ? wplywy.map((item) => (
            <PaymentBox
              key={item.transaction_id}
              amount={item.amount}
              transaction_type={item.transaction_type}
              title={item.title}
              transaction_date={item.transaction_date}
              transaction_method={item.transaction_method}
              account_owner={item.account_owner}
              account={item.account}
            />
          ))
        : 'Zaloguj sie by wyswietlic wplywy'}
    </div>
  );
}
