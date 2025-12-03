import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { StatCard } from "@/components/dashboard/StatCard";
import { RecentActivity } from "@/components/dashboard/RecentActivity";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { WeatherWidget } from "@/components/dashboard/WeatherWidget";
import { UpcomingTasks } from "@/components/dashboard/UpcomingTasks";
import { CropOverview } from "@/components/dashboard/CropOverview";
import { Sprout, PawPrint, Package, DollarSign, TrendingUp, Users } from "lucide-react";

const stats = [
  {
    title: "Active Crops",
    value: 12,
    change: "+2 this month",
    changeType: "positive" as const,
    icon: Sprout,
    iconBg: "bg-success/10",
  },
  {
    title: "Livestock",
    value: 245,
    change: "+15 this week",
    changeType: "positive" as const,
    icon: PawPrint,
    iconBg: "bg-warning/10",
  },
  {
    title: "Inventory Items",
    value: 89,
    change: "3 low stock",
    changeType: "neutral" as const,
    icon: Package,
    iconBg: "bg-info/10",
  },
  {
    title: "Monthly Revenue",
    value: "$24,500",
    change: "+12% vs last month",
    changeType: "positive" as const,
    icon: DollarSign,
    iconBg: "bg-primary/10",
  },
];

const Index = () => {
  return (
    <AppLayout>
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row md:items-center justify-between gap-4"
        >
          <div>
            <h1 className="text-3xl font-bold text-foreground">
              Good morning, <span className="text-primary">Farmer</span>
            </h1>
            <p className="text-muted-foreground mt-1">
              Here's what's happening on your farm today
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground bg-card px-4 py-2 rounded-lg shadow-sm border border-border/50">
            <Users className="w-4 h-4" />
            <span>Green Valley Farm</span>
            <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, index) => (
            <StatCard key={stat.title} {...stat} delay={index * 0.1} />
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            <CropOverview />
            <RecentActivity />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <WeatherWidget />
            <QuickActions />
            <UpcomingTasks />
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default Index;
