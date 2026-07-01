import React from "react"
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { DashboardLayout } from "./layouts/DashboardLayout"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Datasets from "./pages/Datasets"
import Experiments from "./pages/Experiments"
import Registry from "./pages/Registry"

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem("token")
  return token ? <>{children}</> : <Navigate to="/login" />
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route
          path="/"
          element={
            <PrivateRoute>
              <DashboardLayout />
            </PrivateRoute>
          }
        >
          <Route index element={<Dashboard />} />
          {/* We will add more routes in future phases */}
          <Route path="datasets" element={<Datasets />} />
          <Route path="experiments" element={<Experiments />} />
          <Route path="registry" element={<Registry />} />
          <Route path="settings" element={<div className="text-white">Settings Page</div>} />
        </Route>
      </Routes>
    </Router>
  )
}
