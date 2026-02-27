import {
  forwardRef,
  useContext,
  useEffect,
  useImperativeHandle,
  useRef,
} from 'react';

import type { Ref } from 'react';
import { GoogleMapsContext } from '@vis.gl/react-google-maps';

type CircleEventProps = {
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
};

export type CircleProps = google.maps.CircleOptions & CircleEventProps;

export type CircleRef = Ref<google.maps.Circle | null>;

function useCircle(props: CircleProps) {
  const {
    onMouseOver,
    onMouseOut,
    ...circleOptions
  } = props;

  const circle = useRef<google.maps.Circle>(new google.maps.Circle());

  // update circleOptions (note the dependencies aren't properly checked
  // here, we just assume that setOptions is smart enough to not waste a
  // lot of time updating values that didn't change)
  useEffect(() => {
    circle.current.setOptions(circleOptions);
  }, [circleOptions]);

  const map = useContext(GoogleMapsContext)?.map;

  // create circle instance and add to the map once the map is available
  useEffect(() => {
    if (!map) {
      if (map === undefined)
        console.error('<Circle> has to be inside a Map component.');

      return;
    }

    const instance = circle.current;
    instance.setMap(map);

    return () => {
      instance.setMap(null);
    };
  }, [map]);

  // attach and re-attach event-handlers when any of the properties change
  useEffect(() => {
    const gme = google.maps.event;
    const instance = circle.current;

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

  return circle;
}

/**
 * Component to render a circle on a map
 */
export const Circle = forwardRef((props: CircleProps, ref: CircleRef) => {
  const circle = useCircle(props);

  useImperativeHandle(ref, () => circle.current);

  return null;
});
