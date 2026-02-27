import { Separator } from '@/components/ui/separator';

export function Navbar() {
  return (
    <header className="w-full">
      <div className="container mx-auto flex h-16 items-center px-4 bg-gray-800">
        <div className="mr-4 flex h-8 w-8 items-center justify-center bg-gray-800 rounded-md text-primary-foreground font-bold">
          <img
            src="/cires.png"
            alt="CIRES Logo"
            className="h-full w-full object-contain"
          />
        </div>

        <span className="text-lg font-semibold tracking-tight text-white">
          SASMEX CAP
        </span>
      </div>
      <Separator />
    </header>
  );
}
