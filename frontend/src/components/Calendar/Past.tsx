import { useEffect, useState } from 'react';
import PaymentBox from '../subcomponents/PaymentBox';
import type Transakcja from '../Dashboard/Transakcja';
import api from '../../api';

export default function Past() {
  const token = localStorage.getItem('token');
  const [transakcje, setTransakcje] = useState<Transakcja[]>([]);

  useEffect(() => {
    if (!token) {
      setTransakcje([]);
      return;
    }

    api
      .get('/transactions')
      .then((response) => setTransakcje(response.data))
      .catch((error) => console.log('Blad polaczenia z API', error));
  }, [token]);

  return (
    <div className='flex flex-col justify-center items-center w-1/2'>
      {transakcje.map((item) => (
        <PaymentBox
          key={item.transaction_id}
          amount={item.amount}
          transaction_type={item.transaction_type}
          title={item.title}
          transaction_date={item.transaction_date}
          account={item.account}
          transaction_method={item.transaction_method}
          account_owner={item.account_owner}
          description={item.description}
        />
      ))}
    </div>
  );
}
