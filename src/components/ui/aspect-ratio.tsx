"use client";

<<<<<<< HEAD
import * as AspectRatioPrimitive from "@radix-ui/react-aspect-ratio";
=======
import * as AspectRatioPrimitive from "@radix-ui/react-aspect-ratio@1.1.2";
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

function AspectRatio({
  ...props
}: React.ComponentProps<typeof AspectRatioPrimitive.Root>) {
  return <AspectRatioPrimitive.Root data-slot="aspect-ratio" {...props} />;
}

export { AspectRatio };
