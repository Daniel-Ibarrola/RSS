import { useQuery } from '@tanstack/react-query';
import { getAlerts } from '@/lib/api.ts';

export const AlertsTable = () => {
  const {
    isPending,
    error,
    data: alerts,
  } = useQuery({
    queryKey: ['latestAlert'],
    queryFn: getAlerts,
  });

  if (isPending) return 'Loading...';

  if (error) return 'An error has occurred: ' + error.message;

  console.log(alerts);

  return <div>AlertsTable</div>;
};
