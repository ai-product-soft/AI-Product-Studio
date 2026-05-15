import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const labelVariants = cva(
  "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
  {
    variants: {
      variant: {
        default: "text-foreground",
        destructive: "text-destructive",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement>, VariantProps<typeof labelVariants> {}

const Label = ({ className, variant, ...props }: LabelProps) => (
  <label className={cn(labelVariants({ variant, className }))} {...props} />
);
Label.displayName = "Label";

export { Label };
