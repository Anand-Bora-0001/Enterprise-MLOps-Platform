import React, { useState, useEffect } from "react"
import { Button } from "../components/ui/button"
import { Server, Activity, ShieldCheck, Box } from "lucide-react"
import api from "../services/api"

export default function Registry() {
  const [models, setModels] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    try {
      const response = await api.get("/registry/models")
      setModels(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusClass = (status: str) => {
    switch (status) {
      case "approved": return "text-emerald-400 bg-emerald-400/10"
      case "rejected": return "text-red-400 bg-red-400/10"
      case "staged": return "text-blue-400 bg-blue-400/10"
      default: return "text-gray-400 bg-gray-400/10"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Box className="h-6 w-6 text-blue-500" />
            Model Registry
          </h2>
          <p className="text-gray-400 mt-1">Manage, approve, and deploy registered machine learning models.</p>
        </div>
      </div>

      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading models...</div>
      ) : models.length === 0 ? (
        <div className="text-center py-16 bg-gray-900/50 border border-dashed border-gray-800 rounded-xl">
          <Box className="h-12 w-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-white mb-2">No registered models found</h3>
          <p className="text-gray-400 mb-6">Register a model from the experiments dashboard to deploy it.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {models.map((mod) => (
            <div key={mod.id} className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-sm flex flex-col hover:border-gray-700 transition-colors">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-white truncate max-w-[200px]" title={mod.name}>
                    {mod.name}
                  </h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs font-mono text-gray-500">v{mod.version}</span>
                    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${getStatusClass(mod.status)}`}>
                      {mod.status}
                    </span>
                  </div>
                </div>
                <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
                  <ShieldCheck className="h-5 w-5" />
                </div>
              </div>
              <div className="text-sm text-gray-400 space-y-2 mb-6 flex-1">
                <div className="flex justify-between">
                  <span>Experiment ID:</span>
                  <span className="text-gray-300">#{mod.experiment_id}</span>
                </div>
                <div className="flex justify-between">
                  <span>Registered on:</span>
                  <span className="text-gray-300">{new Date(mod.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 pt-4 border-t border-gray-800">
                <Button variant="outline" className="w-full">
                  Details
                </Button>
                <Button className="w-full flex items-center justify-center gap-2">
                  <Server className="h-4 w-4" />
                  Deploy
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
