import '@testing-library/jest-dom';

import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AlertsTable } from './AlertsTable';
import { getAlerts } from '@/lib/api';
import { type Alert } from '@/lib/alerts';

// Mock the API module
vi.mock('@/lib/api', () => ({
  getAlerts: vi.fn(),
}));

const mockAlerts: Alert[] = [
  {
    id: 'alert-1',
    is_event: false,
    references: [],
    region: 1,
    states: [10, 20],
    time: '2026-02-24T12:00:00Z',
  },
  {
    id: 'alert-2',
    is_event: true,
    references: [],
    region: 2,
    states: [30],
    time: '2026-02-24T13:00:00Z',
  },
];

describe('AlertsTable', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(getAlerts).mockReturnValue(new Promise(() => {}));

    render(
      <QueryClientProvider client={queryClient}>
        <AlertsTable />
      </QueryClientProvider>,
    );

    expect(screen.getByText(/loading.../i)).toBeInTheDocument();
  });

  it('renders alerts when data is fetched successfully', async () => {
    vi.mocked(getAlerts).mockResolvedValue(mockAlerts);

    render(
      <QueryClientProvider client={queryClient}>
        <AlertsTable />
      </QueryClientProvider>,
    );

    await waitFor(() => {
      expect(screen.queryByText(/loading.../i)).not.toBeInTheDocument();
    });

    expect(screen.getByText('alert-1')).toBeInTheDocument();
    expect(screen.getByText('alert-2')).toBeInTheDocument();
  });

  it('renders error message on failure', async () => {
    const errorMessage = 'Failed to fetch';
    vi.mocked(getAlerts).mockRejectedValue(new Error(errorMessage));

    render(
      <QueryClientProvider client={queryClient}>
        <AlertsTable />
      </QueryClientProvider>,
    );

    await waitFor(() => {
      expect(
        screen.getByText(
          new RegExp(`An error has occurred: ${errorMessage}`, 'i'),
        ),
      ).toBeInTheDocument();
    });
  });
});
