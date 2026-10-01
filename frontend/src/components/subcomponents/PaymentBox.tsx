interface PaymentBoxProps {
  amount: number;
  title: string;
  description?: string | null;
  transaction_type: 'income' | 'expense';
  transaction_date: string;
  account_owner?: string | null;
  account?: string | null;
  transaction_method?: string;
}

export default function PaymentBox({
  amount,
  title,
  description,
  account_owner,
  account,
  transaction_method,
  transaction_type,
  transaction_date,
}: PaymentBoxProps) {
  return (
    <div className='flex border-2 px-6 py-4 gap-2 flex-col my-4 w-9/10'>
      <div className='flex flex-row justify-between w-full'>
        <h2>{title}</h2>
        <h2>{transaction_date}</h2>
      </div>
      <div className='flex items-center justify-between'>
        <h3 className={transaction_type === 'income' ? 'text-green-600' : 'text-red-600'}>
          {transaction_type === 'expense' ? '-' : ''}
          {amount} PLN
        </h3>
        <div className='flex flex-col justify-end items-end'>
          <p>{transaction_method == 'transfer' ? `Konto: ${account}` : 'Platnosc gotowka'}</p>
          <p>
            {transaction_method == 'transfer' ? `Własciciel konta: ${account_owner}` : ''}
          </p>
        </div>
      </div>
      <div>
        <p>{description ? description : ''}</p>
      </div>
    </div>
  );
}