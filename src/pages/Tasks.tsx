import { useState } from "react";
import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import {
  Plus,
  Search,
  Filter,
  Calendar,
  Clock,
  CheckCircle2,
  Circle,
  AlertCircle,
  User,
  MapPin,
  MoreVertical,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Task {
  id: string;
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
  status: "pending" | "in-progress" | "completed";
  dueDate: string;
  assignee: string;
  location: string;
  category: "crop" | "livestock" | "maintenance" | "general";
}

const tasks: Task[] = [
  {
    id: "1",
    title: "Harvest wheat in Field A-12",
    description: "Complete wheat harvest before weather changes",
    priority: "high",
    status: "in-progress",
    dueDate: "Today",
    assignee: "John D.",
    location: "Field A-12",
    category: "crop",
  },
  {
    id: "2",
    title: "Vaccinate cattle herd",
    description: "Annual vaccination for the main cattle herd",
    priority: "high",
    status: "pending",
    dueDate: "Tomorrow",
    assignee: "Sarah M.",
    location: "Barn B",
    category: "livestock",
  },
  {
    id: "3",
    title: "Repair irrigation system",
    description: "Fix leak in the northern irrigation line",
    priority: "medium",
    status: "pending",
    dueDate: "Nov 28",
    assignee: "Mike R.",
    location: "Field C-3",
    category: "maintenance",
  },
  {
    id: "4",
    title: "Order new tractor parts",
    description: "Replace worn brake pads and filters",
    priority: "medium",
    status: "completed",
    dueDate: "Nov 25",
    assignee: "John D.",
    location: "Workshop",
    category: "maintenance",
  },
  {
    id: "5",
    title: "Apply fertilizer to corn fields",
    description: "Second application of NPK fertilizer",
    priority: "low",
    status: "pending",
    dueDate: "Nov 30",
    assignee: "Sarah M.",
    location: "Field B-7",
    category: "crop",
  },
  {
    id: "6",
    title: "Update farm records",
    description: "Monthly inventory and financial records update",
    priority: "low",
    status: "pending",
    dueDate: "Dec 1",
    assignee: "Admin",
    location: "Office",
    category: "general",
  },
];

const priorityColors = {
  high: "bg-destructive/10 text-destructive border-destructive/20",
  medium: "bg-warning/10 text-warning border-warning/20",
  low: "bg-muted text-muted-foreground border-border",
};

const statusConfig = {
  pending: { icon: Circle, color: "text-muted-foreground", bg: "bg-muted" },
  "in-progress": { icon: Clock, color: "text-info", bg: "bg-info/10" },
  completed: { icon: CheckCircle2, color: "text-success", bg: "bg-success/10" },
};

const categoryColors = {
  crop: "border-l-success",
  livestock: "border-l-warning",
  maintenance: "border-l-info",
  general: "border-l-primary",
};

const Tasks = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = !selectedStatus || task.status === selectedStatus;
    return matchesSearch && matchesStatus;
  });

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === "pending").length,
    inProgress: tasks.filter((t) => t.status === "in-progress").length,
    completed: tasks.filter((t) => t.status === "completed").length,
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
          <div>
            <h1 className="text-3xl font-bold text-foreground">Task Management</h1>
            <p className="text-muted-foreground mt-1">
              Organize and track all farm activities
            </p>
          </div>
          <Button variant="hero" size="lg">
            <Plus className="w-5 h-5" />
            Create Task
          </Button>
        </motion.div>

        {/* Stats Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10">
                <Calendar className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.total}</p>
                <p className="text-sm text-muted-foreground">Total Tasks</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-muted">
                <Circle className="w-5 h-5 text-muted-foreground" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.pending}</p>
                <p className="text-sm text-muted-foreground">Pending</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-info/10">
                <Clock className="w-5 h-5 text-info" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.inProgress}</p>
                <p className="text-sm text-muted-foreground">In Progress</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-success/10">
                <CheckCircle2 className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.completed}</p>
                <p className="text-sm text-muted-foreground">Completed</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Search and Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex flex-col sm:flex-row gap-4"
        >
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
            />
          </div>
          <Button variant="outline" className="gap-2">
            <Filter className="w-4 h-4" />
            Filter
          </Button>
        </motion.div>

        {/* Status Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="flex flex-wrap gap-2"
        >
          <Button
            variant={selectedStatus === null ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedStatus(null)}
          >
            All
          </Button>
          <Button
            variant={selectedStatus === "pending" ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedStatus("pending")}
          >
            Pending
          </Button>
          <Button
            variant={selectedStatus === "in-progress" ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedStatus("in-progress")}
          >
            In Progress
          </Button>
          <Button
            variant={selectedStatus === "completed" ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedStatus("completed")}
          >
            Completed
          </Button>
        </motion.div>

        {/* Tasks List */}
        <div className="space-y-4">
          {filteredTasks.map((task, index) => {
            const StatusIcon = statusConfig[task.status].icon;
            return (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.05 }}
                className={cn(
                  "bg-card rounded-xl p-5 shadow-card border border-border/50 border-l-4 card-hover",
                  categoryColors[task.category]
                )}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex items-start gap-4">
                    <button
                      className={cn(
                        "mt-1 p-1 rounded-full transition-colors",
                        statusConfig[task.status].bg
                      )}
                    >
                      <StatusIcon className={cn("w-5 h-5", statusConfig[task.status].color)} />
                    </button>
                    <div className="flex-1">
                      <h3
                        className={cn(
                          "font-semibold text-lg",
                          task.status === "completed"
                            ? "text-muted-foreground line-through"
                            : "text-foreground"
                        )}
                      >
                        {task.title}
                      </h3>
                      <p className="text-sm text-muted-foreground mt-1">{task.description}</p>
                      <div className="flex flex-wrap items-center gap-4 mt-3">
                        <span className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Calendar className="w-4 h-4" />
                          {task.dueDate}
                        </span>
                        <span className="flex items-center gap-1 text-sm text-muted-foreground">
                          <User className="w-4 h-4" />
                          {task.assignee}
                        </span>
                        <span className="flex items-center gap-1 text-sm text-muted-foreground">
                          <MapPin className="w-4 h-4" />
                          {task.location}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span
                      className={cn(
                        "px-3 py-1 rounded-full text-xs font-medium border",
                        priorityColors[task.priority]
                      )}
                    >
                      {task.priority}
                    </span>
                    <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                      <MoreVertical className="w-5 h-5 text-muted-foreground" />
                    </button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </AppLayout>
  );
};

export default Tasks;
