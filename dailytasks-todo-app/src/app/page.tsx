import { Modal } from "@/components/ui/Modal";
import TodoTable from "@/components/ui/TodoTable";
import { Button } from "@/components/ui/button";
import { Cross } from "lucide-react";


export default function Home() {
  return (
    <main className="max-w-5xl mx-auto mt-8 ">
      {/* Add task section*/}
      <section>
        <Modal title="Add New Task" adding={true}>
          <Button 
              variant="default"
              className="w-full bg-teal-600 px-2 py-1 text-white uppercase text-lg"
          >
              Add Task 
              <Cross className="text-teal-600 fill-white pb-[3px] px-[4px] "/>
          </Button>
        </Modal>
      </section>

      {/* Todo table section*/}
      <section className="mt-4">
        <TodoTable/>
      </section>
    </main>
  );
}
