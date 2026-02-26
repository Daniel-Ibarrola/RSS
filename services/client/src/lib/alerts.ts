export interface Alert {
  id: string;
  is_event: boolean;
  references: Alert[];
  region: number;
  states: number[];
  time: string;
}

export enum EventType {
  Alert = 'Alerta',
  Event = 'Evento',
}
