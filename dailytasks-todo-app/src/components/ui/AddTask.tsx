"use client"
import { add_todo } from "@/actions/actions"
import { useEffect } from "react"
import { useFormState } from "react-dom"
import { useRef } from "react"
import toast from "react-hot-toast"
import SubmitButton from "./SubmitButton"

export default function AddTask() {

  const ref = useRef<HTMLFormElement>(null)
  
  const initial_state = {
    status: " ",
    message: "",
  }
  const [state, formAction] = useFormState(add_todo, initial_state)
  const {status, message} = state

  useEffect(() => {
    if (status === "success") {
      ref.current?.reset()
      toast.success(message)
    }
    else if (status == "error") {
      toast.error(message)
    }
  }, [state])


  return (
    <form
      ref={ref} 
      action={formAction} 
      className='flex flex-col justify-between items-center gap-x-3 w-full'
    >
        <input 
            type="text" 
            placeholder='Add task here' 
            minLength={3} 
            maxLength={54}
            required
            name="add_task"
            className='w-full px-2 py-1 border border-gray-100 rounded-md'
        />
        <SubmitButton/>
    </form>
  )
}
