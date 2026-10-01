import { useNavigate, useLocation } from 'react-router';
import InputTemp from './subcomponents/InputTemp';
import ButtonTemp from './subcomponents/ButtonTemp';
import { useState, useEffect, type SyntheticEvent } from 'react';
import api from '../api';

interface Kategoria {
  category_id: number;
  category_name: string;
}

export default function RecurringForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const editData = location.state;
  const [kategorie, setKategorie] = useState<Kategoria[]>([]);

  useEffect(() => {
    api
      .get('/categories')
      .then((response) => setKategorie(response.data))
      .catch((error) => console.log('Blad przy pobieraniu kategorii: ', error));
  }, []);

  const handleSubmit = async (event: SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const formValues = Object.fromEntries(formData.entries());
    const payload = {
      ...formValues,
      czy_aktywna: formData.get('czy_aktywna') === 'on',
    };

    try {
      await api.put(`/recurring/${editData.id_t_powtarzalnej}`, payload);
      navigate('/kalendarz');
    } catch (error) {
      console.log('Blad polaczenia z API', error);
    }
  };

  return (
    <div className='flex flex-1 justify-center items-center min-w-full'>
      <form
        className='border-2 flex flex-col justify-center items-center px-12 py-6 gap-6'
        onSubmit={handleSubmit}
      >
        <h1>MODYFIKUJ TRANSAKCJE</h1>
        <div className='flex flex-row justify-center items-start gap-6'>
          {/* Lewa strona */}
          <div className='flex flex-col justify-center items-center gap-6 min-h-full'>
            <InputTemp
              inpId='title'
              inpText='Tytul:'
              inpName='title'
              inpType='text'
              inpVal={editData?.title}
            />

            <textarea
              name='description'
              id='description'
              placeholder='Opis:'
              required
              className='bg-neutral-800 border-2 border-white py-2 px-4 resize-none'
              defaultValue={editData?.description}
            ></textarea>

            <InputTemp
              inpId='account'
              inpText='Konto:'
              inpName='account'
              inpType='number'
              inpVal={editData?.account}
              optional
            />

            <InputTemp
              inpId='account_owner'
              inpText='Wlasciciel Konta:'
              inpName='account_owner'
              inpType='text'
              inpVal={editData?.account_owner}
              optional
            />
          </div>

          {/* Prawa strona */}
          <div className='flex flex-col justify-center items-center gap-6'>
            <InputTemp
              inpId='next_date'
              inpText='Nastepny termin:'
              inpName='next_date'
              inpType='date'
              inpVal={editData?.next_date}
            />

            <InputTemp
              inpId='amount'
              inpText='Kwota:'
              inpName='amount'
              inpType='number'
              inpVal={editData?.amount}
            />

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_type'
                  id='expense'
                  value='expense'
                  defaultChecked={editData?.transaction_type === 'expense'}
                />
                <label htmlFor='expense'>Wydatek</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='transaction_type'
                  id='income'
                  value='income'
                  defaultChecked={editData?.transaction_type === 'income'}
                />
                <label htmlFor='income'>Wplyw</label>
              </div>
            </div>

            <div className='flex gap-2'>
              <p>Kategoria:</p>
              {kategorie.length > 0 ? (
                <select
                  defaultValue={editData?.category_id}
                  name='category_id'
                  id='category_id'
                  className='border-2'
                  required
                >
                  <option value='' disabled>
                    ---
                  </option>
                  {kategorie.map((item) => (
                    <option key={item.category_id} value={item.category_id}>
                      {item.category_name}
                    </option>
                  ))}
                </select>
              ) : (
                'Ładownie...'
              )}
            </div>

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  defaultChecked={editData?.transaction_method === 'przelew'}
                  type='radio'
                  name='metoda'
                  id='transfer'
                  value='transfer'
                />
                <label htmlFor='transfer'>Przelew</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  defaultChecked={editData?.transaction_method === 'gotowka'}
                  type='radio'
                  name='metoda'
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
              name='is_active'
              defaultChecked={editData?.is_active === true}
            />
            <label htmlFor='is_active'>Czy aktywna?</label>
          </div>
          <select
            name='interval'
            id='interval'
            className='border-2'
            defaultValue={editData?.interval}
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
