import { beforeEach, describe, expect, it, vi } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { getLatestAlert } from '@/lib/api.ts';
import { render, screen, waitFor } from '@testing-library/react';
import { MapCard } from '@/components/map/MapCard.tsx';
import type { Alert } from '@/lib/alerts.ts';

vi.mock('@/lib/api', () => ({
  getLatestAlert: vi.fn(),
  LATEST_CAP_FILE_URL: 'https://example.com/latest.cap',
}));

describe('MapCard', () => {
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

  describe('Loading and error states', () => {
    it('renders loading state initially', () => {
      vi.mocked(getLatestAlert).mockReturnValue(new Promise(() => {}));

      render(
        <QueryClientProvider client={queryClient}>
          <MapCard />
        </QueryClientProvider>,
      );

      expect(screen.getByLabelText('Loading')).toBeInTheDocument();
    });

    it('renders error message on failure', async () => {
      const errorMessage = 'Failed to fetch alert';
      vi.mocked(getLatestAlert).mockRejectedValue(new Error(errorMessage));

      render(
        <QueryClientProvider client={queryClient}>
          <MapCard />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(
          screen.getByText(new RegExp(`${errorMessage}`, 'i')),
        ).toBeInTheDocument();
      });
    });
  });

  it('renders alert data and link to cap file', async () => {
    const mockAlert: Alert = {
      id: '20260302153939',
      is_event: true,
      references: [],
      region: 41209,
      states: [],
      time: '2026-03-02T15:39:39',
    };

    vi.mocked(getLatestAlert).mockResolvedValue(mockAlert);

    render(
      <QueryClientProvider client={queryClient}>
        <MapCard />
      </QueryClientProvider>,
    );

    await waitFor(() => {
      expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
    });

    expect(
      screen.getByText(
        'Lunes, 2 de marzo de 2026, 15:39:39 Sismo en Guerrero.',
      ),
    ).toBeInTheDocument();
    expect(screen.getByText('Severidad: Menor')).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: /Último CAP/i }),
    ).toBeInTheDocument();
  });
});
