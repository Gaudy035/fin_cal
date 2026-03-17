import { useNavigate } from 'react-router';
import ButtonTemp from './ButtonTemp';

interface UserSettingsProps {
  visibility: boolean;
  change: () => void;
}

export default function UserSettings({
  visibility,
  change,
}: UserSettingsProps) {
  const navigate = useNavigate();

  const logOut = () => {
    change();
    localStorage.removeItem('token');
    navigate('/');
    window.location.reload();
  };

  if (visibility) {
    return (
      <>
        <div
          className='max-h-full min-w-full fixed inset-0 z-10'
          onClick={change}
        ></div>
        <div
          className=' flex flex-col justify-center items-center px-6 py-6 gap-6 border-2 absolute top-full right-0 min-w-max bg-neutral-800 z-20'
          onClick={(e) => e.stopPropagation()}
        >
          <ButtonTemp
            reverse
            btnType='button'
            btnText='Zmien email'
            btnClick={() => console.log('wip')}
          />
          <ButtonTemp
            reverse
            btnType='button'
            btnText='Zmien haslo'
            btnClick={() => console.log('wip')}
          />

          <ButtonTemp
            btnText='LOG-OUT'
            btnType='button'
            btnClick={() => logOut()}
          />
        </div>
      </>
    );
  } else {
    return null;
  }
}
