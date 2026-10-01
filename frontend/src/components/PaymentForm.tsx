import type React from 'react';
import { useNavigate } from 'react-router';
import InputTemp from './subcomponents/InputTemp';
import ButtonTemp from './subcomponents/ButtonTemp';
import { useState, useEffect } from 'react';
import api from '../api';

interface Kategoria {
  category_id: number;
  category_name: string;
}

export default function PaymentForm() {
  const navigate = useNavigate();
  const [kategorie, setKategorie] = useState<Kategoria[]>([]);
  const [isRecurring, setRecurring] = useState<Boolean>(false);

  useEffect(() => {
    api
      .get('/categories')
      .then((response) => {
        setKategorie(response.data);
      })
      .catch((error) => console.log('Blad przy pobieraniu kategorii: ', error));
  }, []);

  const handleSubmit = async (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const formValues = Object.fromEntries(formData.entries());

    let payload = { ...formValues };
    delete payload.czy_powt;

    let endpoint = '/transactions';
    if (isRecurring) {
      endpoint = '/recurring';
      payload.nastepny_termin = formValues.data;
      delete payload.data;
    } else {
      delete payload.co_ile;
    }

    try {
      await api.post(`${endpoint}`, payload);
      navigate('/');
    } catch (error) {
      console.log('Blad polaczenia z API: ', error);
    }
  };

  return (
    <div className='flex flex-1 justify-center items-center min-w-full'>
      <form
        className='border-2 flex flex-col justify-center items-center px-12 py-6 gap-6'
        onSubmit={handleSubmit}
      >
        <h1>NOWA TRANSAKCJA</h1>
        <div className='flex flex-row justify-center items-start gap-6'>
          {/* Lewa strona */}
          <div className='flex flex-col justify-center items-center gap-6 min-h-full'>
            <InputTemp
              inpId='title'
              inpText='Tytul:'
              inpName='title'
              inpType='text'
            />

            <textarea
              name='description'
              id='description'
              placeholder='Opis:'
              required
              className='bg-neutral-800 border-2 border-white py-2 px-4 resize-none'
            ></textarea>

            <InputTemp
              inpId='account'
              inpText='Konto:'
              inpName='account'
              inpType='number'
              optional
            />

            <InputTemp
              inpId='account_owner'
              inpText='Wlasciciel Konta:'
              inpName='account_owner'
              inpType='text'
              optional
            />
          </div>

          {/* Prawa strona */}
          <div className='flex flex-col justify-center items-center gap-6'>
            <InputTemp
              inpId='transaction_date'
              inpText='Data:'
              inpName='transaction_date'
              inpType='date'
            />

            <InputTemp
              inpId='amount'
              inpText='Kwota:'
              inpName='amount'
              inpType='number'
            />

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_type'
                  id='expense'
                  value='expense'
                />
                <label htmlFor='expense'>Wydatek</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_type'
                  id='income'
                  value='income'
                />
                <label htmlFor='income'>Wplyw</label>
              </div>
            </div>

            <div className='flex gap-2'>
              <p>Kategoria:</p>
              <select
                name='category_id'
                id='category_id'
                className='border-2'
                required
              >
                <option value=''>---</option>
                {kategorie.map((item) => (
                  <option key={item.category_id} value={item.category_id}>
                    {item.category_name}
                  </option>
                ))}
              </select>
            </div>

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_method'
                  id='transfer'
                  value='transfer'
                />
                <label htmlFor='transfer'>Przelew</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_method'
                  id='cash'
                  value='cash'
                />
                <label htmlFor='cash'>Gotowka</label>
              </div>
            </div>
          </div>
        </div>
        <div className='flex justify-center flex-col gap-2 items-center'>
          <div className='flex justify-center items-center gap-2'>
            <input
              type='checkbox'
              name='czy_powt'
              onChange={(e) => setRecurring(e.target.checked)}
            />
            <label htmlFor='czy_powt'>Czy powtarzalna?</label>
          </div>
          <select
            name='interval'
            id='interval'
            className={isRecurring ? 'border-2' : 'hidden'}
          >
            <option value='' disabled>
              Co ile?
            </option>
            <option value='P7D'>Tydzien</option>
            <option value='P30D'>Miesiac</option>
            <option value='P1Y'>Rok</option>
          </select>
        </div>
        <ButtonTemp btnText='ZAPISZ' btnType='submit' />
      </form>
    </div>
  );
}
