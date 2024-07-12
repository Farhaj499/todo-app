"use client"
import React from 'react'
import { Todo } from '../../../types'
import { CiSquareCheck } from 'react-icons/ci'
import { FiEdit, FiTrash2 } from 'react-icons/fi'
import { CustomTooltip } from './CustomTooltip'
import { Modal } from './Modal'
import { delete_todo, edit_todo, status_change } from '@/actions/actions'
import toast from 'react-hot-toast'

export default function SingleTodo({task}:{task: Todo}) {
  
  const handleStatus = async ()=>{
    const response = await status_change(
      task.id, 
      task.content, 
      task.is_completed
    ) 
    if(response.status == "success"){
      toast.success(response.message)
    }
    else if (response.status == "error"){
      toast.error(response.message)
    }
  }


  const handleDelete = async ()=>{
    const response = await delete_todo(
      task.id, 
    ) 
    if(response.status == "success"){
      toast.success(response.message)
    }
    else if (response.status == "error"){
      toast.error(response.message)
    }
  }
   
  return (
    <tr className='flex justify-between items-center border-b border-gray-300 px-2 py-2 '>
        <td> {task.content} </td>
        <td className='flex gap-x-2 '>
          <CustomTooltip tooltip_content='Mark as completed'>
            <button onClick={handleStatus}>
              <CiSquareCheck size={28} className={`${task.is_completed ? 'text-green-500' : 'text-gray-400'}`}/>
            </button>
          </CustomTooltip>
          
          <CustomTooltip tooltip_content='Edit task'>
            <Modal title="Edit Task" editing={true} task={task} >  
              <FiEdit size={24} className='text-blue-500'/>
            </Modal>
          </CustomTooltip>
          
          <CustomTooltip tooltip_content='Delete task'>
            <button onClick={handleDelete}>
              <FiTrash2 size={24} className='text-red-500'/>
            </button>
          </CustomTooltip>
        </td>
    </tr>
  )
}
