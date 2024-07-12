import React from 'react'
import { Todo } from '../../../types'
import SingleTodo from './SingleTodo'

async function TodoTable() {

    const response = await fetch("http://localhost:8000/todos/")
    const data = await response.json()
    const todo_list: Todo[] = data.sort((a:Todo, b:Todo) => a.id - b.id)

    // const todo_list: Todo[] = [
    //     {id:1, content:'Task 1', is_completed: false}, 
    //     {id:2, content:'Task 2', is_completed: false}, 
    //     {id:3, content:'Task 3', is_completed: false}, 
    //     {id:4, content:'Task 4', is_completed: false}]
  return (
    <table className='w-full'>
        <thead>
            <tr className='flex justify-between items-center px-2 py-1 bg-gray-100 shadow-md uppercase'>
                <th>Tasks</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {
                todo_list.map((task:Todo) => (
                    <SingleTodo key={task.id} task={task}/>
                ))
            }
        </tbody>
    </table>
  )
}

export default TodoTable