import type React from 'react';
import { useNavigate } from 'react-router';
import InputTemp from './subcomponents/InputTemp';
import ButtonTemp from './subcomponents/ButtonTemp';
import { useState, useEffect } from 'react';

interface Kategoria {
  id_kategorii: number;
  nazwa: string;
}

export default function PaymentForm() {
  const navigate = useNavigate();
  const [kategorie, setKategorie] = useState<Kategoria[]>([]);
  const userId = localStorage.getItem('user_id');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/kategorie')
      .then((response) => response.json())
      .then((data: Kategoria[]) => setKategorie(data))
      .catch((error) => console.log('Blad przy pobieraniu kategorii: ', error));
  }, []);

  const handleSubmit = async (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const formValues = Object.fromEntries(formData.entries());

    const payload = { id_uzytkownika: userId, ...formValues };

    try {
      const response = await fetch('http://127.0.0.1:8000/add_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        navigate('/');
      }
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
              inpId='tytul'
              inpText='Tytul:'
              inpName='tytul'
              inpType='text'
            />

            <textarea
              name='opis'
              id='opis'
              placeholder='Opis:'
              required
              className='bg-neutral-800 border-2 border-white py-2 px-4 resize-none'
            ></textarea>

            <InputTemp
              inpId='konto'
              inpText='Konto:'
              inpName='konto'
              inpType='number'
              optional
            />

            <InputTemp
              inpId='wlasciciel_konta'
              inpText='Wlasciciel Konta:'
              inpName='wlasciciel_konta'
              inpType='text'
              optional
            />
          </div>

          {/* Prawa strona */}
          <div className='flex flex-col justify-center items-center gap-6'>
            <InputTemp
              inpId='kwota'
              inpText='Kwota:'
              inpName='kwota'
              inpType='number'
            />

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input type='radio' name='typ' id='wydatek' value='wydatek' />
                <label htmlFor='wydatek'>Wydatek</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input type='radio' name='typ' id='wplyw' value='wplyw' />
                <label htmlFor='wplyw'>Wplyw</label>
              </div>
            </div>

            <div className='flex gap-2'>
              <p>Kategoria:</p>
              <select
                name='id_kategorii'
                id='id_kategorii'
                className='border-2'
                required
              >
                <option value=''>---</option>
                {kategorie.map((item) => (
                  <option value={item.id_kategorii}>{item.nazwa}</option>
                ))}
              </select>
            </div>

            <div className='flex justify-between items-center min-w-full px-2'>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='metoda'
                  id='przelew'
                  value='przelew'
                />
                <label htmlFor='przelew'>Przelew</label>
              </div>
              <div className='flex gap-2 justify-center items-center'>
                <input
                  type='radio'
                  name='metoda'
                  id='gotowka'
                  value='gotowka'
                />
                <label htmlFor='gotowka'>Gotowka</label>
              </div>
            </div>
          </div>
        </div>
        <ButtonTemp btnText='ZAPISZ' btnType='submit' />
      </form>
    </div>
  );
}
