interface InputTempProps {
  inpType: string;
  inpText: string;
  inpId: string;
  inpName: string;
}

export default function InputTemp({
  inpType,
  inpText,
  inpId,
  inpName,
}: InputTempProps) {
  return (
    <input
      type={inpType}
      placeholder={inpText}
      id={inpId}
      name={inpName}
      required
      className='bg-neutral-800 border-2 border-white py-2 px-4'
    />
  );
}
