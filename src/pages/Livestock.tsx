import { useState } from "react";
import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import {
  Plus,
  Search,
  Filter,
  PawPrint,
  Heart,
  Calendar,
  Scale,
  Syringe,
  MoreVertical,
  AlertCircle,
  CheckCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Animal {
  id: string;
  type: string;
  breed: string;
  tag: string;
  age: string;
  weight: string;
  healthStatus: "healthy" | "needs-attention" | "sick";
  lastCheckup: string;
  nextVaccination: string;
  location: string;
}

const animals: Animal[] = [
  {
    id: "1",
    type: "Cattle",
    breed: "Angus",
    tag: "C-001",
    age: "3 years",
    weight: "650 kg",
    healthStatus: "healthy",
    lastCheckup: "Nov 15, 2024",
    nextVaccination: "Feb 2025",
    location: "Pasture A",
  },
  {
    id: "2",
    type: "Cattle",
    breed: "Holstein",
    tag: "C-042",
    age: "2 years",
    weight: "580 kg",
    healthStatus: "needs-attention",
    lastCheckup: "Oct 28, 2024",
    nextVaccination: "Dec 2024",
    location: "Barn B",
  },
  {
    id: "3",
    type: "Sheep",
    breed: "Merino",
    tag: "S-015",
    age: "1.5 years",
    weight: "75 kg",
    healthStatus: "healthy",
    lastCheckup: "Nov 20, 2024",
    nextVaccination: "Mar 2025",
    location: "Pasture C",
  },
  {
    id: "4",
    type: "Pig",
    breed: "Yorkshire",
    tag: "P-008",
    age: "8 months",
    weight: "120 kg",
    healthStatus: "healthy",
    lastCheckup: "Nov 18, 2024",
    nextVaccination: "Jan 2025",
    location: "Pen D",
  },
  {
    id: "5",
    type: "Chicken",
    breed: "Rhode Island Red",
    tag: "CH-Flock1",
    age: "6 months",
    weight: "3.5 kg (avg)",
    healthStatus: "healthy",
    lastCheckup: "Nov 22, 2024",
    nextVaccination: "Apr 2025",
    location: "Coop E",
  },
  {
    id: "6",
    type: "Goat",
    breed: "Boer",
    tag: "G-023",
    age: "2 years",
    weight: "85 kg",
    healthStatus: "sick",
    lastCheckup: "Nov 25, 2024",
    nextVaccination: "Pending",
    location: "Barn F",
  },
];

const healthColors = {
  healthy: { bg: "bg-success/10", text: "text-success", icon: CheckCircle },
  "needs-attention": { bg: "bg-warning/10", text: "text-warning", icon: AlertCircle },
  sick: { bg: "bg-destructive/10", text: "text-destructive", icon: AlertCircle },
};

const typeIcons: Record<string, string> = {
  Cattle: "🐄",
  Sheep: "🐑",
  Pig: "🐷",
  Chicken: "🐔",
  Goat: "🐐",
};

const Livestock = () => {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredAnimals = animals.filter(
    (animal) =>
      animal.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
      animal.tag.toLowerCase().includes(searchQuery.toLowerCase()) ||
      animal.breed.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const stats = {
    total: animals.length,
    healthy: animals.filter((a) => a.healthStatus === "healthy").length,
    needsAttention: animals.filter((a) => a.healthStatus === "needs-attention").length,
    sick: animals.filter((a) => a.healthStatus === "sick").length,
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
            <h1 className="text-3xl font-bold text-foreground">Livestock Management</h1>
            <p className="text-muted-foreground mt-1">
              Track health, breeding, and care for all animals
            </p>
          </div>
          <Button variant="hero" size="lg">
            <Plus className="w-5 h-5" />
            Add Animal
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
                <PawPrint className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.total}</p>
                <p className="text-sm text-muted-foreground">Total Animals</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-success/10">
                <Heart className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.healthy}</p>
                <p className="text-sm text-muted-foreground">Healthy</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-warning/10">
                <AlertCircle className="w-5 h-5 text-warning" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.needsAttention}</p>
                <p className="text-sm text-muted-foreground">Needs Attention</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-destructive/10">
                <Syringe className="w-5 h-5 text-destructive" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.sick}</p>
                <p className="text-sm text-muted-foreground">Under Treatment</p>
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
              placeholder="Search by type, tag, or breed..."
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

        {/* Animals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredAnimals.map((animal, index) => {
            const HealthIcon = healthColors[animal.healthStatus].icon;
            return (
              <motion.div
                key={animal.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="bg-card rounded-xl p-6 shadow-card border border-border/50 card-hover"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-muted flex items-center justify-center text-2xl">
                      {typeIcons[animal.type] || "🐾"}
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground text-lg">{animal.type}</h3>
                      <p className="text-sm text-muted-foreground">{animal.breed}</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                    <MoreVertical className="w-5 h-5 text-muted-foreground" />
                  </button>
                </div>

                <div className="flex items-center gap-2 mb-4">
                  <span className="px-3 py-1 bg-muted rounded-full text-sm font-mono font-medium text-foreground">
                    {animal.tag}
                  </span>
                  <span
                    className={cn(
                      "px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1",
                      healthColors[animal.healthStatus].bg,
                      healthColors[animal.healthStatus].text
                    )}
                  >
                    <HealthIcon className="w-3 h-3" />
                    {animal.healthStatus === "needs-attention"
                      ? "Needs Attention"
                      : animal.healthStatus.charAt(0).toUpperCase() + animal.healthStatus.slice(1)}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      Age
                    </span>
                    <span className="font-medium text-foreground">{animal.age}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Scale className="w-4 h-4" />
                      Weight
                    </span>
                    <span className="font-medium text-foreground">{animal.weight}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-2">
                      <Syringe className="w-4 h-4" />
                      Next Vaccine
                    </span>
                    <span className="font-medium text-foreground">{animal.nextVaccination}</span>
                  </div>
                </div>

                <div className="pt-4 border-t border-border/50">
                  <p className="text-xs text-muted-foreground">
                    Last checkup: {animal.lastCheckup}
                  </p>
                  <p className="text-xs text-muted-foreground">Location: {animal.location}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </AppLayout>
  );
};

export default Livestock;
