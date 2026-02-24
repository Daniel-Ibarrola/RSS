import { useQuery } from '@tanstack/react-query';
import { getLatestAlert } from '@/lib/api.ts';

export const Map = () => {
  const {
    isPending,
    error,
    data: alert,
  } = useQuery({
    queryKey: ['latestAlert'],
    queryFn: getLatestAlert,
  });

  if (isPending) return 'Loading...';

  if (error) return 'An error has occurred: ' + error.message;

  console.log(alert);

  return <div>Map</div>;
};
