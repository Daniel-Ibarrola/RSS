import { Map } from './components/map/Map';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AlertsTable } from '@/components/alerts-table/AlertsTable.tsx';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex flex-col items-center justify-center w-screen h-screen text-blue-500">
        <Map />
        <AlertsTable />
      </div>
    </QueryClientProvider>
  );
}

export default App;
