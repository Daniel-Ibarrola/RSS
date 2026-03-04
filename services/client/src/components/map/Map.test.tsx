import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Map } from './Map';
import { type Alert } from '@/lib/alerts';
import type { ReactNode } from 'react';
import type { CircleProps } from './Circle';
import type { PolygonProps } from './Polygon';

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
  it('renders Circle when alert is an event with region', async () => {
    const mockAlert: Alert = {
      id: '20260224074620',
      is_event: true,
      references: [],
      region: 42237,
      states: [42],
      time: '2026-02-24T07:46:20',
    };

    render(<Map alert={mockAlert} />);

    expect(screen.getByTestId('api-provider')).toBeInTheDocument();
    expect(screen.getByTestId('google-map')).toBeInTheDocument();
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

    render(<Map alert={mockAlert} />);

    await waitFor(() => {
      expect(screen.queryByLabelText('Loading')).not.toBeInTheDocument();
    });

    const polygons = screen.queryAllByTestId('polygon');
    expect(polygons.length).toBeGreaterThan(0);
    expect(screen.queryByTestId('circle')).not.toBeInTheDocument();
  });
});
