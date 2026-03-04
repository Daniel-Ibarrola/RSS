import {
  forwardRef,
  useContext,
  useEffect,
  useImperativeHandle,
  useRef,
} from 'react';

import type { Ref } from 'react';
import { GoogleMapsContext } from '@vis.gl/react-google-maps';

type PolygonEventProps = {
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
};

export type PolygonProps = google.maps.PolygonOptions & PolygonEventProps;

export type PolygonRef = Ref<google.maps.Polygon | null>;

function usePolygon(props: PolygonProps) {
  const {
    onMouseOver,
    onMouseOut,
    ...polygonOptions
  } = props;

  const polygon = useRef<google.maps.Polygon>(new google.maps.Polygon());

  // update polygonOptions (note the dependencies aren't properly checked
  // here, we just assume that setOptions is smart enough to not waste a
  // lot of time updating values that didn't change)
  useEffect(() => {
    polygon.current.setOptions(polygonOptions);
  }, [polygonOptions]);

  const map = useContext(GoogleMapsContext)?.map;

  // create polygon instance and add to the map once the map is available
  useEffect(() => {
    if (!map) {
      if (map === undefined)
        console.error('<Polygon> has to be inside a Map component.');

      return;
    }

    const instance = polygon.current;
    instance.setMap(map);

    return () => {
      instance.setMap(null);
    };
  }, [map]);

  // attach and re-attach event-handlers when any of the properties change
  useEffect(() => {
    const gme = google.maps.event;
    const instance = polygon.current;

    const listeners = [
      gme.addListener(instance, 'mouseover', (e: google.maps.MapMouseEvent) => {
        onMouseOver?.(e);
      }),
      gme.addListener(instance, 'mouseout', (e: google.maps.MapMouseEvent) => {
        onMouseOut?.(e);
      }),
    ];

    return () => {
      listeners.forEach(listener => listener.remove());
    };
  }, [onMouseOver, onMouseOut]);

  return polygon;
}

/**
 * Component to render a polygon on a map
 */
export const Polygon = forwardRef((props: PolygonProps, ref: PolygonRef) => {
  const polygon = usePolygon(props);

  useImperativeHandle(ref, () => polygon.current);

  return null;
});
