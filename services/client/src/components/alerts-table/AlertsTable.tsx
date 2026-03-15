import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { type AlertFilters, getAlerts, getCapFileUrl } from '@/lib/api.ts';
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select.tsx';
import { Field, FieldLabel } from '@/components/ui/field.tsx';
import { Button } from '@/components/ui/button.tsx';
import { DatePickerWithRange } from '@/components/ui/range-picker.tsx';
import { type DateRange } from 'react-day-picker';
import { format } from 'date-fns';

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
    header: 'Región',
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

const getUniqueRegions = (): Array<{ id: string; name: string }> => {
  const seen: Set<string> = new Set();
  for (const [, value] of Object.entries(REGIONS)) {
    if (!seen.has(value)) {
      seen.add(value);
    }
  }
  return Array.from(seen)
    .map((region) => ({ id: region, name: region }))
    .sort((regionA, regionB) => regionA.name.localeCompare(regionB.name));
};

const buildFilters = (
  dateRange: DateRange | undefined,
  state: string | undefined,
  region: string | undefined,
  type: string | undefined,
): AlertFilters => ({
  startDate: dateRange?.from ? format(dateRange.from, 'yyyy-MM-dd') : undefined,
  endDate: dateRange?.to ? format(dateRange.to, 'yyyy-MM-dd') : undefined,
  state: state && state !== 'all' ? Number(state) : undefined,
  region: region && region !== 'all' ? region : undefined,
  type: type && type !== 'all' ? (type as 'event' | 'alert') : undefined,
});

/**
 * Component that displays a table of alerts fetched from the API.
 * Uses React Query for data fetching and TanStack Table for table management.
 *
 * @returns {JSX.Element} The rendered AlertsTable component.
 */
export const AlertsTable = () => {
  const [page, setPage] = useState(1);
  const [dateRange, setDateRange] = useState<DateRange | undefined>();
  const [selectedState, setSelectedState] = useState<string | undefined>();
  const [selectedRegion, setSelectedRegion] = useState<string | undefined>();
  const [selectedType, setSelectedType] = useState<string | undefined>();

  const [appliedFilters, setAppliedFilters] = useState<AlertFilters>({});

  const {
    isPending,
    error,
    data: alertsResponse,
  } = useQuery({
    queryKey: ['alerts', page, appliedFilters],
    queryFn: () => getAlerts(page, appliedFilters),
  });

  const applyFilters = () => {
    setPage(1);
    setAppliedFilters(
      buildFilters(dateRange, selectedState, selectedRegion, selectedType),
    );
  };

  const clearFilters = () => {
    setDateRange(undefined);
    setSelectedState(undefined);
    setSelectedRegion(undefined);
    setSelectedType(undefined);
    setPage(1);
    setAppliedFilters({});
  };

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

  const uniqueRegions = getUniqueRegions();

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 w-full">
        <div className="flex gap-2">
          <Field>
            <FieldLabel htmlFor="date-range">Fecha</FieldLabel>
            <DatePickerWithRange
              date={dateRange}
              onDateChange={setDateRange}
              id="date-range"
            />
          </Field>

          <Field>
            <FieldLabel htmlFor="state-filter">Estado</FieldLabel>
            <Select value={selectedState} onValueChange={setSelectedState}>
              <SelectTrigger id="state-filter">
                <SelectValue placeholder="Todos" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(STATES).map(([id, name]) => (
                  <SelectItem key={id} value={id}>
                    {name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>

          <Field>
            <FieldLabel htmlFor="region-filter">Región</FieldLabel>
            <Select value={selectedRegion} onValueChange={setSelectedRegion}>
              <SelectTrigger id="region-filter">
                <SelectValue placeholder="Todas" />
              </SelectTrigger>
              <SelectContent>
                {uniqueRegions.map(({ id, name }) => (
                  <SelectItem key={id} value={id}>
                    {name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>

          <Field>
            <FieldLabel htmlFor="type-filter">Tipo</FieldLabel>
            <Select value={selectedType} onValueChange={setSelectedType}>
              <SelectTrigger id="type-filter">
                <SelectValue placeholder="Todos" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos</SelectItem>
                <SelectItem value="event">Evento</SelectItem>
                <SelectItem value="alert">Alerta</SelectItem>
              </SelectContent>
            </Select>
          </Field>
        </div>

        <div className="flex gap-2 w-full">
          <Button onClick={clearFilters} variant="outline">
            Limpiar
          </Button>

          <Button onClick={applyFilters}>Aplicar</Button>
        </div>
      </div>

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
