import { useQuery } from '@tanstack/react-query';
import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { getAlerts } from '@/lib/api.ts';
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
      return `${row.original.id}.cap`;
    },
  },
];

export const AlertsTable = () => {
  const {
    isPending,
    error,
    data: alertsResponse,
  } = useQuery({
    queryKey: ['alerts'],
    queryFn: getAlerts,
  });

  // tanstack table is currently incompatible with react compiler
  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    data: alertsResponse?.alerts ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isPending) return <Spinner />;

  if (error) return <p>Ha ocurrido un error: {error.message}</p>;

  return (
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
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
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
  );
};
