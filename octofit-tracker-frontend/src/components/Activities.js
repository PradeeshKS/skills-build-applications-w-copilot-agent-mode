import React, { useEffect, useState } from 'react';

const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

function Activities() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    console.log('Fetching activities from:', API_URL);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, []);

  return (
    <div className="card shadow mb-4">
      <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h2 className="h4 mb-0">Activities</h2>
        <button className="btn btn-light btn-sm" onClick={() => window.location.reload()}><i className="bi bi-arrow-clockwise"></i> Refresh</button>
      </div>
      <div className="card-body">
        <table className="table table-striped table-bordered align-middle">
          <thead className="table-light">
            <tr>
              <th scope="col">Type</th>
              <th scope="col">Duration (min)</th>
              <th scope="col">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity, idx) => (
              <tr key={activity.id || idx}>
                <td>{activity.type}</td>
                <td>{activity.duration}</td>
                <td>{activity.timestamp ? new Date(activity.timestamp).toLocaleString() : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activities;
