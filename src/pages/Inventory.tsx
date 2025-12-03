import { useState } from "react";
import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Plus,
  Search,
  Filter,
  Package,
  AlertTriangle,
  Truck,
  Wrench,
  Leaf,
  Droplets,
  MoreVertical,
  TrendingDown,
  CheckCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface InventoryItem {
  id: string;
  name: string;
  category: "seeds" | "fertilizers" | "pesticides" | "feed" | "equipment" | "fuel";
  quantity: number;
  unit: string;
  minStock: number;
  maxStock: number;
  lastUpdated: string;
  location: string;
  status: "in-stock" | "low-stock" | "out-of-stock";
}

const inventoryItems: InventoryItem[] = [
  {
    id: "1",
    name: "Wheat Seeds",
    category: "seeds",
    quantity: 500,
    unit: "kg",
    minStock: 100,
    maxStock: 1000,
    lastUpdated: "Nov 25, 2024",
    location: "Storage A",
    status: "in-stock",
  },
  {
    id: "2",
    name: "NPK Fertilizer",
    category: "fertilizers",
    quantity: 80,
    unit: "bags",
    minStock: 50,
    maxStock: 200,
    lastUpdated: "Nov 20, 2024",
    location: "Storage B",
    status: "low-stock",
  },
  {
    id: "3",
    name: "Insecticide Spray",
    category: "pesticides",
    quantity: 25,
    unit: "liters",
    minStock: 20,
    maxStock: 100,
    lastUpdated: "Nov 22, 2024",
    location: "Chemical Store",
    status: "low-stock",
  },
  {
    id: "4",
    name: "Cattle Feed",
    category: "feed",
    quantity: 2000,
    unit: "kg",
    minStock: 500,
    maxStock: 5000,
    lastUpdated: "Nov 24, 2024",
    location: "Feed Barn",
    status: "in-stock",
  },
  {
    id: "5",
    name: "Tractor Parts",
    category: "equipment",
    quantity: 0,
    unit: "sets",
    minStock: 5,
    maxStock: 20,
    lastUpdated: "Nov 18, 2024",
    location: "Workshop",
    status: "out-of-stock",
  },
  {
    id: "6",
    name: "Diesel Fuel",
    category: "fuel",
    quantity: 450,
    unit: "liters",
    minStock: 200,
    maxStock: 1000,
    lastUpdated: "Nov 26, 2024",
    location: "Fuel Tank",
    status: "in-stock",
  },
];

const categoryIcons = {
  seeds: { icon: Leaf, color: "text-success bg-success/10" },
  fertilizers: { icon: Package, color: "text-primary bg-primary/10" },
  pesticides: { icon: Droplets, color: "text-warning bg-warning/10" },
  feed: { icon: Package, color: "text-accent bg-accent/10" },
  equipment: { icon: Wrench, color: "text-info bg-info/10" },
  fuel: { icon: Truck, color: "text-destructive bg-destructive/10" },
};

const statusConfig = {
  "in-stock": { color: "bg-success text-success-foreground", icon: CheckCircle },
  "low-stock": { color: "bg-warning text-warning-foreground", icon: AlertTriangle },
  "out-of-stock": { color: "bg-destructive text-destructive-foreground", icon: TrendingDown },
};

const Inventory = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const filteredItems = inventoryItems.filter((item) => {
    const matchesSearch =
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const stats = {
    total: inventoryItems.length,
    inStock: inventoryItems.filter((i) => i.status === "in-stock").length,
    lowStock: inventoryItems.filter((i) => i.status === "low-stock").length,
    outOfStock: inventoryItems.filter((i) => i.status === "out-of-stock").length,
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
            <h1 className="text-3xl font-bold text-foreground">Inventory Management</h1>
            <p className="text-muted-foreground mt-1">
              Track stock levels and manage farm resources
            </p>
          </div>
          <Button variant="hero" size="lg">
            <Plus className="w-5 h-5" />
            Add Item
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
                <Package className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.total}</p>
                <p className="text-sm text-muted-foreground">Total Items</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-success/10">
                <CheckCircle className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.inStock}</p>
                <p className="text-sm text-muted-foreground">In Stock</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-warning/10">
                <AlertTriangle className="w-5 h-5 text-warning" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.lowStock}</p>
                <p className="text-sm text-muted-foreground">Low Stock</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl p-4 shadow-card border border-border/50">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-destructive/10">
                <TrendingDown className="w-5 h-5 text-destructive" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stats.outOfStock}</p>
                <p className="text-sm text-muted-foreground">Out of Stock</p>
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
              placeholder="Search inventory..."
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

        {/* Category Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="flex flex-wrap gap-2"
        >
          <Button
            variant={selectedCategory === null ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory(null)}
          >
            All
          </Button>
          {Object.entries(categoryIcons).map(([key, { icon: Icon }]) => (
            <Button
              key={key}
              variant={selectedCategory === key ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCategory(key)}
              className="capitalize"
            >
              <Icon className="w-4 h-4 mr-1" />
              {key}
            </Button>
          ))}
        </motion.div>

        {/* Inventory Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredItems.map((item, index) => {
            const CategoryIcon = categoryIcons[item.category].icon;
            const StatusIcon = statusConfig[item.status].icon;
            const stockPercentage = (item.quantity / item.maxStock) * 100;

            return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="bg-card rounded-xl p-6 shadow-card border border-border/50 card-hover"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={cn("p-3 rounded-xl", categoryIcons[item.category].color)}>
                      <CategoryIcon className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground text-lg">{item.name}</h3>
                      <p className="text-sm text-muted-foreground capitalize">{item.category}</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-muted rounded-lg transition-colors">
                    <MoreVertical className="w-5 h-5 text-muted-foreground" />
                  </button>
                </div>

                <div className="mb-4">
                  <div className="flex items-baseline gap-2 mb-2">
                    <span className="text-3xl font-bold text-foreground">{item.quantity}</span>
                    <span className="text-muted-foreground">{item.unit}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-muted-foreground">Stock Level</span>
                    <span className="font-medium text-foreground">{Math.round(stockPercentage)}%</span>
                  </div>
                  <Progress
                    value={stockPercentage}
                    className={cn(
                      "h-2",
                      item.status === "low-stock" && "[&>div]:bg-warning",
                      item.status === "out-of-stock" && "[&>div]:bg-destructive"
                    )}
                  />
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-border/50">
                  <span
                    className={cn(
                      "px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1",
                      statusConfig[item.status].color
                    )}
                  >
                    <StatusIcon className="w-3 h-3" />
                    {item.status.replace("-", " ")}
                  </span>
                  <span className="text-xs text-muted-foreground">{item.location}</span>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </AppLayout>
  );
};

export default Inventory;
