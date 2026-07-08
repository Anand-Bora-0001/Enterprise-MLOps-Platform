import { useState, useEffect } from "react"
import { Button } from "../components/ui/button"
import { Activity, Play, BarChart3, CheckCircle2, XCircle, Clock } from "lucide-react"
import api from "../services/api"

export default function Experiments() {
  const [experiments, setExperiments] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchExperiments()
  }, [])

  const fetchExperiments = async () => {
    try {
      const response = await api.get("/experiments/")
      setExperiments(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return <CheckCircle2 className="h-4 w-4 text-emerald-400" />
      case "failed": return <XCircle className="h-4 w-4 text-red-400" />
      case "running": return <Activity className="h-4 w-4 text-blue-400 animate-pulse" />
      default: return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusClass = (status: string) => {
    switch (status) {
      case "completed": return "text-emerald-400 bg-emerald-400/10"
      case "failed": return "text-red-400 bg-red-400/10"
      case "running": return "text-blue-400 bg-blue-400/10"
      default: return "text-gray-400 bg-gray-400/10"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Activity className="h-6 w-6 text-blue-500" />
            Experiments & Training
          </h2>
          <p className="text-gray-400 mt-1">Train models asynchronously and track their performance via MLflow.</p>
        </div>
        <Button className="flex items-center gap-2">
          <Play className="h-4 w-4" />
          New Experiment
        </Button>
      </div>

      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading experiments...</div>
      ) : experiments.length === 0 ? (
        <div className="text-center py-16 bg-gray-900/50 border border-dashed border-gray-800 rounded-xl">
          <BarChart3 className="h-12 w-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-white mb-2">No experiments found</h3>
          <p className="text-gray-400 mb-6">You haven't run any model training experiments yet.</p>
          <Button variant="outline" className="flex items-center gap-2 mx-auto">
            <Play className="h-4 w-4" />
            Start your first experiment
          </Button>
        </div>
      ) : (
        <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-gray-800/50 text-gray-300">
              <tr>
                <th className="px-6 py-4 font-medium">Experiment Name</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Model Type</th>
                <th className="px-6 py-4 font-medium">Metrics</th>
                <th className="px-6 py-4 font-medium">Run ID (MLflow)</th>
                <th className="px-6 py-4 font-medium">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {experiments.map((exp) => (
                <tr key={exp.id} className="hover:bg-gray-800/30 transition-colors">
                  <td className="px-6 py-4 font-medium text-white">{exp.name}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${getStatusClass(exp.status)}`}>
                      {getStatusIcon(exp.status)}
                      {exp.status.charAt(0).toUpperCase() + exp.status.slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4">{exp.model_type}</td>
                  <td className="px-6 py-4">
                    {exp.metrics ? (
                      <span className="text-emerald-400 font-mono">
                        {JSON.parse(exp.metrics).accuracy?.toFixed(4) || "-"}
                      </span>
                    ) : (
                      <span className="text-gray-500">-</span>
                    )}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs text-gray-500">
                    {exp.mlflow_run_id ? exp.mlflow_run_id.substring(0, 8) + '...' : '-'}
                  </td>
                  <td className="px-6 py-4">{new Date(exp.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
