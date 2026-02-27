import { Map } from './components/map/Map';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AlertsTable } from '@/components/alerts-table/AlertsTable.tsx';
import { Navbar } from '@/components/ui/navbar.tsx';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Navbar />
      <div className="flex flex-col items-center justify-center">
        <div className="p-4">
          <Map />
        </div>
        <div className="p-4">
          <AlertsTable />
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
