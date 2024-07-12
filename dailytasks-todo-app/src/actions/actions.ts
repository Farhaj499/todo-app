"use server"
import { revalidatePath } from "next/cache"
import { Todo } from "../../types"


// add_task

export async function add_todo(state:{status: string, message: string}, formData: FormData){
    {/* add_task is the name of the input in AddTask file */}
    const new_todo = formData.get("add_task") as string

    try {
        const response = await fetch ("http://localhost:8000/todos/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({content: new_todo})
        })
        const data = await response.json()
        if (data.content){
            // after sending to database, it will refresh the page
            // it will do both above tasks in one request
            revalidatePath("/todos")
            return {status: "success", message: "Todo added successfully"}        
        }
        else {
            return {status: "error", message: "Something went wrong"}
        }

    } catch (error: any) {
        return {status: "error", message: error.message}
    }
    
}

// edit_task

export async function edit_todo(
    state:{status: string, message: string}, 
    {id, content, is_completed}: Todo
){
    // const new_edited_todo = formData.get("edit_task") as string


    try {
        const response = await fetch (`http://localhost:8000/todos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({id: id, content: content, is_completed: is_completed})
        })

        // after sending to database, it will refresh the page
        // it will do both above tasks in one request
        revalidatePath("/todos")

        return {status: "success", message: "Todo changed successfully"}

    } catch (error: any) {
        return {status: "error", message: error.message}
    }
    
}

// status change

export async function status_change(
    id: number, 
    content: string, 
    is_completed: boolean
){
    try {
        const response = await fetch (`http://localhost:8000/todos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({id: id, content: content, is_completed: !is_completed})
        })
        const res = await response.json()
        revalidatePath("/todos")
        return {status: "success", message: "Status changed successfully"}

    } catch (error: any) {
        return {status: "error", message: error.message}
    }
    
}   


// Delete task

export async function delete_todo(
    id: number, 
){
    try {
        const response = await fetch (`http://localhost:8000/todos/${id}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
        })
        const res = await response.json()
        revalidatePath("/todos")
        return {status: "success", message: "Status deleted successfully"}

    } catch (error: any) {
        return {status: "error", message: error.message}
    }
    
}   

