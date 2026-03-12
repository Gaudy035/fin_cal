interface PaymentBoxProps {
  kwota: number;
  tytul: string;
  //   opis: string;
  typ: 'wplyw' | 'wydatek';
  data: string;
}

export default function PaymentBox({
  kwota,
  tytul,
  //   opis,
  typ,
  data,
}: PaymentBoxProps) {
  return (
    <div className='flex border-2 px-6 py-4 gap-2 flex-col my-4 w-9/10'>
      <div className='flex flex-row justify-between w-full'>
        <h2>{tytul}</h2>
        <h2>{data}</h2>
      </div>
      <div>
        <h3 className={typ === 'wplyw' ? 'text-green-600' : 'text-red-600'}>
          {typ === 'wydatek' ? '-' : ''}
          {kwota} PLN
        </h3>
      </div>
    </div>
  );
}
