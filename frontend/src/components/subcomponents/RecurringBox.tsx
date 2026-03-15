interface RecurringBoxProps {
  kwota: number;
  tytul: string;
  opis?: string | null;
  typ: 'wplyw' | 'wydatek';
  nastepny_termin: string;
  wlasciciel_konta?: string | null;
  konto?: string | null;
  metoda?: string;
  co_ile: string;
}

export default function RecurringBox({
  kwota,
  tytul,
  opis,
  wlasciciel_konta,
  konto,
  metoda,
  typ,
  nastepny_termin,
  co_ile,
}: RecurringBoxProps) {
  const durConv = function (co_ile: string) {
    switch (co_ile) {
      case 'P30D':
        return 'miesiac';
      case 'P7D':
        return 'tydzien';
      case 'P1Y':
        return 'rok';
    }
  };

  return (
    <div className='flex border-2 px-6 py-4 gap-2 flex-col my-4 w-9/10'>
      <div className='flex flex-row justify-between w-full'>
        <h2>{tytul}</h2>
        <div className='flex flex-col justify-start items-end'>
          <h2>Nastepny termin: {nastepny_termin}</h2>
          <p>Platne co {durConv(co_ile)}</p>
        </div>
      </div>
      <div className='flex items-center justify-between'>
        <h3 className={typ === 'wplyw' ? 'text-green-600' : 'text-red-600'}>
          {typ === 'wydatek' ? '-' : ''}
          {kwota} PLN
        </h3>
        <div className='flex flex-col justify-end items-end'>
          <p>{metoda == 'przelew' ? `Konto: ${konto}` : 'Platnosc gotowka'}</p>
          <p>
            {metoda == 'przelew' ? `Własciciel konta: ${wlasciciel_konta}` : ''}
          </p>
        </div>
      </div>
      <p>{opis ? opis : ''}</p>
    </div>
  );
}
