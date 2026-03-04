import { Loader2Icon } from 'lucide-react';

import { cn } from '@/lib/utils';

/**
 * A reusable loading spinner component based on Lucide's Loader2Icon.
 *
 * @param {React.ComponentProps<"svg">} props - The SVG properties for the spinner.
 * @returns {JSX.Element} The rendered Spinner component.
 */
function Spinner({ className, ...props }: React.ComponentProps<'svg'>) {
  return (
    <Loader2Icon
      role="status"
      aria-label="Loading"
      className={cn('size-4 animate-spin', className)}
      {...props}
    />
  );
}

export { Spinner };
