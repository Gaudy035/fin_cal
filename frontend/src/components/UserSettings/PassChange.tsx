import { useNavigate } from 'react-router';
import { useState, type SyntheticEvent } from 'react';
import ButtonTemp from '../subcomponents/ButtonTemp';
import InputTemp from '../subcomponents/InputTemp';

export default function PassChange() {
  const token = localStorage.getItem('token');
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  const handleSubmit = async (event: SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    const formData = new FormData(event.currentTarget);
    const formValues = Object.fromEntries(formData.entries());
    const payload = { ...formValues };

    try {
      const response = await fetch('http://127.0.0.1:8000/update_password', {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => {
          navigate('/');
          localStorage.removeItem('token');
        }, 1500);
      } else setError(data.detail);
    } catch (err) {
      console.log('Blad polaczenia z API', err);
    }
  };

  return (
    <div className='flex flex-1 min-w-full min-h-full justify-center items-center'>
      <form
        onSubmit={handleSubmit}
        className='flex flex-col border-2 py-6 px-12 gap-6 justify-center items-center'
      >
        <h1 className='font-bold text-2xl'>Zmiana hasla</h1>
        <InputTemp
          inpId='new_pass'
          inpName='new_pass'
          inpText='Nowe haslo:'
          inpType='password'
        />
        <InputTemp
          inpId='current_pass'
          inpName='current_pass'
          inpText='Aktualne haslo:'
          inpType='password'
        />
        <ButtonTemp btnText='ZAPISZ' btnType='submit' />
        <p className={success ? 'text-green-600' : 'text-red-600'}>
          {success ? 'Zmiana hasla pomyslna' : ''}
          {error ? error : ''}
        </p>
      </form>
    </div>
  );
}
