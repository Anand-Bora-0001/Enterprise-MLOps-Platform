
import { Activity, Database, Server, AlertTriangle } from "lucide-react"

export default function Dashboard() {
  const stats = [
    { name: "Active Models", value: "12", icon: Activity, trend: "+2.5%" },
    { name: "Total Datasets", value: "48", icon: Database, trend: "+12%" },
    { name: "Deployments", value: "8", icon: Server, trend: "Stable" },
    { name: "Active Alerts", value: "3", icon: AlertTriangle, trend: "-1" },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Overview</h2>
        <p className="text-gray-400">Welcome back. Here's what's happening with your models today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-400">{stat.name}</h3>
                <div className="p-2 bg-gray-800 rounded-lg text-blue-400">
                  <Icon className="h-4 w-4" />
                </div>
              </div>
              <div className="flex items-end justify-between">
                <div className="text-3xl font-bold text-white">{stat.value}</div>
                <div className="text-sm font-medium text-emerald-400">{stat.trend}</div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Placeholder Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 h-80 flex flex-col">
          <h3 className="text-lg font-medium text-white mb-4">Model Invocations (24h)</h3>
          <div className="flex-1 flex items-center justify-center border border-dashed border-gray-700 rounded-lg text-gray-500">
            Chart coming in Phase 5
          </div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 h-80 flex flex-col">
          <h3 className="text-lg font-medium text-white mb-4">System Latency</h3>
          <div className="flex-1 flex items-center justify-center border border-dashed border-gray-700 rounded-lg text-gray-500">
            Chart coming in Phase 5
          </div>
        </div>
      </div>
    </div>
  )
}
