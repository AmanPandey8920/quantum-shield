import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

const apiBase = 'http://127.0.0.1:8000';

function App() {
  const [devices, setDevices] = React.useState([]);
  const [events, setEvents] = React.useState([]);
  const [readings, setReadings] = React.useState([]);
  const [status, setStatus] = React.useState('Loading...');

  React.useEffect(() => {
    fetch(`${apiBase}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('Backend unavailable'));

    fetch(`${apiBase}/devices`)
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch(() => setDevices([]));

    fetch(`${apiBase}/monitoring/events`)
      .then((res) => res.json())
      .then((data) => setEvents(data))
      .catch(() => setEvents([]));
  }, []);

  return (
    <div className="app-shell">
      <header className="header">
        <div>
          <p className="eyebrow">IoT Cybersecurity Prototype</p>
          <h1>QuantumShield</h1>
        </div>
        <div className="status-pill">{status}</div>
      </header>

      <section className="panel-grid">
        <div className="panel">
          <h2>Registered devices</h2>
          <ul>
            {devices.length ? devices.map((device) => (
              <li key={device.device_id}>
                <strong>{device.device_id}</strong> — {device.name} ({device.is_active ? 'active' : 'inactive'})
              </li>
            )) : <li>No devices registered yet.</li>}
          </ul>
        </div>

        <div className="panel">
          <h2>Security events</h2>
          <ul>
            {events.length ? events.map((event, index) => (
              <li key={`${event.event_type}-${index}`}>
                <strong>{event.event_type}</strong> — {event.device_id || 'system'}
                <div>{event.details}</div>
              </li>
            )) : <li>No events recorded yet.</li>}
          </ul>
        </div>
      </section>

      <section className="panel">
        <h2>Prototype notes</h2>
        <p>
          This dashboard is a live demonstration of readings, device state, and event monitoring for the
          QuantumShield educational prototype.
        </p>
        <p>
          Use the backend API to register devices and ingest sensor telemetry for a more complete demo.
        </p>
      </section>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
