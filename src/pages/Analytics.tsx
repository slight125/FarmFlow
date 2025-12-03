import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import {
  Download,
  Calendar,
  TrendingUp,
  TrendingDown,
  Sprout,
  PawPrint,
  DollarSign,
  Package,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend,
} from "recharts";

const cropYieldData = [
  { crop: "Wheat", yield: 4.5, target: 4.2 },
  { crop: "Corn", yield: 3.8, target: 4.0 },
  { crop: "Soybeans", yield: 2.9, target: 3.0 },
  { crop: "Rice", yield: 5.2, target: 5.0 },
  { crop: "Potatoes", yield: 8.5, target: 8.0 },
];

const livestockDistribution = [
  { name: "Cattle", value: 150, color: "hsl(142, 45%, 28%)" },
  { name: "Sheep", value: 80, color: "hsl(38, 92%, 50%)" },
  { name: "Pigs", value: 45, color: "hsl(199, 89%, 48%)" },
  { name: "Chickens", value: 200, color: "hsl(0, 72%, 51%)" },
  { name: "Goats", value: 30, color: "hsl(150, 30%, 15%)" },
];

const monthlyProductivity = [
  { month: "Jan", crops: 75, livestock: 82 },
  { month: "Feb", crops: 78, livestock: 80 },
  { month: "Mar", crops: 85, livestock: 85 },
  { month: "Apr", crops: 90, livestock: 88 },
  { month: "May", crops: 95, livestock: 90 },
  { month: "Jun", crops: 92, livestock: 87 },
  { month: "Jul", crops: 88, livestock: 85 },
  { month: "Aug", crops: 82, livestock: 88 },
  { month: "Sep", crops: 78, livestock: 90 },
  { month: "Oct", crops: 80, livestock: 92 },
  { month: "Nov", crops: 85, livestock: 88 },
  { month: "Dec", crops: 82, livestock: 85 },
];

const resourceUtilization = [
  { resource: "Water", usage: 78 },
  { resource: "Fertilizer", usage: 65 },
  { resource: "Feed", usage: 82 },
  { resource: "Labor", usage: 70 },
  { resource: "Equipment", usage: 55 },
];

const Analytics = () => {
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
            <h1 className="text-3xl font-bold text-foreground">Analytics Dashboard</h1>
            <p className="text-muted-foreground mt-1">
              Comprehensive insights into farm performance
            </p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <Calendar className="w-4 h-4" />
              Last 12 months
            </Button>
            <Button variant="hero" className="gap-2">
              <Download className="w-4 h-4" />
              Export Report
            </Button>
          </div>
        </motion.div>

        {/* KPI Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-2">
              <div className="p-2 rounded-lg bg-success/10">
                <Sprout className="w-5 h-5 text-success" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-success">
                <TrendingUp className="w-4 h-4" />
                +15%
              </span>
            </div>
            <p className="text-2xl font-bold text-foreground">4.2 t/ha</p>
            <p className="text-sm text-muted-foreground">Avg Crop Yield</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-2">
              <div className="p-2 rounded-lg bg-warning/10">
                <PawPrint className="w-5 h-5 text-warning" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-success">
                <TrendingUp className="w-4 h-4" />
                +8%
              </span>
            </div>
            <p className="text-2xl font-bold text-foreground">92%</p>
            <p className="text-sm text-muted-foreground">Livestock Health</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-2">
              <div className="p-2 rounded-lg bg-primary/10">
                <DollarSign className="w-5 h-5 text-primary" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-success">
                <TrendingUp className="w-4 h-4" />
                +22%
              </span>
            </div>
            <p className="text-2xl font-bold text-foreground">$294K</p>
            <p className="text-sm text-muted-foreground">Annual Revenue</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-2">
              <div className="p-2 rounded-lg bg-info/10">
                <Package className="w-5 h-5 text-info" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-destructive">
                <TrendingDown className="w-4 h-4" />
                -5%
              </span>
            </div>
            <p className="text-2xl font-bold text-foreground">72%</p>
            <p className="text-sm text-muted-foreground">Resource Efficiency</p>
          </div>
        </motion.div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Crop Yield Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-card rounded-xl p-6 shadow-card border border-border/50"
          >
            <h3 className="text-lg font-semibold text-foreground mb-6">Crop Yield vs Target (t/ha)</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={cropYieldData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis
                    dataKey="crop"
                    type="category"
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={12}
                    width={80}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Bar dataKey="yield" fill="hsl(142, 45%, 28%)" radius={[0, 4, 4, 0]} name="Actual" />
                  <Bar dataKey="target" fill="hsl(var(--muted))" radius={[0, 4, 4, 0]} name="Target" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Livestock Distribution */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="bg-card rounded-xl p-6 shadow-card border border-border/50"
          >
            <h3 className="text-lg font-semibold text-foreground mb-6">Livestock Distribution</h3>
            <div className="h-64 flex items-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={livestockDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {livestockDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-2">
                {livestockDistribution.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <span
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm text-muted-foreground">{item.name}</span>
                    <span className="text-sm font-medium text-foreground">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Productivity Trends */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-card rounded-xl p-6 shadow-card border border-border/50"
        >
          <h3 className="text-lg font-semibold text-foreground mb-6">Monthly Productivity Index</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyProductivity}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis
                  dataKey="month"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                  domain={[60, 100]}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="crops"
                  stroke="hsl(142, 45%, 28%)"
                  strokeWidth={3}
                  dot={{ fill: "hsl(142, 45%, 28%)", strokeWidth: 2 }}
                  name="Crops"
                />
                <Line
                  type="monotone"
                  dataKey="livestock"
                  stroke="hsl(38, 92%, 50%)"
                  strokeWidth={3}
                  dot={{ fill: "hsl(38, 92%, 50%)", strokeWidth: 2 }}
                  name="Livestock"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Resource Utilization */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          className="bg-card rounded-xl p-6 shadow-card border border-border/50"
        >
          <h3 className="text-lg font-semibold text-foreground mb-6">Resource Utilization (%)</h3>
          <div className="space-y-4">
            {resourceUtilization.map((resource, index) => (
              <motion.div
                key={resource.resource}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.05 }}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-foreground">{resource.resource}</span>
                  <span className="text-sm font-semibold text-primary">{resource.usage}%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${resource.usage}%` }}
                    transition={{ duration: 0.8, delay: 0.5 + index * 0.1 }}
                    className="h-full bg-primary rounded-full"
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </AppLayout>
  );
};

export default Analytics;
