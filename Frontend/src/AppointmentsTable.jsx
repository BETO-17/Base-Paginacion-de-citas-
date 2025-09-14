import { useEffect, useState } from 'react'
import LoadingBar from "./LoadingBar"

function AppointmentsTable() {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchAppointments() {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:8000/ghl/appointments/')
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()
        // Algunas respuestas vienen en { appointments: [...] } y otras como array directo
        const list = Array.isArray(data) ? data : (data.appointments || [])
        setAppointments(list)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchAppointments()
  }, [])

  const formatDateTime = (dateString) => {
    if (!dateString) return '—'
    try {
      const date = new Date(dateString)
      return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return dateString
    }
  }

  const getStatusBadge = (status) => {
    const statusMap = {
      'confirmed': { class: 'confirmed', text: 'Confirmada' },
      'pending': { class: 'pending', text: 'Pendiente' },
      'cancelled': { class: 'cancelled', text: 'Cancelada' },
      'completed': { class: 'completed', text: 'Completada' }
    }
    
    const statusInfo = statusMap[status?.toLowerCase()] || { class: 'unknown', text: status || 'Sin estado' }
    
    return (
      <span className={`badge ${statusInfo.class}`}>
        {statusInfo.text}
      </span>
    )
  }

  return (
    <div className="apt-wrapper">
      <h2 className="apt-title">Lista de Citas</h2>

      {/* Mostrar la barrita si está cargando */}
      {loading && <LoadingBar />}

      {loading ? (
        <div className="apt-loading">Cargando citas…</div>
      ) : error ? (
        <div className="apt-error">Error: {error}</div>
      ) : (
        <>
          <div className="apt-table-container">
            <table className="apt-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Título</th>
                  <th>Fecha Inicio</th>
                  <th>Fecha Fin</th>
                  <th>Estado</th>
                  <th>Contact ID</th>
                  <th>Calendar ID</th>
                </tr>
              </thead>
              <tbody>
                {appointments.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="apt-empty">No hay citas registradas</td>
                  </tr>
                ) : (
                  appointments.map((apt, idx) => (
                    <tr key={apt.id || idx}>
                      <td>{idx + 1}</td>
                      <td className="apt-title-cell">{apt.title || '—'}</td>
                      <td className="apt-datetime">{formatDateTime(apt.startTime)}</td>
                      <td className="apt-datetime">{formatDateTime(apt.endTime)}</td>
                      <td>{getStatusBadge(apt.status)}</td>
                      <td className="mono">{apt.contactId || '—'}</td>
                      <td className="mono">{apt.calendarId || '—'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          
          {appointments.length > 0 && (
            <div className="apt-summary">
              <p>Total: <strong>{appointments.length}</strong> citas</p>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default AppointmentsTable