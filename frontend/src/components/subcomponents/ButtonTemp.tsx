interface ButtonTempProps {
  btnClick?: () => void;
  btnText: string;
  btnType: 'button' | 'submit';
}

export default function ButtonTemp({
  btnClick,
  btnText,
  btnType,
}: ButtonTempProps) {
  return (
    <button
      type={btnType}
      onClick={btnClick}
      className='border-2 border-white bg-white text-neutral-800 px-2 py-1 font-semibold cursor-pointer hover:bg-neutral-800 hover:text-white'
    >
      {btnText}
    </button>
  );
}
