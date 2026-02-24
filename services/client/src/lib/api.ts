import type { Alert } from '@/lib/alerts.ts';

const BASE_URL = '/api/v1';

export async function getAlerts(): Promise<Alert[]> {
  const alertsUrl = BASE_URL + '/alerts/';
  const response = await fetch(alertsUrl);
  return await response.json();
}

export async function getLatestAlert(): Promise<Alert | null> {
  const lastAlertUrl = BASE_URL + '/alerts/latest/';
  const response = await fetch(lastAlertUrl);
  return await response.json();
}
