import InputTemp from './subcomponents/InputTemp';
import ButtonTemp from './subcomponents/ButtonTemp';

export default function RegisterForm() {
  return (
    <div className=' min-w-full flex flex-1 justify-center items-center'>
      <div className='border-2 flex flex-col justify-center items-center px-12 py-6 gap-6 '>
        <h1 className='font-bold text-2xl'>REJESTRACJA</h1>
        <InputTemp
          inpType='text'
          inpText='Imie::'
          inpId='imie'
          inpName='imie'
        />
        <InputTemp
          inpType='text'
          inpText='Nazwisko:'
          inpId='nazwisko'
          inpName='nazwisko'
        />
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
          btnClick={() => console.log('SignIN!!!')}
          btnText='Zarejestruj'
          btnType='submit'
        />
        <div></div>
      </div>
    </div>
  );
}
