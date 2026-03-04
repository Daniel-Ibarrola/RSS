import { STATES } from '@/lib/states.ts';
import { REGIONS } from '@/lib/regions.ts';

/**
 * Represents an alert or event in the system.
 */
export interface Alert {
  /** Unique identifier for the alert. */
  id: string;
  /** Whether the alert is an event. An event means that the earthquake didn't trigger the
   * early warning system.
   */
  is_event: boolean;
  /** References to other related alerts. */
  references: Alert[];
  /** The region ID where the alert originated. */
  region: number;
  /** List of state IDs covered by the alert. */
  states: number[];
  /** Timestamp of the alert. */
  time: string;
}

/**
 * Human-readable names for the type of alert.
 */
export enum EventType {
  Alert = 'Alerta',
  Event = 'Evento',
}

/**
 * Returns a human-readable description of the alert.
 * @param alert
 */
export const getAlertDescription = (alert: Alert) => {
  const date = new Date(alert.time);
  let dateStr = date.toLocaleDateString('es-MX', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    hour12: false,
  });
  dateStr = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
  const statesStr = alert.states.map((c) => STATES[c]).join('/');

  if (alert.is_event) {
    return `${dateStr} Sismo en ${REGIONS[alert.region]}.`;
  }
  return `${dateStr} Alerta en ${statesStr} por sismo en ${REGIONS[alert.region]}.`;
};
