import { useQuery } from '@tanstack/react-query';
import { getAlerts } from '@/lib/api.ts';

export const AlertsTable = () => {
  const {
    isPending,
    error,
    data: alerts,
  } = useQuery({
    queryKey: ['alerts'],
    queryFn: getAlerts,
  });

  if (isPending) return 'Loading...';

  if (error) return 'An error has occurred: ' + error.message;

  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      {alerts?.map((alert) => (
        <div key={alert.id}>{alert.id}</div>
      ))}
    </div>
  );
};
