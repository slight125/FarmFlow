import { motion } from "framer-motion";
import { Plus, Sprout, PawPrint, ClipboardList, Package } from "lucide-react";
import { Button } from "@/components/ui/button";

const actions = [
  { icon: Sprout, label: "Log Crop Activity", color: "bg-success/10 hover:bg-success/20 text-success" },
  { icon: PawPrint, label: "Record Health Check", color: "bg-warning/10 hover:bg-warning/20 text-warning" },
  { icon: ClipboardList, label: "Create Task", color: "bg-info/10 hover:bg-info/20 text-info" },
  { icon: Package, label: "Update Inventory", color: "bg-primary/10 hover:bg-primary/20 text-primary" },
];

export function QuickActions() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="bg-card rounded-xl p-6 shadow-card border border-border/50"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground">Quick Actions</h3>
        <Plus className="w-5 h-5 text-muted-foreground" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        {actions.map((action, index) => (
          <motion.div
            key={action.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 + index * 0.1 }}
          >
            <Button
              variant="ghost"
              className={`w-full h-auto flex-col gap-2 py-4 ${action.color} transition-all duration-200`}
            >
              <action.icon className="w-6 h-6" />
              <span className="text-xs font-medium text-center leading-tight">
                {action.label}
              </span>
            </Button>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
