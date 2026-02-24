import { useQuery } from '@tanstack/react-query';
import { getLatestAlert } from '@/lib/api.ts';
import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';

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

  return (
    <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string}>
      <GoogleMap
        className="w-80 h-80"
        defaultCenter={{ lat: 22.54992, lng: 0 }}
        defaultZoom={3}
        gestureHandling="greedy"
        disableDefaultUI
      />
    </APIProvider>
  );
};
