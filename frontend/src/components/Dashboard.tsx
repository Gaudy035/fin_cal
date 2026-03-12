import RightPanel from './Dashboard/RightPanel';
import LeftPanel from './Dashboard/LeftPanel';

export default function Dashboard() {
  return (
    <div className='flex flex-row min-w-full min-h-full flex-1 justify-center  gap-3 p-4'>
      <LeftPanel />
      <RightPanel />
    </div>
  );
}
