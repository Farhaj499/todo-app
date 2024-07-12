import { useFormStatus } from "react-dom"



export default function SubmitButton() {
    const {pending} = useFormStatus()
  
    return (
    <button disabled={pending} className='mt-4 px-2 py-1 text-white bg-teal-600 rounded-md w-full'>
        {
            pending ? "Saving..." : "Save"
        }
    </button>   
  )
}
