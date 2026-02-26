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

  describe('Data fetching loading and error states', () => {
    it('renders loading state initially', () => {
      vi.mocked(getAlerts).mockReturnValue(new Promise(() => {}));

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      expect(screen.getByLabelText('Loading')).toBeInTheDocument();
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
            new RegExp(`Ha ocurrido un error: ${errorMessage}`, 'i'),
          ),
        ).toBeInTheDocument();
      });
    });
  });

  describe('Data Rendering', () => {
    it('Renders Headers', async () => {
      const mockAlerts: Alert[] = [];
      vi.mocked(getAlerts).mockResolvedValue(mockAlerts);

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByText('Fecha')).toBeInTheDocument();
      expect(screen.getByText('Estado(s)')).toBeInTheDocument();
      expect(screen.getByText('Region')).toBeInTheDocument();
      expect(screen.getByText('Tipo')).toBeInTheDocument();
      expect(screen.getByText('Archivo')).toBeInTheDocument();
    });

    it('renders alerts when data is fetched successfully', async () => {
      const mockAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42210,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];
      vi.mocked(getAlerts).mockResolvedValue(mockAlerts);

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByText('2026-02-24 07:46:20')).toBeInTheDocument();
      expect(screen.getByText('Oaxaca')).toBeInTheDocument();
      expect(screen.getByText('Oaxaca')).toBeInTheDocument();
      expect(screen.getByText('Evento')).toBeInTheDocument();
      expect(screen.getByText('20260224074620')).toBeInTheDocument();
    });
  });
});
