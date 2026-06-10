import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { get } from '../lib/api';
import StatusBadge from '../components/StatusBadge';

const STATUSES = ['draft', 'in_review', 'published', 'scheduled', 'rejected', 'archived'];

export default function Dashboard() {
  const [counts, setCounts] = useState({});
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function load() {
      try {
        // Fetch counts for each status
        const countMap = {};
        let total = 0;
        for (const s of STATUSES) {
          const res = await get('/admin/articles', { status: s, limit: 1, page: 1 });
          countMap[s] = res.total;
          total += res.total;
        }
        countMap.total = total;
        setCounts(countMap);

        // Fetch recent articles
        const recentRes = await get('/admin/articles', { limit: 8, page: 1 });
        setRecent(recentRes.items);
      } catch (err) {
        console.error('Dashboard load error:', err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="loading">Loading dashboard…</div>;

  const cards = [
    { label: 'Total', value: counts.total || 0, status: null, color: '#6366f1' },
    { label: 'Published', value: counts.published || 0, status: 'published', color: '#10b981' },
    { label: 'Drafts', value: counts.draft || 0, status: 'draft', color: '#8b8b8b' },
    { label: 'In Review', value: counts.in_review || 0, status: 'in_review', color: '#f59e0b' },
    { label: 'Scheduled', value: counts.scheduled || 0, status: 'scheduled', color: '#3b82f6' },
    { label: 'Rejected', value: counts.rejected || 0, status: 'rejected', color: '#ef4444' },
  ];

  return (
    <div className="dashboard">
      <div className="stat-cards">
        {cards.map((c) => (
          <div
            key={c.label}
            className="stat-card"
            style={{ borderTopColor: c.color }}
            onClick={() => c.status && navigate(`/articles?status=${c.status}`)}
          >
            <div className="stat-card-value">{c.value}</div>
            <div className="stat-card-label">{c.label}</div>
          </div>
        ))}
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2 className="section-title">Recent Articles</h2>
          <button className="btn btn--secondary btn--sm" onClick={() => navigate('/articles')}>
            View all →
          </button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Category</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {recent.map((a) => (
              <tr key={a.id} className="data-table-row" onClick={() => navigate(`/articles/${a.id}`)}>
                <td className="data-table-title">{a.title}</td>
                <td><StatusBadge status={a.status} /></td>
                <td>{a.category?.name || '—'}</td>
                <td className="data-table-date">
                  {a.published_at
                    ? new Date(a.published_at).toLocaleDateString()
                    : new Date(a.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
            {recent.length === 0 && (
              <tr><td colSpan={4} className="data-table-empty">No articles yet</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
