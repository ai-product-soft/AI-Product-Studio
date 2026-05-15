import { cn } from "@/lib/utils";

export function Table({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className="w-full overflow-auto"><table className={cn("w-full", className)}>{children}</table></div>;
}

export function TableHeader({ children }: { children: React.ReactNode }) {
  return <thead>{children}</thead>;
}

export function TableBody({ children }: { children: React.ReactNode }) {
  return <tbody>{children}</tbody>;
}

export function TableRow({ children, className }: { children: React.ReactNode; className?: string }) {
  return <tr className={cn("border-b", className)}>{children}</tr>;
}

export function TableHead({ children, className }: { children: React.ReactNode; className?: string }) {
  return <th className={cn("px-4 py-2 text-left font-medium", className)}>{children}</th>;
}

export function TableCell({ children, className }: { children: React.ReactNode; className?: string }) {
  return <td className={cn("px-4 py-2", className)}>{children}</td>;
}
