import '@testing-library/jest-dom';

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AlertsTable } from './AlertsTable';
import { getAlerts } from '@/lib/api';
import { type Alert } from '@/lib/alerts';

// Mock the API module
vi.mock('@/lib/api', () => ({
  getAlerts: vi.fn(),
  getCapFileUrl: vi.fn(),
}));

vi.mock('@/components/ui/range-picker.tsx', () => ({
  DatePickerWithRange: ({
    id,
    onDateChange,
  }: {
    id: string;
    onDateChange?: (range: { from: Date; to: Date }) => void;
  }) => (
    <button
      aria-label="Fecha"
      id={id}
      onClick={() =>
        onDateChange?.({
          from: new Date('2026-02-24'),
          to: new Date('2026-02-25'),
        })
      }
      type="button"
    >
      Fecha
    </button>
  ),
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
          screen.getByText(new RegExp(`${errorMessage}`, 'i')),
        ).toBeInTheDocument();
      });
    });
  });

  describe('Data Rendering', () => {
    it('renders alerts when data is fetched successfully', async () => {
      const mockAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];
      vi.mocked(getAlerts).mockResolvedValue({
        alerts: mockAlerts,
        count: 1,
        next: null,
        prev: null,
      });

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
      expect(screen.getByText('Oax Centro')).toBeInTheDocument();
      expect(screen.getByText('Evento')).toBeInTheDocument();
      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
    });
  });

  describe('Filters', () => {
    it('renders filter controls', async () => {
      vi.mocked(getAlerts).mockResolvedValue({
        alerts: [],
        count: 0,
        next: null,
        prev: null,
      });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByLabelText('Fecha')).toBeInTheDocument();
      expect(screen.getByLabelText('Estado')).toBeInTheDocument();
      expect(screen.getByLabelText('Región')).toBeInTheDocument();
      expect(screen.getByLabelText('Tipo')).toBeInTheDocument();
    });

    it('filters by date range', async () => {
      const user = userEvent.setup();
      vi.mocked(getAlerts).mockResolvedValue({
        alerts: [],
        count: 0,
        next: null,
        prev: null,
      });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      // Open date picker
      const dateButton = screen.getByLabelText('Fecha');
      const applyButton = screen.getByText('Aplicar');
      await user.click(dateButton);
      await user.click(applyButton);

      await waitFor(() => {
        expect(vi.mocked(getAlerts)).toHaveBeenLastCalledWith(1, {
          endDate: '2026-02-24',
          region: undefined,
          startDate: '2026-02-23',
          state: undefined,
          type: undefined,
        });
      });
    });

    it('filters by state', async () => {
      const user = userEvent.setup();
      const allAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42], // Oaxaca
          time: '2026-02-24T07:46:20',
        },
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 41201,
          states: [41], // Guerrero
          time: '2026-02-23T12:34:56',
        },
      ];

      const filteredAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: allAlerts,
          count: 2,
          next: null,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: filteredAlerts,
          count: 1,
          next: null,
          prev: null,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      // Both alerts should be visible initially
      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
      expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();

      const stateSelect = screen.getByLabelText('Estado');
      await user.click(stateSelect);

      // Select Oaxaca (state 42)
      const oaxacaOption = screen.getByRole('option', { name: 'Oaxaca' });
      await user.click(oaxacaOption);

      const applyButton = screen.getByText('Aplicar');
      await user.click(applyButton);

      // After filtering, only Oaxaca alert should remain
      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
        expect(
          screen.queryByText('20260223123456.cap'),
        ).not.toBeInTheDocument();
      });
    });

    it('filters by region', async () => {
      const user = userEvent.setup();
      const allAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237, // Oax Centro
          states: [42],
          time: '2026-02-24T07:46:20',
        },
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 41201, // Petatlan Gro
          states: [41],
          time: '2026-02-23T12:34:56',
        },
      ];

      const filteredAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: allAlerts,
          count: 2,
          next: null,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: filteredAlerts,
          count: 1,
          next: null,
          prev: null,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      // Both alerts should be visible initially
      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
      expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();

      const regionSelect = screen.getByLabelText('Región');
      await user.click(regionSelect);

      // Select Oax Centro
      const regionOption = screen.getByRole('option', { name: 'Oax Centro' });
      await user.click(regionOption);

      const applyButton = screen.getByText('Aplicar');
      await user.click(applyButton);

      // After filtering, only Oax Centro alert should remain
      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
        expect(
          screen.queryByText('20260223123456.cap'),
        ).not.toBeInTheDocument();
      });
    });

    it('filters by type', async () => {
      const user = userEvent.setup();
      const allAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-23T12:34:56',
        },
      ];

      const filteredAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: allAlerts,
          count: 2,
          next: null,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: filteredAlerts,
          count: 1,
          next: null,
          prev: null,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      // Both alerts should be visible initially
      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
      expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();

      const typeSelect = screen.getByLabelText('Tipo');
      await user.click(typeSelect);

      // Select Event
      const eventOption = screen.getByRole('option', { name: 'Evento' });
      await user.click(eventOption);

      const applyButton = screen.getByText('Aplicar');
      await user.click(applyButton);

      // After filtering, only event should remain
      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
        expect(
          screen.queryByText('20260223123456.cap'),
        ).not.toBeInTheDocument();
      });
    });

    it('clears filters', async () => {
      const user = userEvent.setup();
      const allAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-23T12:34:56',
        },
      ];

      const filteredAlerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: allAlerts,
          count: 2,
          next: null,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: filteredAlerts,
          count: 1,
          next: null,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: allAlerts,
          count: 2,
          next: null,
          prev: null,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      // Both alerts should be visible initially
      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
      expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();

      // Apply a filter
      const typeSelect = screen.getByLabelText('Tipo');
      await user.click(typeSelect);
      const eventOption = screen.getByRole('option', { name: 'Evento' });
      await user.click(eventOption);
      const applyButton = screen.getByText('Aplicar');
      await user.click(applyButton);

      // Only one alert should be visible after filtering
      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
        expect(
          screen.queryByText('20260223123456.cap'),
        ).not.toBeInTheDocument();
      });

      // Clear filters
      const clearButton = screen.getByText('Limpiar');
      await user.click(clearButton);

      // Both alerts should be visible again
      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
        expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();
      });
    });
  });

  describe('Pagination', () => {
    it('disables previous button on first page', async () => {
      vi.mocked(getAlerts).mockResolvedValue({
        alerts: [],
        count: 0,
        next: 2,
        prev: null,
      });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      const prevButton = screen.getByLabelText('pagina anterior');
      expect(prevButton).toHaveClass('pointer-events-none opacity-50');
    });

    it('disables next button on last page', async () => {
      vi.mocked(getAlerts).mockResolvedValue({
        alerts: [],
        count: 0,
        next: null,
        prev: 1,
      });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      const nextButton = screen.getByLabelText('siguiente pagina');
      expect(nextButton).toHaveClass('pointer-events-none opacity-50');
    });

    it('navigates to next page when next button is clicked', async () => {
      const user = userEvent.setup();
      const page1Alerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];
      const page2Alerts: Alert[] = [
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-23T12:34:56',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: page1Alerts,
          count: 2,
          next: 2,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: page2Alerts,
          count: 2,
          next: null,
          prev: 1,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();

      const nextButton = screen.getByLabelText('siguiente pagina');
      await user.click(nextButton);

      await waitFor(() => {
        expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();
      });
      expect(screen.queryByText('20260224074620.cap')).not.toBeInTheDocument();
    });

    it('navigates to previous page when previous button is clicked', async () => {
      const user = userEvent.setup();
      const page1Alerts: Alert[] = [
        {
          id: '20260224074620',
          is_event: true,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-24T07:46:20',
        },
      ];
      const page2Alerts: Alert[] = [
        {
          id: '20260223123456',
          is_event: false,
          references: [],
          region: 42237,
          states: [42],
          time: '2026-02-23T12:34:56',
        },
      ];

      vi.mocked(getAlerts)
        .mockResolvedValueOnce({
          alerts: page1Alerts,
          count: 2,
          next: 2,
          prev: null,
        })
        .mockResolvedValueOnce({
          alerts: page2Alerts,
          count: 2,
          next: null,
          prev: 1,
        })
        .mockResolvedValueOnce({
          alerts: page1Alerts,
          count: 2,
          next: 2,
          prev: null,
        });

      render(
        <QueryClientProvider client={queryClient}>
          <AlertsTable />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();

      // Navigate to page 2
      const nextButton = screen.getByLabelText('siguiente pagina');
      await user.click(nextButton);

      await waitFor(() => {
        expect(screen.getByText('20260223123456.cap')).toBeInTheDocument();
      });
      expect(screen.queryByText('20260224074620.cap')).not.toBeInTheDocument();

      // Navigate back to page 1
      const prevButton = screen.getByLabelText('pagina anterior');
      await user.click(prevButton);

      await waitFor(() => {
        expect(screen.getByText('20260224074620.cap')).toBeInTheDocument();
      });
      expect(screen.queryByText('20260223123456.cap')).not.toBeInTheDocument();
    });
  });
});
