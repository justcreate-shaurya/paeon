"use client";

import * as React from "react";
<<<<<<< HEAD
import * as ProgressPrimitive from "@radix-ui/react-progress";
=======
import * as ProgressPrimitive from "@radix-ui/react-progress@1.1.2";
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

import { cn } from "./utils";

function Progress({
  className,
  value,
  ...props
}: React.ComponentProps<typeof ProgressPrimitive.Root>) {
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      className={cn(
        "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full",
        className,
      )}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className="bg-primary h-full w-full flex-1 transition-all"
        style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
      />
    </ProgressPrimitive.Root>
  );
}

export { Progress };
