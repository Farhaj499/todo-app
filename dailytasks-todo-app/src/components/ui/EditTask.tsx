"use client"
import { edit_todo } from "@/actions/actions"
import { Todo } from "../../../types"
import { useFormState } from "react-dom"
import SubmitButton from "./SubmitButton"
import { useEffect } from "react"
import toast from "react-hot-toast"



export default function EditTask({task}:{task: Todo}) {
  
  const initial_state = {
    status: " ",
    message: "",
  }
  const [state, formAction] = useFormState(edit_todo, initial_state)
  const {status, message} = state
  
  const handleSubmit = (FormData: FormData) => {
    const id: number = task.id
    const content: string = FormData.get('edit_task') as string
    formAction({id, content, is_completed: task.is_completed})
  }
  

  useEffect(() => {
    if (status === "success") {
      toast.success(message)
    }
    else if (status == "error") {
      toast.error(message)
    }
  }, [state])

  
  return (
    <form action={handleSubmit} className='flex flex-col justify-between items-center gap-x-3 w-full'>
        <input 
            type="text" 
            placeholder='Add task here' 
            minLength={3} 
            maxLength={54}
            required
            defaultValue={task.content}
            name="edit_task"
            className='w-full px-2 py-1 border border-gray-100 rounded-md'
        />
        <SubmitButton/>
    </form>
  )
}
