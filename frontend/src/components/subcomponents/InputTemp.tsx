interface InputTempProps {
  inpType: string;
  inpText: string;
  inpId: string;
  inpName: string;
  optional?: boolean;
}

export default function InputTemp({
  inpType,
  inpText,
  inpId,
  inpName,
  optional,
}: InputTempProps) {
  return (
    <input
      type={inpType}
      placeholder={inpText}
      id={inpId}
      name={inpName}
      required={!optional}
      className='bg-neutral-800 border-2 border-white py-2 px-4'
    />
  );
}
