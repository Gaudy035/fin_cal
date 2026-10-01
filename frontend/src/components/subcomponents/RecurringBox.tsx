import NavbarLink from './NavbarLink';
import { useNavigate } from 'react-router';

interface RecurringBoxProps {
  recurring_id: number;
  category_id: number | null;
  amount: number;
  title: string;
  description?: string | null;
  transaction_type: 'income' | 'expense';
  next_date: string;
  account_owner?: string | null;
  account?: string | null;
  transaction_method?: 'cash' | 'transfer';
  interval: string;
  is_active: boolean | number;
}

export default function RecurringBox({
  recurring_id,
  category_id,
  amount,
  title,
  description,
  account_owner,
  account,
  transaction_method,
  transaction_type,
  next_date,
  interval,
  is_active,
}: RecurringBoxProps) {
  const navigate = useNavigate();

  const durConv = function (interval: string) {
    switch (interval) {
      case 'P30D':
        return 'miesiac';
      case 'P7D':
        return 'tydzien';
      case 'P1Y':
        return 'rok';
    }
  };

  const handleModify = () => {
    navigate('/modify', {
      state: {
        recurring_id,
        category_id,
        amount,
        title,
        description,
        account_owner,
        account,
        transaction_method,
        transaction_type,
        next_date,
        interval,
        is_active,
      },
    });
  };

  return (
    <div className='flex border-2 px-6 py-4 gap-2 flex-col my-4 w-9/10'>
      <div className='flex flex-row justify-between w-full'>
        <h2>{title}</h2>
        <div className='flex flex-col justify-start items-end'>
          <h2>Nastepny termin: {next_date}</h2>
          <p>Platne co {durConv(interval)}</p>
        </div>
      </div>
      <div className='flex items-center justify-between'>
        <h3
          className={
            transaction_type === 'income' ? 'text-green-600' : 'text-red-600'
          }
        >
          {transaction_type === 'expense' ? '-' : ''}
          {amount} PLN
        </h3>
        <div className='flex flex-col justify-end items-end'>
          <p>
            {transaction_method == 'transfer'
              ? `account: ${account}`
              : 'Platnosc gotowka'}
          </p>
          <p>
            {transaction_method == 'cash'
              ? `Własciciel konta: ${account_owner}`
              : ''}
          </p>
        </div>
      </div>
      <div className='flex flex-col justify-center items-start'>
        <p>{description ? description : ''}</p>
        <p className={is_active ? 'text-green-600' : 'text-red-600'}>
          {is_active ? 'AKTYWNA' : 'NIEAKTYWNA'}
        </p>
        <NavbarLink linkClick={handleModify} linkText='*Modyfikuj*' />
      </div>
    </div>
  );
}
