import { motion } from "framer-motion";
import { Calendar, CheckCircle2, Circle, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Task {
  id: string;
  title: string;
  dueDate: string;
  priority: "high" | "medium" | "low";
  completed: boolean;
}

const tasks: Task[] = [
  {
    id: "1",
    title: "Harvest wheat in Field A-12",
    dueDate: "Today",
    priority: "high",
    completed: false,
  },
  {
    id: "2",
    title: "Order new tractor parts",
    dueDate: "Tomorrow",
    priority: "medium",
    completed: false,
  },
  {
    id: "3",
    title: "Schedule vet visit for cattle",
    dueDate: "In 2 days",
    priority: "high",
    completed: false,
  },
  {
    id: "4",
    title: "Update irrigation system",
    dueDate: "In 3 days",
    priority: "low",
    completed: true,
  },
];

const priorityColors = {
  high: "text-destructive",
  medium: "text-warning",
  low: "text-muted-foreground",
};

export function UpcomingTasks() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.35 }}
      className="bg-card rounded-xl p-6 shadow-card border border-border/50"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground">Upcoming Tasks</h3>
        <Calendar className="w-5 h-5 text-muted-foreground" />
      </div>
      <div className="space-y-3">
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + index * 0.1 }}
            className={cn(
              "flex items-start gap-3 p-3 rounded-lg transition-colors",
              task.completed ? "bg-muted/30" : "hover:bg-muted/50"
            )}
          >
            <button className="mt-0.5 flex-shrink-0">
              {task.completed ? (
                <CheckCircle2 className="w-5 h-5 text-success" />
              ) : task.priority === "high" ? (
                <AlertCircle className="w-5 h-5 text-destructive" />
              ) : (
                <Circle className="w-5 h-5 text-muted-foreground" />
              )}
            </button>
            <div className="flex-1 min-w-0">
              <p
                className={cn(
                  "font-medium truncate",
                  task.completed
                    ? "text-muted-foreground line-through"
                    : "text-foreground"
                )}
              >
                {task.title}
              </p>
              <p className={cn("text-sm", priorityColors[task.priority])}>
                {task.dueDate}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
