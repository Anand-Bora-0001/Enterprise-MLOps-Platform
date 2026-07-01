import React, { useState, useEffect } from "react"
import { Button } from "../components/ui/button"
import { Database, UploadCloud, File as FileIcon, Search } from "lucide-react"
import { Input } from "../components/ui/input"
import api from "../services/api"

export default function Datasets() {
  const [datasets, setDatasets] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    try {
      const response = await api.get("/datasets/")
      setDatasets(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Database className="h-6 w-6 text-blue-500" />
            Dataset Management
          </h2>
          <p className="text-gray-400 mt-1">Upload and manage your training and evaluation datasets.</p>
        </div>
        <Button className="flex items-center gap-2">
          <UploadCloud className="h-4 w-4" />
          Upload Dataset
        </Button>
      </div>

      {/* Toolbar */}
      <div className="flex items-center gap-4 bg-gray-900 border border-gray-800 p-4 rounded-xl">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
          <Input placeholder="Search datasets..." className="pl-9" />
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400 ml-auto">
          <span>Sort by:</span>
          <select className="bg-gray-800 border-none rounded text-white text-sm focus:ring-0">
            <option>Newest first</option>
            <option>Size (largest)</option>
            <option>Name (A-Z)</option>
          </select>
        </div>
      </div>

      {/* Dataset Grid */}
      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading datasets...</div>
      ) : datasets.length === 0 ? (
        <div className="text-center py-16 bg-gray-900/50 border border-dashed border-gray-800 rounded-xl">
          <Database className="h-12 w-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-white mb-2">No datasets found</h3>
          <p className="text-gray-400 mb-6">You haven't uploaded any datasets to this project yet.</p>
          <Button variant="outline" className="flex items-center gap-2 mx-auto">
            <UploadCloud className="h-4 w-4" />
            Upload your first dataset
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {datasets.map((ds) => (
            <div key={ds.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors group cursor-pointer">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
                    <FileIcon className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="font-medium text-white group-hover:text-blue-400 transition-colors truncate max-w-[150px]" title={ds.name}>
                      {ds.name}
                    </h3>
                    <p className="text-xs text-gray-500 uppercase">{ds.format}</p>
                  </div>
                </div>
              </div>
              {ds.description && (
                <p className="text-sm text-gray-400 line-clamp-2 mb-4">
                  {ds.description}
                </p>
              )}
              <div className="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-4 mt-auto">
                <span>{(ds.file_size_bytes / (1024 * 1024)).toFixed(2)} MB</span>
                <span>{new Date(ds.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
