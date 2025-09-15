import { useEffect, useState } from 'react'
import LoadingBar from "./LoadingBar"

function AppointmentsTable() {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const itemsPerPage = 5

  useEffect(() => {
    async function fetchAppointments() {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:8000/api/ghl-appointments/')
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()
        // Extraer la propiedad "appointment" de cada elemento
        const list = data.map(item => item.appointment)
        setAppointments(list)
        
        // Calcular el número total de páginas
        const total = Math.ceil(list.length / itemsPerPage)
        setTotalPages(total)
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

  // Función para obtener las citas de la página actual
  const getCurrentPageAppointments = () => {
    const startIndex = (currentPage - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    return appointments.slice(startIndex, endIndex)
  }

  // Función para ir a la página anterior
  const goToPreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  // Función para ir a la página siguiente
  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1)
    }
  }

  return (
    <div className="apt-wrapper">
      <h2 className="apt-title">Lista de Citas</h2>

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
                  getCurrentPageAppointments().map((apt, idx) => {
                    const globalIndex = (currentPage - 1) * itemsPerPage + idx
                    return (
                      <tr key={apt.id || globalIndex}>
                        <td>{globalIndex + 1}</td>
                        <td className="apt-title-cell">{apt.title || '—'}</td>
                        <td className="apt-datetime">{formatDateTime(apt.startTime)}</td>
                        <td className="apt-datetime">{formatDateTime(apt.endTime)}</td>
                        <td>{getStatusBadge(apt.appointmentStatus)}</td>
                        <td className="mono">{apt.contactId || '—'}</td>
                        <td className="mono">{apt.calendarId || '—'}</td>
                      </tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>

          {appointments.length > 0 && (
            <div className="apt-summary">
              <p>Total: <strong>{appointments.length}</strong> citas</p>
              <p>Página <strong>{currentPage}</strong> de <strong>{totalPages}</strong></p>
            </div>
          )}

          {/* Controles de paginación */}
          {appointments.length > 0 && totalPages > 1 && (
            <div className="pagination-controls">
              <button 
                onClick={goToPreviousPage} 
                disabled={currentPage === 1}
                className="pagination-btn prev-btn"
              >
                ← Anterior
              </button>
              
              <span className="pagination-info">
                Página {currentPage} de {totalPages}
              </span>
              
              <button 
                onClick={goToNextPage} 
                disabled={currentPage === totalPages}
                className="pagination-btn next-btn"
              >
                Siguiente →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default AppointmentsTable