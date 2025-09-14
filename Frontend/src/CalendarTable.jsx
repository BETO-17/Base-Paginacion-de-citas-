import { useEffect, useState } from "react"
import LoadingBar from "./LoadingBar" 

function CalendarTable() {
  const [calendars, setCalendars] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchCalendars() {
      try {
        setLoading(true) 
        const response = await fetch("http://localhost:8000/calendars/")
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()
        const list = Array.isArray(data) ? data : data.calendars || []
        setCalendars(list)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false) 
      }
    }

    fetchCalendars()
  }, [])

  return (
    <div className="cal-wrapper">
      <h2 className="cal-title">Calendarios</h2>

      {loading && <LoadingBar />}

      {loading ? (
        <div className="cal-loading">Cargando calendarios…</div>
      ) : error ? (
        <div className="cal-error">Error: {error}</div>
      ) : (
        <div className="cal-table-container">
          <table className="cal-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>ID</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {calendars.length === 0 ? (
                <tr>
                  <td colSpan={4} className="cal-empty">
                    Sin calendarios
                  </td>
                </tr>
              ) : (
                calendars.map((cal, idx) => (
                  <tr key={cal.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{cal.name || cal.title || "—"}</td>
                    <td className="mono">{cal.id || "—"}</td>
                    <td>
                      <span
                        className={`badge ${cal.active ? "ok" : "off"}`}
                      >
                        {cal.active ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default CalendarTable
