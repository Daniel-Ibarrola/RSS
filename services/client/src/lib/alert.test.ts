import { describe, expect, it } from 'vitest';
import { type Alert, getAlertDescription } from '@/lib/alerts.ts';

describe('getAlertDescription', () => {
  it('Gets correct description for alerts of single state', () => {
    const alert: Alert = {
      id: '20230525000000',
      is_event: false,
      references: [],
      region: 41204,
      states: [40],
      time: '2023-05-25T00:00:00',
    };

    const title = getAlertDescription(alert);
    expect(title).toBe(
      'Jueves, 25 de mayo de 2023, 00:00:00 Alerta en CDMX por sismo en Guerrero.',
    );
  });

  it('Gets alert title for alerts of multiple states', () => {
    const alert: Alert = {
      id: '20230525000000',
      is_event: false,
      references: [],
      region: 41204,
      states: [40, 46],
      time: '2023-05-25T00:00:00',
    };

    const title = getAlertDescription(alert);
    expect(title).toBe(
      'Jueves, 25 de mayo de 2023, 00:00:00 Alerta en CDMX/Puebla por sismo en Guerrero.',
    );
  });

  it('Gets alert title for events', () => {
    const alert: Alert = {
      id: '20230525000000',
      is_event: true,
      references: [],
      region: 41204,
      states: [40],
      time: '2023-05-25T00:00:00',
    };

    const title = getAlertDescription(alert);
    expect(title).toBe(
      'Jueves, 25 de mayo de 2023, 00:00:00 Sismo en Guerrero.',
    );
  });
});
