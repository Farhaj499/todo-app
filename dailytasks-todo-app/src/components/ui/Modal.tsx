import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import AddTask from "./AddTask"
import EditTask from "./EditTask"
import { Todo } from "../../../types"

export function Modal(
  {title, children, adding, editing, task}:{
    title: string,
    children: React.ReactNode,
    adding?: boolean,
    editing?: boolean,
    task: Todo
  }
) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        {
          children
        }
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        {adding && <AddTask/>}
        {editing && <EditTask task={task}/>}
      </DialogContent>
    </Dialog>
  )
}
