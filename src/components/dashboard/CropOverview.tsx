import { motion } from "framer-motion";
import { Sprout, TrendingUp } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface Crop {
  id: string;
  name: string;
  field: string;
  progress: number;
  stage: string;
  health: "good" | "moderate" | "poor";
}

const crops: Crop[] = [
  { id: "1", name: "Wheat", field: "Field A-12", progress: 85, stage: "Harvest Ready", health: "good" },
  { id: "2", name: "Corn", field: "Field B-7", progress: 60, stage: "Grain Filling", health: "good" },
  { id: "3", name: "Soybeans", field: "Field C-3", progress: 35, stage: "Flowering", health: "moderate" },
  { id: "4", name: "Rice", field: "Field D-1", progress: 15, stage: "Vegetative", health: "good" },
];

const healthColors = {
  good: "bg-success",
  moderate: "bg-warning",
  poor: "bg-destructive",
};

export function CropOverview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-card rounded-xl p-6 shadow-card border border-border/50"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Sprout className="w-5 h-5 text-success" />
          <h3 className="text-lg font-semibold text-foreground">Crop Overview</h3>
        </div>
        <TrendingUp className="w-5 h-5 text-success" />
      </div>
      <div className="space-y-4">
        {crops.map((crop, index) => (
          <motion.div
            key={crop.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 + index * 0.1 }}
            className="p-4 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="font-semibold text-foreground">{crop.name}</p>
                <p className="text-sm text-muted-foreground">{crop.field}</p>
              </div>
              <div className="text-right">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${healthColors[crop.health]}`} />
                  <span className="text-sm font-medium text-foreground">{crop.stage}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Progress value={crop.progress} className="flex-1 h-2" />
              <span className="text-sm font-semibold text-primary w-12 text-right">
                {crop.progress}%
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
