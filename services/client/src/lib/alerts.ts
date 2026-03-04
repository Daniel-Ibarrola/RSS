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
