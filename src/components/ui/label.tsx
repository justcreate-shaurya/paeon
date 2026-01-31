"use client";

import * as React from "react";
<<<<<<< HEAD
import * as LabelPrimitive from "@radix-ui/react-label";
=======
import * as LabelPrimitive from "@radix-ui/react-label@2.1.2";
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

import { cn } from "./utils";

function Label({
  className,
  ...props
}: React.ComponentProps<typeof LabelPrimitive.Root>) {
  return (
    <LabelPrimitive.Root
      data-slot="label"
      className={cn(
        "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}

export { Label };
