import { ReactNode } from "react";
import { AppSidebar } from "./AppSidebar";
import { motion } from "framer-motion";

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <AppSidebar />
      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="lg:ml-64 min-h-screen"
      >
        <div className="p-4 lg:p-8 pt-16 lg:pt-8">
          {children}
        </div>
      </motion.main>
    </div>
  );
}
