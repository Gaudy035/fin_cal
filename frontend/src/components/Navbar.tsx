import ButtonTemp from './subcomponents/ButtonTemp';
import NavbarLink from './subcomponents/NavbarLink';
import { useNavigate } from 'react-router';

export default function Navbar() {
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem('user_id');

  const logOut = () => {
    localStorage.removeItem('user_id');
    window.location.reload();
  };

  return (
    <div className='px-4 pt-4'>
      <div className='flex flex-row w-full justify-between items-center px-12 h-20 border-2'>
        {/* Logo */}
        <div>
          <h1
            onClick={() => navigate('/')}
            className='font-semibold cursor-pointer'
          >
            LOGO
          </h1>
        </div>
        {/* Linki */}
        <div className='flex items-center gap-12 justify-center'>
          <NavbarLink linkText='DASHBOARD' linkClick={() => navigate('/')} />
          <NavbarLink
            linkText='KALENDARZ'
            linkClick={() => console.log('Link 2')}
          />
          <NavbarLink
            linkText='WYKRESY'
            linkClick={() => console.log('Link 3')}
          />
        </div>
        {/* Buttony */}
        <div className='flex items-center justify-center'>
          <ButtonTemp
            btnText={isLoggedIn ? 'LOG-OUT' : 'LOG-IN'}
            btnClick={isLoggedIn ? () => logOut() : () => navigate('/login')}
            btnType='button'
          />
        </div>
      </div>
    </div>
  );
}
