interface NavbarButtonProps {
  btnClick: () => void;
  btnText: string;
}

export default function NavbarButton({ btnClick, btnText }: NavbarButtonProps) {
  return (
    <button
      type='button'
      onClick={btnClick}
      className='border-2 border-white bg-white text-neutral-800 px-2 py-1 font-semibold cursor-pointer hover:bg-neutral-800 hover:text-white'
    >
      {btnText}
    </button>
  );
}
