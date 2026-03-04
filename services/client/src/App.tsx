import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AlertsTable } from '@/components/alerts-table/AlertsTable.tsx';
import { Navbar } from '@/components/ui/navbar.tsx';
import { MapCard } from '@/components/map/MapCard.tsx';

const queryClient = new QueryClient();

/**
 * The main application component that sets up the React Query client and
 * the layout of the application, including the navbar, map, and alerts table.
 */
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Navbar />
      <div className="flex flex-col items-center justify-center">
        <div className="p-4 w-full">
          <MapCard />
        </div>
        <div className="p-4">
          <AlertsTable />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
