"use client";

import * as React from "react";
<<<<<<< HEAD
import * as SeparatorPrimitive from "@radix-ui/react-separator";
=======
import * as SeparatorPrimitive from "@radix-ui/react-separator@1.1.2";
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

import { cn } from "./utils";

function Separator({
  className,
  orientation = "horizontal",
  decorative = true,
  ...props
}: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return (
    <SeparatorPrimitive.Root
      data-slot="separator-root"
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "bg-border shrink-0 data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-px",
        className,
      )}
      {...props}
    />
  );
}

export { Separator };
