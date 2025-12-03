import { motion } from "framer-motion";
import { Clock, Sprout, PawPrint, Package, DollarSign } from "lucide-react";

interface Activity {
  id: string;
  type: "crop" | "livestock" | "inventory" | "finance";
  title: string;
  description: string;
  time: string;
}

const activities: Activity[] = [
  {
    id: "1",
    type: "crop",
    title: "Wheat Field Irrigated",
    description: "Field A-12 irrigation completed",
    time: "2 hours ago",
  },
  {
    id: "2",
    type: "livestock",
    title: "Cattle Vaccination",
    description: "25 cattle received annual vaccines",
    time: "4 hours ago",
  },
  {
    id: "3",
    type: "inventory",
    title: "Fertilizer Restocked",
    description: "Added 500kg NPK fertilizer",
    time: "6 hours ago",
  },
  {
    id: "4",
    type: "finance",
    title: "Sale Recorded",
    description: "Sold 2 tons of corn - $4,200",
    time: "1 day ago",
  },
  {
    id: "5",
    type: "crop",
    title: "New Crop Planted",
    description: "Soybeans planted in Field B-3",
    time: "2 days ago",
  },
];

const iconMap = {
  crop: Sprout,
  livestock: PawPrint,
  inventory: Package,
  finance: DollarSign,
};

const colorMap = {
  crop: "bg-success/10 text-success",
  livestock: "bg-warning/10 text-warning",
  inventory: "bg-info/10 text-info",
  finance: "bg-primary/10 text-primary",
};

export function RecentActivity() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="bg-card rounded-xl p-6 shadow-card border border-border/50"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground">Recent Activity</h3>
        <Clock className="w-5 h-5 text-muted-foreground" />
      </div>
      <div className="space-y-4">
        {activities.map((activity, index) => {
          const Icon = iconMap[activity.type];
          return (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + index * 0.1 }}
              className="flex items-start gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className={`p-2 rounded-lg ${colorMap[activity.type]}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-foreground truncate">{activity.title}</p>
                <p className="text-sm text-muted-foreground truncate">
                  {activity.description}
                </p>
              </div>
              <span className="text-xs text-muted-foreground whitespace-nowrap">
                {activity.time}
              </span>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
