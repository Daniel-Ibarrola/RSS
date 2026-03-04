/**
 * @fileoverview API client for fetching alerts from the backend.
 */

import type { Alert } from '@/lib/alerts.ts';

const BASE_URL = '/api/v1';

/**
 * Response structure for the alerts list endpoint.
 */
interface AlertsResponse {
  alerts: Alert[];
  count: number;
  next: number | null;
  previous: number | null;
}

/**
 * Fetches a list of alerts from the API.
 *
 * @returns {Promise<AlertsResponse>} A promise that resolves to the alerts response.
 */
export async function getAlerts(): Promise<AlertsResponse> {
  const alertsUrl = BASE_URL + '/alerts/';
  const response = await fetch(alertsUrl);
  return await response.json();
}

/**
 * Fetches the latest alert from the API.
 *
 * @returns {Promise<Alert | null>} A promise that resolves to the latest alert or null.
 */
export async function getLatestAlert(): Promise<Alert | null> {
  const lastAlertUrl = BASE_URL + '/alerts/latest/';
  const response = await fetch(lastAlertUrl);
  return await response.json();
}
