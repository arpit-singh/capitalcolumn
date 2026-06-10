import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { get } from '../lib/api';
import StatusBadge from '../components/StatusBadge';
import Pagination from '../components/Pagination';

const STATUS_OPTIONS = [
  { value: '', label: 'All Statuses' },
  { value: 'draft', label: 'Draft' },
  { value: 'in_review', label: 'In Review' },
  { value: 'published', label: 'Published' },
  { value: 'scheduled', label: 'Scheduled' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'archived', label: 'Archived' },
];

export default function ArticleList() {
  const [articles, setArticles] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const page = parseInt(searchParams.get('page') || '1');
  const status = searchParams.get('status') || '';
  const search = searchParams.get('search') || '';

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await get('/admin/articles', { page, limit: 20, status, search });
        setArticles(res.items);
        setTotal(res.total);
        setTotalPages(res.total_pages);
      } catch (err) {
        console.error('Articles load error:', err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [page, status, search]);

  function updateFilter(key, value) {
    const params = new URLSearchParams(searchParams);
    if (value) params.set(key, value);
    else params.delete(key);
    params.set('page', '1');
    setSearchParams(params);
  }

  return (
    <div className="article-list">
      <div className="list-toolbar">
        <div className="list-filters">
          <select
            className="form-select"
            value={status}
            onChange={(e) => updateFilter('status', e.target.value)}
          >
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
          <input
            className="form-input"
            type="text"
            placeholder="Search articles…"
            value={search}
            onChange={(e) => updateFilter('search', e.target.value)}
          />
        </div>
        <div className="list-meta">{total} article{total !== 1 ? 's' : ''}</div>
      </div>

      {loading ? (
        <div className="loading">Loading articles…</div>
      ) : (
        <>
          <table className="data-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Type</th>
                <th>Category</th>
                <th>AI</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {articles.map((a) => (
                <tr key={a.id} className="data-table-row" onClick={() => navigate(`/articles/${a.id}`)}>
                  <td className="data-table-title">
                    {a.title}
                    {a.dek && <span className="data-table-dek">{a.dek}</span>}
                  </td>
                  <td><StatusBadge status={a.status} /></td>
                  <td className="data-table-type">{a.article_type}</td>
                  <td>{a.category?.name || '—'}</td>
                  <td>
                    {a.is_editor_reviewed
                      ? <span className="badge badge--green">Reviewed</span>
                      : a.is_ai_generated
                        ? <span className="badge badge--yellow">AI</span>
                        : '—'}
                  </td>
                  <td className="data-table-date">
                    {a.published_at
                      ? new Date(a.published_at).toLocaleDateString()
                      : new Date(a.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
              {articles.length === 0 && (
                <tr><td colSpan={6} className="data-table-empty">No articles found</td></tr>
              )}
            </tbody>
          </table>
          <Pagination
            page={page}
            totalPages={totalPages}
            onPageChange={(p) => updateFilter('page', String(p))}
          />
        </>
      )}
    </div>
  );
}
