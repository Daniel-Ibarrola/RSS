import { useQuery } from '@tanstack/react-query';
import { getLatestAlert } from '@/lib/api.ts';
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
        <CardTitle>Último CAP</CardTitle>
        <CardDescription>
          <p>{alert.time}</p>
          <p>Severidad: menor</p>
        </CardDescription>
      </CardHeader>
      <Map alert={alert} />
    </Card>
  );
};
