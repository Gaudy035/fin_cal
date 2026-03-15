import InputTemp from './subcomponents/InputTemp';
import ButtonTemp from './subcomponents/ButtonTemp';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function LoginForm() {
  const navigate = useNavigate();

  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    const formData = new FormData(event.currentTarget);
    const formValues = Object.fromEntries(formData.entries());

    const payload = {
      imie: '',
      nazwisko: '',
      ...formValues,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        navigate('/');
      } else {
        setError(data.detail || 'Wystapil blad logowania');
      }
    } catch (err) {
      setError('Blad polaczenia z API');
    }
  };

  return (
    <div className=' min-w-full flex flex-1 justify-center items-center'>
      <form
        className='border-2 flex flex-col justify-center items-center px-12 py-6 gap-6'
        onSubmit={handleSubmit}
      >
        <h1 className='font-bold text-2xl'>LOG IN</h1>
        <InputTemp
          inpType='email'
          inpText='Email:'
          inpId='email'
          inpName='email'
        />
        <InputTemp
          inpType='password'
          inpText='Haslo:'
          inpId='haslo'
          inpName='haslo'
        />
        <ButtonTemp
          // btnClick={() => handleSubmit}
          btnText='LOG-IN'
          btnType='submit'
        />
        <div className='flex justify-center items-center flex-col'>
          <h2 className='text-red-600'>{error ? error : ''}</h2>
          <h2>Nie masz konta?</h2>{' '}
          <a
            className='underline cursor-pointer'
            onClick={() => navigate('/rejestracja')}
          >
            Zarejestruj sie
          </a>
        </div>
      </form>
    </div>
  );
}
