import { useState, useEffect } from 'react';
import type TPowtarzalna from '../Dashboard/TPowtarzalna';
import RecurringBox from '../subcomponents/RecurringBox';
import api from '../../api';

export default function Upcoming() {
  const token = localStorage.getItem('token');
  const [transakcje, setTransakcje] = useState<TPowtarzalna[]>([]);

  useEffect(() => {
    if (!token) {
      setTransakcje([]);
      return;
    }

    api
      .get('/recurring')
      .then((response) => setTransakcje(response.data))
      .catch((error) => console.log('blad polaczenia z API', error));
  }, [token]);

  return (
    <div className='flex flex-col justify-center items-center w-1/2'>
      {transakcje.map((item) => (
        <RecurringBox
          recurring_id={item.recurring_id}
          category_id={item.category_id}
          key={item.recurring_id}
          amount={item.amount}
          title={item.title}
          description={item.description}
          account_owner={item.account_owner}
          account={item.account}
          transaction_method={item.transaction_method}
          transaction_type={item.transaction_type}
          next_date={item.next_date}
          interval={item.interval}
          is_active={item.is_active}
        />
      ))}
    </div>
  );
}
