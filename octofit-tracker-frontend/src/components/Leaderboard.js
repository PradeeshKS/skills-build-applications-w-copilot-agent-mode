import React, { useEffect, useState } from 'react';

const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboards/`;

function Leaderboard() {
  const [leaderboards, setLeaderboards] = useState([]);

  useEffect(() => {
    console.log('Fetching leaderboards from:', API_URL);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaderboards(results);
        console.log('Fetched leaderboards:', results);
      })
      .catch(err => console.error('Error fetching leaderboards:', err));
  }, []);

  return (
    <div className="card shadow mb-4">
      <div className="card-header bg-success text-white">
        <h2 className="h4 mb-0">Leaderboard</h2>
      </div>
      <div className="card-body">
        <table className="table table-striped table-bordered">
          <thead className="table-light">
            <tr>
              <th scope="col">Team</th>
              <th scope="col">Points</th>
              <th scope="col">Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {leaderboards.map((entry, idx) => (
              <tr key={entry.id || idx}>
                <td>{entry.team?.name || 'Team'}</td>
                <td>{entry.points}</td>
                <td>{entry.last_updated ? new Date(entry.last_updated).toLocaleString() : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button className="btn btn-success mt-2" onClick={() => window.location.reload()}>Refresh</button>
      </div>
    </div>
  );
}

export default Leaderboard;
