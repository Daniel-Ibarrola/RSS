import '@testing-library/jest-dom';

import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Map } from './Map';
import { getLatestAlert } from '@/lib/api';
import { type Alert } from '@/lib/alerts';
import type { ReactNode } from 'react';
import type { CircleProps } from './Circle';
import type { PolygonProps } from './Polygon';

// Mock the API module
vi.mock('@/lib/api', () => ({
  getLatestAlert: vi.fn(),
}));

// Mock Google Maps components
vi.mock('@vis.gl/react-google-maps', () => ({
  APIProvider: ({ children }: { children: ReactNode }) => (
    <div data-testid="api-provider">{children}</div>
  ),
  Map: ({ children }: { children: ReactNode }) => (
    <div data-testid="google-map">{children}</div>
  ),
  GoogleMapsContext: {
    Provider: ({ children }: { children: ReactNode }) => <>{children}</>,
  },
}));

vi.mock('./Circle', () => ({
  Circle: ({
    'data-testid': testId,
  }: CircleProps & { 'data-testid'?: string }) => (
    <div data-testid={testId || 'circle'} />
  ),
}));

vi.mock('./Polygon', () => ({
  Polygon: ({
    'data-testid': testId,
  }: PolygonProps & { 'data-testid'?: string }) => (
    <div data-testid={testId || 'polygon'} />
  ),
}));

describe('Map', () => {
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
          <Map />
        </QueryClientProvider>,
      );

      expect(screen.getByLabelText('Loading')).toBeInTheDocument();
    });

    it('renders error message on failure', async () => {
      const errorMessage = 'Failed to fetch alert';
      vi.mocked(getLatestAlert).mockRejectedValue(new Error(errorMessage));

      render(
        <QueryClientProvider client={queryClient}>
          <Map />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(
          screen.getByText(new RegExp(`${errorMessage}`, 'i')),
        ).toBeInTheDocument();
      });
    });
  });

  describe('Map rendering with alert data', () => {
    it('renders map container when data is loaded', async () => {
      const mockAlert: Alert = {
        id: '20260224074620',
        is_event: false,
        references: [],
        region: 41201,
        states: [],
        time: '2026-02-24T07:46:20',
      };

      vi.mocked(getLatestAlert).mockResolvedValue(mockAlert);

      render(
        <QueryClientProvider client={queryClient}>
          <Map />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByTestId('api-provider')).toBeInTheDocument();
      expect(screen.getByTestId('google-map')).toBeInTheDocument();
    });

    it('renders Circle when alert is an event with region', async () => {
      const mockAlert: Alert = {
        id: '20260224074620',
        is_event: true,
        references: [],
        region: 42237,
        states: [42],
        time: '2026-02-24T07:46:20',
      };

      vi.mocked(getLatestAlert).mockResolvedValue(mockAlert);

      render(
        <QueryClientProvider client={queryClient}>
          <Map />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      expect(screen.getByTestId('circle')).toBeInTheDocument();
      expect(screen.queryByTestId('polygon')).not.toBeInTheDocument();
    });

    it('renders Polygons when alert is not an event and has states', async () => {
      const mockAlert: Alert = {
        id: '20260224074620',
        is_event: false,
        references: [],
        region: 42237,
        states: [42, 43],
        time: '2026-02-24T07:46:20',
      };

      vi.mocked(getLatestAlert).mockResolvedValue(mockAlert);

      render(
        <QueryClientProvider client={queryClient}>
          <Map />
        </QueryClientProvider>,
      );

      await waitFor(() => {
        expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
      });

      const polygons = screen.queryAllByTestId('polygon');
      expect(polygons.length).toBeGreaterThan(0);
      expect(screen.queryByTestId('circle')).not.toBeInTheDocument();
    });
  });
});
