import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import {
  User,
  Bell,
  Shield,
  Palette,
  Globe,
  Database,
  HelpCircle,
  ChevronRight,
  Mail,
  Smartphone,
  Lock,
  Users,
  Building,
  MapPin,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SettingSection {
  title: string;
  description: string;
  icon: React.ElementType;
  items: {
    label: string;
    value?: string;
    action?: string;
  }[];
}

const settingSections: SettingSection[] = [
  {
    title: "Profile",
    description: "Manage your personal information",
    icon: User,
    items: [
      { label: "Full Name", value: "John Farmer" },
      { label: "Email", value: "john@greenvalleyfarm.com" },
      { label: "Phone", value: "+1 (555) 123-4567" },
      { label: "Role", value: "Farm Manager" },
    ],
  },
  {
    title: "Farm Details",
    description: "Your farm information and location",
    icon: Building,
    items: [
      { label: "Farm Name", value: "Green Valley Farm" },
      { label: "Location", value: "Rural County, State" },
      { label: "Total Area", value: "500 acres" },
      { label: "Established", value: "1985" },
    ],
  },
  {
    title: "Notifications",
    description: "Configure how you receive alerts",
    icon: Bell,
    items: [
      { label: "Email Notifications", action: "Enabled" },
      { label: "Push Notifications", action: "Enabled" },
      { label: "SMS Alerts", action: "Disabled" },
      { label: "Weekly Reports", action: "Enabled" },
    ],
  },
  {
    title: "Team Members",
    description: "Manage farm workers and access",
    icon: Users,
    items: [
      { label: "Total Members", value: "8 users" },
      { label: "Admins", value: "2 users" },
      { label: "Workers", value: "6 users" },
      { label: "Pending Invites", value: "1" },
    ],
  },
  {
    title: "Security",
    description: "Protect your account",
    icon: Shield,
    items: [
      { label: "Password", action: "Change" },
      { label: "Two-Factor Auth", action: "Disabled" },
      { label: "Active Sessions", value: "2 devices" },
      { label: "Login History", action: "View" },
    ],
  },
  {
    title: "Data & Privacy",
    description: "Manage your data and exports",
    icon: Database,
    items: [
      { label: "Export Data", action: "Download" },
      { label: "Data Retention", value: "2 years" },
      { label: "Analytics", action: "Enabled" },
      { label: "Delete Account", action: "Request" },
    ],
  },
];

const Settings = () => {
  return (
    <AppLayout>
      <div className="space-y-6 max-w-4xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          <p className="text-muted-foreground mt-1">
            Manage your account and farm preferences
          </p>
        </motion.div>

        {/* Settings Sections */}
        <div className="space-y-6">
          {settingSections.map((section, sectionIndex) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: sectionIndex * 0.1 }}
              className="bg-card rounded-xl shadow-card border border-border/50 overflow-hidden"
            >
              <div className="p-6 border-b border-border/50">
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-xl bg-primary/10">
                    <section.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-foreground">{section.title}</h2>
                    <p className="text-sm text-muted-foreground">{section.description}</p>
                  </div>
                </div>
              </div>
              <div className="divide-y divide-border/50">
                {section.items.map((item, itemIndex) => (
                  <motion.div
                    key={item.label}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: sectionIndex * 0.1 + itemIndex * 0.05 }}
                    className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors cursor-pointer group"
                  >
                    <span className="text-foreground">{item.label}</span>
                    <div className="flex items-center gap-2">
                      {item.value && (
                        <span className="text-muted-foreground">{item.value}</span>
                      )}
                      {item.action && (
                        <span
                          className={cn(
                            "text-sm font-medium",
                            item.action === "Enabled"
                              ? "text-success"
                              : item.action === "Disabled"
                              ? "text-muted-foreground"
                              : "text-primary"
                          )}
                        >
                          {item.action}
                        </span>
                      )}
                      <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors" />
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Help Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl p-6 border border-primary/20"
        >
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-xl bg-primary/10">
              <HelpCircle className="w-6 h-6 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-foreground">Need Help?</h3>
              <p className="text-muted-foreground mt-1 mb-4">
                Our support team is here to help you get the most out of FarmFlow.
              </p>
              <div className="flex flex-wrap gap-3">
                <Button variant="default">Contact Support</Button>
                <Button variant="outline">View Documentation</Button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Version Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="text-center py-4"
        >
          <p className="text-sm text-muted-foreground">
            FarmFlow v1.0.0 • Made with 🌱 for farmers everywhere
          </p>
        </motion.div>
      </div>
    </AppLayout>
  );
};

export default Settings;
