import NavbarButton from './subcomponents/NavbarButton';
import NavbarLink from './subcomponents/NavbarLink';
import { useNavigate } from 'react-router';

export default function Navbar() {
  const navigate = useNavigate();

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
          <NavbarLink
            linkText='LINK 1'
            linkClick={() => console.log('Link 1')}
          />
          <NavbarLink
            linkText='LINK 2'
            linkClick={() => console.log('Link 2')}
          />
          <NavbarLink
            linkText='LINK 3'
            linkClick={() => console.log('Link 3')}
          />
        </div>
        {/* Buttony */}
        <div className='flex items-center justify-center'>
          <NavbarButton btnText='LOG IN' btnClick={() => navigate('/login')} />
        </div>
      </div>
    </div>
  );
}
