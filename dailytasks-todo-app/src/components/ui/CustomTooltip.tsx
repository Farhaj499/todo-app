import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export function CustomTooltip({tooltip_content, children}:{tooltip_content:string, children: React.ReactNode}) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>
        <TooltipContent>
            <p>
                {
                    tooltip_content
                }
            </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
