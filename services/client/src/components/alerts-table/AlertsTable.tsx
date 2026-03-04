import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { getAlerts, getCapFileUrl } from '@/lib/api.ts';
import { type Alert, EventType } from '@/lib/alerts.ts';
import { STATES } from '@/lib/states.ts';
import { REGIONS } from '@/lib/regions.ts';
import { Spinner } from '@/components/ui/spinner.tsx';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table.tsx';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
} from '@/components/ui/pagination.tsx';
import { AlertCircleIcon } from 'lucide-react';
import {
  Alert as AlertMessage,
  AlertDescription,
  AlertTitle,
} from '@/components/ui/alert.tsx';

/**
 * Column definitions for the alerts table using TanStack Table.
 */
const columns: ColumnDef<Alert>[] = [
  {
    accessorKey: 'time',
    header: 'Fecha',
    cell: ({ row }) => {
      const time = row.original.time;
      return time.replace('T', ' ');
    },
  },
  {
    accessorKey: 'states',
    header: 'Estado(s)',
    cell: ({ row }) => {
      return row.original.states.map((s) => STATES[s] ?? s).join(', ');
    },
  },
  {
    accessorKey: 'region',
    header: 'Region',
    cell: ({ row }) => {
      return REGIONS[row.original.region] ?? row.original.region;
    },
  },
  {
    id: 'type',
    header: 'Tipo',
    cell: ({ row }) => {
      return row.original.is_event ? EventType.Event : EventType.Alert;
    },
  },
  {
    id: 'file',
    header: 'Archivo',
    cell: ({ row }) => {
      return (
        <a
          className="text-blue-500 underline"
          href={getCapFileUrl(row.original.id)}
        >
          {row.original.id}.cap
        </a>
      );
    },
  },
];

/**
 * Component that displays a table of alerts fetched from the API.
 * Uses React Query for data fetching and TanStack Table for table management.
 *
 * @returns {JSX.Element} The rendered AlertsTable component.
 */
export const AlertsTable = () => {
  const [page, setPage] = useState(1);

  const {
    isPending,
    error,
    data: alertsResponse,
  } = useQuery({
    queryKey: ['alerts', page],
    queryFn: () => getAlerts(page),
  });

  // tanstack table is currently incompatible with react compiler
  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    data: alertsResponse?.alerts ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isPending) return <Spinner />;

  if (error)
    return (
      <AlertMessage variant="destructive">
        <AlertCircleIcon />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </AlertMessage>
    );

  if (!alertsResponse) {
    console.error('No alert data available');
    return null;
  }

  const hasNext = alertsResponse.next !== null;
  const hasPrevious = alertsResponse.prev !== null;

  return (
    <div className="space-y-4">
      <div className="w-full rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="text-center">
                  No hay alertas.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious
              onClick={() => setPage((p) => p - 1)}
              className={
                hasPrevious
                  ? 'cursor-pointer'
                  : 'pointer-events-none opacity-50'
              }
            />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext
              onClick={() => setPage((p) => p + 1)}
              className={
                hasNext ? 'cursor-pointer' : 'pointer-events-none opacity-50'
              }
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
};
