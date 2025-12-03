import { motion } from "framer-motion";
import { Cloud, Sun, Droplets, Wind, Thermometer } from "lucide-react";

export function WeatherWidget() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.25 }}
      className="bg-gradient-to-br from-info/20 to-info/5 rounded-xl p-6 shadow-card border border-info/20 overflow-hidden relative"
    >
      <div className="absolute -right-4 -top-4 opacity-10">
        <Sun className="w-32 h-32 text-warning" />
      </div>
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-4">
          <Cloud className="w-5 h-5 text-info" />
          <h3 className="text-lg font-semibold text-foreground">Weather</h3>
        </div>
        
        <div className="flex items-center gap-4 mb-4">
          <div className="text-5xl font-bold text-foreground">24°</div>
          <div>
            <p className="font-medium text-foreground">Partly Cloudy</p>
            <p className="text-sm text-muted-foreground">Perfect for fieldwork</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 pt-4 border-t border-border/50">
          <div className="flex items-center gap-2">
            <Droplets className="w-4 h-4 text-info" />
            <div>
              <p className="text-xs text-muted-foreground">Humidity</p>
              <p className="text-sm font-semibold text-foreground">65%</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Wind className="w-4 h-4 text-muted-foreground" />
            <div>
              <p className="text-xs text-muted-foreground">Wind</p>
              <p className="text-sm font-semibold text-foreground">12 km/h</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Thermometer className="w-4 h-4 text-warning" />
            <div>
              <p className="text-xs text-muted-foreground">Feels like</p>
              <p className="text-sm font-semibold text-foreground">26°</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
