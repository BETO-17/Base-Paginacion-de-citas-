import { useState } from "react"
import CalendarTable from "./CalendarTable"
import AppointmentForm from "./AppointmentForm"
import AppointmentsTable from "./AppointmentsTable"

export default function App() {
  const [currentView, setCurrentView] = useState("calendars") // "calendars", "appointments", "view-appointments"

  const showCalendars = () => setCurrentView("calendars")
  const showCreateAppointments = () => setCurrentView("appointments")
  const showViewAppointments = () => setCurrentView("view-appointments")

  return (
    <div className="app">
      <h1 className="main-title">Gestión de Citas</h1>
      
      {/* Navegación */}
      <div className="nav-buttons">
        <button 
          className={`nav-button ${currentView === "calendars" ? "active" : ""}`}
          onClick={showCalendars}
        >
          📅 Ver Calendarios
        </button>
        <button 
          className={`nav-button ${currentView === "appointments" ? "active" : ""}`}
          onClick={showCreateAppointments}
        >
          ➕ Crear Cita
        </button>
        <button 
          className={`nav-button ${currentView === "view-appointments" ? "active" : ""}`}
          onClick={showViewAppointments}
        >
          👀 Ver Citas
        </button>
      </div>

      {/* Contenido basado en la vista actual */}
      {currentView === "calendars" && <CalendarTable />}
      {currentView === "appointments" && <AppointmentForm />}
      {currentView === "view-appointments" && <AppointmentsTable />}
    </div>
  )
}