import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import PrivateRoute from './components/PrivateRoute/PrivateRoute.jsx'
import Login from './components/Login/Login.jsx'
import Registro from './components/Registro/Registro.jsx'
import DashCliente from './pages/DashboardCliente/DashCliente.jsx'
import DashMecanico from './pages/DashboardMecanico/DashMecanico.jsx'
import DashGerente from './pages/DashboardGerente/DashGerente.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rotas públicas */}
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        
        {/* Rotas protegidas */}
        <Route 
          path="/dashboard/cliente" 
          element={
            <PrivateRoute>
              <DashCliente />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/dashboard/mecanico" 
          element={
            <PrivateRoute>
              <DashMecanico />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/dashboard/gerente" 
          element={
            <PrivateRoute>
              <DashGerente />
            </PrivateRoute>
          } 
        />
        
        {/* Rota padrão */}
        <Route path="/" element={<Navigate to="/registro" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
