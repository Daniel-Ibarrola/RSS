import { useQuery } from '@tanstack/react-query';
import { getLatestAlert, LATEST_CAP_FILE_URL } from '@/lib/api.ts';
import { Spinner } from '@/components/ui/spinner.tsx';
import {
  Alert as ShadAlert,
  AlertDescription,
  AlertTitle,
} from '@/components/ui/alert.tsx';
import { AlertCircleIcon } from 'lucide-react';
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card.tsx';
import { Map } from '@/components/map/Map.tsx';
import { getAlertDescription } from '@/lib/alerts.ts';

/**
 * Component for displaying the latest CAP alert.
 * It includes a short description of the alert, and a map with the alert's location.
 */
export const MapCard = () => {
  const {
    isPending,
    error,
    data: alert,
  } = useQuery({
    queryKey: ['latestAlert'],
    queryFn: getLatestAlert,
  });

  if (isPending) return <Spinner />;

  if (error)
    return (
      <ShadAlert variant="destructive">
        <AlertCircleIcon />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </ShadAlert>
    );

  if (!alert) {
    console.error('No alert data available');
    return null;
  }

  return (
    <Card className="mx-auto w-full max-w-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <img
            src="/ciresFeedLogo2b.png"
            alt="CIRES Logo"
            className="object-contain"
          />
          <a
            className="text-blue-500 underline font-bold"
            href={LATEST_CAP_FILE_URL}
          >
            Último CAP
          </a>
        </CardTitle>
        <CardDescription>
          <p className="font-bold">{getAlertDescription(alert)}</p>
          <p>Severidad: {alert.is_event ? 'Menor' : 'Mayor'}</p>
        </CardDescription>
      </CardHeader>
      <Map alert={alert} />
    </Card>
  );
};
