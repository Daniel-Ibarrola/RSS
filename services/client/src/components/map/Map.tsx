import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';
import type { Coords } from '@/lib/coords.ts';
import { regionCoords } from '@/lib/coords.ts';
import { Circle } from '@/components/map/Circle.tsx';
import { Polygon } from '@/components/map/Polygon.tsx';
import { statePolygons } from '@/lib/polygons.ts';
import type { Alert } from '@/lib/alerts.ts';

/**
 * Default center coordinates for the map (Mexico City).
 */
const center: Coords = { lat: 19.4287, lng: -99.12766 };

interface MapProps {
  alert: Alert;
}

/**
 * Component that renders a Google Map to display alert information.
 * Shows a circle if it's an event (e.g., earthquake epicenter) or polygons
 * if it's a general alert covering multiple states.
 *
 * @returns {JSX.Element | null} The rendered Map component or null if no data.
 */
export const Map = ({ alert }: MapProps) => {
  const alertCoords = alert.region ? regionCoords[alert.region] : null;
  const showCircle = alert.is_event && alertCoords;
  const showPolygons = !alert.is_event && alert.states;

  return (
    <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string}>
      <GoogleMap
        className="h-80 w-full p-2"
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
