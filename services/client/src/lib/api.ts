import type { Alert } from '@/lib/alerts.ts';

const BASE_URL = '/api/v1';

interface AlertsResponse {
  alerts: Alert[];
  count: number;
  next: number | null;
  previous: number | null;
}

export async function getAlerts(): Promise<AlertsResponse> {
  const alertsUrl = BASE_URL + '/alerts/';
  const response = await fetch(alertsUrl);
  return await response.json();
}

export async function getLatestAlert(): Promise<Alert | null> {
  const lastAlertUrl = BASE_URL + '/alerts/latest/';
  const response = await fetch(lastAlertUrl);
  return await response.json();
}
