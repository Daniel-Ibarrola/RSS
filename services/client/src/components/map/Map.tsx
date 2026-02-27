import { useQuery } from '@tanstack/react-query';
import { getLatestAlert } from '@/lib/api.ts';
import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';
import type { Coords } from '@/lib/coords.ts';
import { regionCoords } from '@/lib/coords.ts';
import { Circle } from '@/components/map/circle.tsx';
import { Polygon } from '@/components/map/polygon.tsx';
import { statePolygons } from '@/lib/polygons.ts';

const center: Coords = { lat: 19.4287, lng: -99.12766 }; // centers the map in Mexico

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

  const alertCoords = alert?.region ? regionCoords[alert.region] : null;
  const showCircle = alert?.is_event && alertCoords;
  const showPolygons = !alert?.is_event && alert?.states;

  return (
    <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string}>
      <GoogleMap
        className="w-80 h-80"
        defaultCenter={center}
        defaultZoom={6}
        gestureHandling="greedy"
        disableDefaultUI
      >
        {showCircle && (
          <Circle
            radius={50000}
            center={alertCoords}
            strokeColor={'#0c4cb3'}
            strokeOpacity={1}
            strokeWeight={3}
            fillColor={'#3b82f6'}
            fillOpacity={0.3}
          />
        )}
        {showPolygons &&
          alert.states.map((stateId) => {
            const polygonCoords = statePolygons[stateId];
            if (!polygonCoords) return null;

            return (
              <Polygon
                key={stateId}
                paths={polygonCoords}
                strokeColor={'#0c4cb3'}
                strokeOpacity={1}
                strokeWeight={3}
                fillColor={'#3b82f6'}
                fillOpacity={0.3}
              />
            );
          })}
      </GoogleMap>
    </APIProvider>
  );
};
