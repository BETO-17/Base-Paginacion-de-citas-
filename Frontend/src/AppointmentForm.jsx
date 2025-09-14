import { useState } from "react"

export default function AppointmentForm() {
  const [formData, setFormData] = useState({
    calendarId: "",
    contactId: "",
    locationId: "",
    startTime: "",
    endTime: "",
    title: "",
    assignedUserId: "",
  })

  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const [savedData, setSavedData] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target

    // Si es un campo de fecha/hora, lo convertimos a ISO con Z (UTC)
    if (name === "startTime" || name === "endTime") {
      const date = new Date(value)
      setFormData({ ...formData, [name]: date.toISOString() })
    } else {
      setFormData({ ...formData, [name]: value })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage("")
    setSavedData(null)

    try {
      const res = await fetch("http://localhost:8000/ghl/appointment/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!res.ok) throw new Error("Error al guardar la cita")

      const saved = await res.json()
      setMessage("✅ Cita guardada con éxito")
      setSavedData(saved)
      setFormData({
        calendarId: "",
        contactId: "",
        locationId: "",
        startTime: "",
        endTime: "",
        title: "",
        assignedUserId: "",
      })
    } catch (error) {
      console.error(error)
      setMessage("❌ Error al guardar la cita")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2 className="section-title">Crear Cita</h2>
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label>Calendar ID:</label>
          <input
            type="text"
            name="calendarId"
            value={formData.calendarId}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Contact ID:</label>
          <input
            type="text"
            name="contactId"
            value={formData.contactId}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Location ID:</label>
          <input
            type="text"
            name="locationId"
            value={formData.locationId}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Título:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Usuario asignado (ID):</label>
          <input
            type="text"
            name="assignedUserId"
            value={formData.assignedUserId}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Inicio:</label>
          <input
            type="datetime-local"
            name="startTime"
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Fin:</label>
          <input
            type="datetime-local"
            name="endTime"
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? "Guardando..." : "Guardar Cita"}
        </button>
      </form>

      {message && (
        <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      {savedData && (
        <pre className="response-box">
          {JSON.stringify(savedData, null, 2)}
        </pre>
      )}
    </div>
  )
}