import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import {
  Plus,
  DollarSign,
  TrendingUp,
  TrendingDown,
  ArrowUpRight,
  ArrowDownRight,
  Download,
  Calendar,
  CreditCard,
  Wallet,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";

const revenueData = [
  { month: "Jan", revenue: 12000, expenses: 8000 },
  { month: "Feb", revenue: 15000, expenses: 9500 },
  { month: "Mar", revenue: 18000, expenses: 11000 },
  { month: "Apr", revenue: 22000, expenses: 12500 },
  { month: "May", revenue: 28000, expenses: 15000 },
  { month: "Jun", revenue: 32000, expenses: 16500 },
  { month: "Jul", revenue: 35000, expenses: 18000 },
  { month: "Aug", revenue: 30000, expenses: 17000 },
  { month: "Sep", revenue: 26000, expenses: 14500 },
  { month: "Oct", revenue: 24000, expenses: 13000 },
  { month: "Nov", revenue: 28000, expenses: 14000 },
  { month: "Dec", revenue: 24500, expenses: 12500 },
];

interface Transaction {
  id: string;
  type: "income" | "expense";
  category: string;
  description: string;
  amount: number;
  date: string;
}

const transactions: Transaction[] = [
  {
    id: "1",
    type: "income",
    category: "Crop Sales",
    description: "Sold 5 tons of wheat",
    amount: 8500,
    date: "Nov 26, 2024",
  },
  {
    id: "2",
    type: "expense",
    category: "Equipment",
    description: "Tractor maintenance",
    amount: 1200,
    date: "Nov 25, 2024",
  },
  {
    id: "3",
    type: "income",
    category: "Livestock Sales",
    description: "Sold 10 cattle",
    amount: 15000,
    date: "Nov 24, 2024",
  },
  {
    id: "4",
    type: "expense",
    category: "Supplies",
    description: "Fertilizer purchase",
    amount: 2500,
    date: "Nov 23, 2024",
  },
  {
    id: "5",
    type: "expense",
    category: "Labor",
    description: "Seasonal workers payment",
    amount: 4000,
    date: "Nov 22, 2024",
  },
  {
    id: "6",
    type: "income",
    category: "Crop Sales",
    description: "Corn harvest sale",
    amount: 12000,
    date: "Nov 20, 2024",
  },
];

const Finance = () => {
  const totalRevenue = revenueData.reduce((acc, curr) => acc + curr.revenue, 0);
  const totalExpenses = revenueData.reduce((acc, curr) => acc + curr.expenses, 0);
  const netProfit = totalRevenue - totalExpenses;
  const profitMargin = ((netProfit / totalRevenue) * 100).toFixed(1);

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
            <h1 className="text-3xl font-bold text-foreground">Financial Management</h1>
            <p className="text-muted-foreground mt-1">
              Track revenue, expenses, and profitability
            </p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <Download className="w-4 h-4" />
              Export
            </Button>
            <Button variant="hero" size="lg">
              <Plus className="w-5 h-5" />
              Add Transaction
            </Button>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-success/10">
                <DollarSign className="w-6 h-6 text-success" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-success">
                <TrendingUp className="w-4 h-4" />
                +12%
              </span>
            </div>
            <p className="text-sm text-muted-foreground mb-1">Total Revenue</p>
            <p className="text-2xl font-bold text-foreground">${totalRevenue.toLocaleString()}</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-destructive/10">
                <CreditCard className="w-6 h-6 text-destructive" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-destructive">
                <TrendingDown className="w-4 h-4" />
                +8%
              </span>
            </div>
            <p className="text-sm text-muted-foreground mb-1">Total Expenses</p>
            <p className="text-2xl font-bold text-foreground">${totalExpenses.toLocaleString()}</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-primary/10">
                <Wallet className="w-6 h-6 text-primary" />
              </div>
              <span className="flex items-center gap-1 text-sm font-medium text-success">
                <TrendingUp className="w-4 h-4" />
                +18%
              </span>
            </div>
            <p className="text-sm text-muted-foreground mb-1">Net Profit</p>
            <p className="text-2xl font-bold text-foreground">${netProfit.toLocaleString()}</p>
          </div>

          <div className="bg-card rounded-xl p-6 shadow-card border border-border/50">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-info/10">
                <TrendingUp className="w-6 h-6 text-info" />
              </div>
            </div>
            <p className="text-sm text-muted-foreground mb-1">Profit Margin</p>
            <p className="text-2xl font-bold text-foreground">{profitMargin}%</p>
          </div>
        </motion.div>

        {/* Charts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-card rounded-xl p-6 shadow-card border border-border/50"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground">Revenue vs Expenses</h3>
              <p className="text-sm text-muted-foreground">Monthly financial overview</p>
            </div>
            <Button variant="outline" size="sm" className="gap-2">
              <Calendar className="w-4 h-4" />
              2024
            </Button>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(142, 45%, 28%)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="hsl(142, 45%, 28%)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(0, 72%, 51%)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="hsl(0, 72%, 51%)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis
                  dataKey="month"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) => `$${value / 1000}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                  formatter={(value: number) => [`$${value.toLocaleString()}`, ""]}
                />
                <Area
                  type="monotone"
                  dataKey="revenue"
                  stroke="hsl(142, 45%, 28%)"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorRevenue)"
                  name="Revenue"
                />
                <Area
                  type="monotone"
                  dataKey="expenses"
                  stroke="hsl(0, 72%, 51%)"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorExpenses)"
                  name="Expenses"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Recent Transactions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-card rounded-xl p-6 shadow-card border border-border/50"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-foreground">Recent Transactions</h3>
            <Button variant="ghost" size="sm">
              View All
            </Button>
          </div>
          <div className="space-y-4">
            {transactions.map((transaction, index) => (
              <motion.div
                key={transaction.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.05 }}
                className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div
                    className={cn(
                      "p-2 rounded-lg",
                      transaction.type === "income"
                        ? "bg-success/10"
                        : "bg-destructive/10"
                    )}
                  >
                    {transaction.type === "income" ? (
                      <ArrowUpRight className="w-5 h-5 text-success" />
                    ) : (
                      <ArrowDownRight className="w-5 h-5 text-destructive" />
                    )}
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{transaction.description}</p>
                    <p className="text-sm text-muted-foreground">{transaction.category}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p
                    className={cn(
                      "font-semibold",
                      transaction.type === "income" ? "text-success" : "text-destructive"
                    )}
                  >
                    {transaction.type === "income" ? "+" : "-"}$
                    {transaction.amount.toLocaleString()}
                  </p>
                  <p className="text-sm text-muted-foreground">{transaction.date}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </AppLayout>
  );
};

export default Finance;
