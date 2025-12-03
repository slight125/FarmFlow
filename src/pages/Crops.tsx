import { useState } from "react";
import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Plus,
  Search,
  Filter,
  Sprout,
  Droplets,
  Sun,
  Calendar,
  MapPin,
  MoreVertical,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Crop {
  id: string;
  name: string;
  variety: string;
  field: string;
  area: string;
  plantedDate: string;
  expectedHarvest: string;
  progress: number;
  stage: string;
  health: "excellent" | "good" | "moderate" | "poor";
  lastActivity: string;
  irrigation: "optimal" | "needs-water" | "excess";
}

const crops: Crop[] = [
  {
    id: "1",
    name: "Wheat",
    variety: "Hard Red Winter",
    field: "Field A-12",
    area: "45 acres",
    plantedDate: "Oct 15, 2024",
    expectedHarvest: "Jul 2025",
    progress: 85,
    stage: "Harvest Ready",
    health: "excellent",
    lastActivity: "Fertilized 3 days ago",
    irrigation: "optimal",
  },
  {
    id: "2",
    name: "Corn",
    variety: "Yellow Dent",
    field: "Field B-7",
    area: "60 acres",
    plantedDate: "Apr 20, 2024",
    expectedHarvest: "Sep 2024",
    progress: 60,
    stage: "Grain Filling",
    health: "good",
    lastActivity: "Irrigated yesterday",
    irrigation: "optimal",
  },
  {
    id: "3",
    name: "Soybeans",
    variety: "Roundup Ready",
    field: "Field C-3",
    area: "30 acres",
    plantedDate: "May 10, 2024",
    expectedHarvest: "Oct 2024",
    progress: 35,
    stage: "Flowering",
    health: "moderate",
    lastActivity: "Pest inspection needed",
    irrigation: "needs-water",
  },
  {
    id: "4",
    name: "Rice",
    variety: "Long Grain",
    field: "Field D-1",
    area: "25 acres",
    plantedDate: "Jun 1, 2024",
    expectedHarvest: "Nov 2024",
    progress: 15,
    stage: "Vegetative",
    health: "excellent",
    lastActivity: "Flooded paddies maintained",
    irrigation: "optimal",
  },
  {
    id: "5",
    name: "Potatoes",
    variety: "Russet Burbank",
    field: "Field E-5",
    area: "20 acres",
    plantedDate: "Mar 25, 2024",
    expectedHarvest: "Aug 2024",
    progress: 70,
    stage: "Tuber Bulking",
    health: "good",
    lastActivity: "Hilling completed",
    irrigation: "optimal",
  },
];

const healthColors = {
  excellent: "bg-success text-success-foreground",
  good: "bg-primary text-primary-foreground",
  moderate: "bg-warning text-warning-foreground",
  poor: "bg-destructive text-destructive-foreground",
};

const irrigationIcons = {
  optimal: { icon: Droplets, color: "text-success" },
  "needs-water": { icon: AlertTriangle, color: "text-warning" },
  excess: { icon: Droplets, color: "text-info" },
};

const Crops = () => {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredCrops = crops.filter(
    (crop) =>
      crop.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      crop.field.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
            <h1 className="text-3xl font-bold text-foreground">Crop Management</h1>
            <p className="text-muted-foreground mt-1">
              Track and manage all your crop cycles
            </p>
          </div>
          <Button variant="hero" size="lg">
            <Plus className="w-5 h-5" />
            Add New Crop
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
              <div className="p-2 rounded-lg bg-success/10">
                <Sprout className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">5</p>
                <p className="text-sm text-muted-foreground">Active Crops</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10">
                <MapPin className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">180</p>
                <p className="text-sm text-muted-foreground">Total Acres</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-warning/10">
                <Calendar className="w-5 h-5 text-warning" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">2</p>
                <p className="text-sm text-muted-foreground">Harvest Ready</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-info/10">
                <TrendingUp className="w-5 h-5 text-info" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">+18%</p>
                <p className="text-sm text-muted-foreground">Yield Estimate</p>
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
              placeholder="Search crops or fields..."
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

        {/* Crops Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredCrops.map((crop, index) => {
            const IrrigationIcon = irrigationIcons[crop.irrigation].icon;
            return (
              <motion.div
                key={crop.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="bg-card rounded-xl p-6 shadow-card border border-border/50 card-hover"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-xl bg-success/10">
                      <Sprout className="w-6 h-6 text-success" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground text-lg">{crop.name}</h3>
                      <p className="text-sm text-muted-foreground">{crop.variety}</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                    <MoreVertical className="w-5 h-5 text-muted-foreground" />
                  </button>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <MapPin className="w-4 h-4" />
                      {crop.field}
                    </span>
                    <span className="font-medium text-foreground">{crop.area}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      Harvest
                    </span>
                    <span className="font-medium text-foreground">{crop.expectedHarvest}</span>
                  </div>
                </div>

                <div className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-foreground">{crop.stage}</span>
                    <span className="text-sm font-bold text-primary">{crop.progress}%</span>
                  </div>
                  <Progress value={crop.progress} className="h-2" />
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-border/50">
                  <span
                    className={cn(
                      "px-3 py-1 rounded-full text-xs font-medium capitalize",
                      healthColors[crop.health]
                    )}
                  >
                    {crop.health}
                  </span>
                  <div className="flex items-center gap-2">
                    <IrrigationIcon
                      className={cn("w-4 h-4", irrigationIcons[crop.irrigation].color)}
                    />
                    <Sun className="w-4 h-4 text-warning" />
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

export default Crops;
