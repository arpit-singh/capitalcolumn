import { useState, useEffect, useCallback } from 'react';
import { get, post, patch } from '../lib/api';

const STATUS_COLORS = {
  pending: { bg: '#fef3c7', color: '#92400e' },
  approved: { bg: '#dbeafe', color: '#1e40af' },
  processing: { bg: '#ede9fe', color: '#5b21b6' },
  completed: { bg: '#d1fae5', color: '#065f46' },
  rejected: { bg: '#fee2e2', color: '#991b1b' },
  error: { bg: '#fee2e2', color: '#991b1b' },
};

function StatusBadge({ status }) {
  const s = STATUS_COLORS[status] || { bg: '#f1f1f4', color: '#6c6c80' };
  return (
    <span style={{
      display: 'inline-block', padding: '3px 10px', borderRadius: '20px',
      fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase',
      letterSpacing: '0.03em', background: s.bg, color: s.color,
    }}>
      {status}
    </span>
  );
}

export default function Pipeline() {
  const [tab, setTab] = useState('topics');
  const [topics, setTopics] = useState([]);
  const [stats, setStats] = useState({});
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [selected, setSelected] = useState(new Set());
  const [statusFilter, setStatusFilter] = useState('');
  const [toast, setToast] = useState('');
  const [showGenDialog, setShowGenDialog] = useState(false);
  const [showAddTopic, setShowAddTopic] = useState(false);
  const [showAddSource, setShowAddSource] = useState(false);

  // Generation options
  const [genProvider, setGenProvider] = useState('openai');
  const [genModel, setGenModel] = useState('gpt-4o');
  const [genImageModel, setGenImageModel] = useState('prunaai/z-image-turbo');
  const [genWordCount, setGenWordCount] = useState(1200);
  const [genSkipImage, setGenSkipImage] = useState(false);

  // Add topic form
  const [newTitle, setNewTitle] = useState('');
  const [newCategory, setNewCategory] = useState('markets');
  const [newUrl, setNewUrl] = useState('');

  // Add source form
  const [sourceName, setSourceName] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [sourceCategory, setSourceCategory] = useState('markets');
  const [sourceType, setSourceType] = useState('rss');

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  };

  const loadData = useCallback(async () => {
    try {
      const [topicsRes, statsRes, configRes] = await Promise.all([
        get('/admin/pipeline/topics', { status: statusFilter || undefined }),
        get('/admin/pipeline/stats'),
        get('/admin/pipeline/config'),
      ]);
      setTopics(topicsRes.topics || []);
      setStats(statsRes);
      setConfig(configRes);
      if (configRes?.defaults) {
        setGenProvider(configRes.defaults.llm_provider || 'openai');
        setGenModel(configRes.defaults.llm_model || 'gpt-4o');
        setGenImageModel(configRes.defaults.image_model || 'prunaai/z-image-turbo');
        setGenWordCount(configRes.defaults.word_count || 1200);
      }
    } catch (err) {
      console.error('Pipeline load error:', err);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleScan = async () => {
    setScanning(true);
    try {
      const res = await post('/admin/pipeline/scan');
      showToast(`Found ${res.new_topics} new topic(s)`);
      setStats(res.stats);
      loadData();
    } catch (err) {
      showToast(`Scan error: ${err.message}`);
    } finally {
      setScanning(false);
    }
  };

  const handleStatusUpdate = async (newStatus) => {
    if (selected.size === 0) return;
    try {
      const res = await patch('/admin/pipeline/topics/status', {
        topic_ids: [...selected],
        status: newStatus,
      });
      showToast(`${res.updated} topic(s) ${newStatus}`);
      setSelected(new Set());
      setStats(res.stats);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleGenerate = async () => {
    const approvedIds = [...selected].filter(id =>
      topics.find(t => t.id === id && t.status === 'approved')
    );
    if (approvedIds.length === 0) {
      showToast('Select approved topics first');
      return;
    }
    setGenerating(true);
    setShowGenDialog(false);
    try {
      const res = await post('/admin/pipeline/generate', {
        topic_ids: approvedIds,
        llm_provider: genProvider,
        llm_model: genModel,
        image_model: genImageModel,
        word_count: genWordCount,
        skip_image: genSkipImage,
      });
      showToast(res.message);
      setSelected(new Set());
      loadData();
    } catch (err) {
      showToast(`Generate error: ${err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleAddTopic = async () => {
    if (!newTitle.trim()) return;
    try {
      const res = await post('/admin/pipeline/topics', {
        title: newTitle, category: newCategory, url: newUrl,
      });
      showToast('Topic added');
      setNewTitle(''); setNewUrl('');
      setShowAddTopic(false);
      setStats(res.stats);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleAddSource = async () => {
    if (!sourceName.trim() || !sourceUrl.trim()) return;
    try {
      await post('/admin/pipeline/sources', {
        name: sourceName, url: sourceUrl, category: sourceCategory, source_type: sourceType,
      });
      showToast('Source added');
      setSourceName(''); setSourceUrl('');
      setShowAddSource(false);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleClear = async (status) => {
    if (!window.confirm(`Clear all ${status || ''} topics?`)) return;
    try {
      const res = await post(`/admin/pipeline/topics/clear${status ? `?status=${status}` : ''}`);
      showToast(`Cleared ${res.cleared} topic(s)`);
      setStats(res.stats);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const toggleSelect = (id) => {
    setSelected(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selected.size === topics.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(topics.map(t => t.id)));
    }
  };

  if (loading) return <div className="loading">Loading pipeline…</div>;

  const approvedSelected = [...selected].filter(id =>
    topics.find(t => t.id === id && t.status === 'approved')
  ).length;

  const currentModels = config?.llm_providers?.find(p => p.id === genProvider)?.models || [];

  return (
    <div className="pipeline-page">
      {toast && <div className="toast">{toast}</div>}

      {/* Stats Cards */}
      <div className="stat-cards" style={{ marginBottom: 20 }}>
        {[
          { label: 'Total', value: stats.total || 0, color: '#6366f1' },
          { label: 'Pending', value: stats.pending || 0, color: '#f59e0b', filter: 'pending' },
          { label: 'Approved', value: stats.approved || 0, color: '#3b82f6', filter: 'approved' },
          { label: 'Processing', value: stats.processing || 0, color: '#8b5cf6', filter: 'processing' },
          { label: 'Completed', value: stats.completed || 0, color: '#10b981', filter: 'completed' },
          { label: 'Errors', value: stats.error || 0, color: '#ef4444', filter: 'error' },
        ].map(c => (
          <div key={c.label} className="stat-card" style={{ borderTopColor: c.color }}
            onClick={() => { setStatusFilter(c.filter || ''); setSelected(new Set()); }}>
            <div className="stat-card-value">{c.value}</div>
            <div className="stat-card-label">{c.label}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="pipeline-tabs">
        {['topics', 'sources', 'settings'].map(t => (
          <button key={t} className={`pipeline-tab ${tab === t ? 'pipeline-tab--active' : ''}`}
            onClick={() => setTab(t)}>
            {t === 'topics' ? '📋 Topics' : t === 'sources' ? '📡 Sources' : '⚙️ Settings'}
          </button>
        ))}
      </div>

      {/* ---- Topics Tab ---- */}
      {tab === 'topics' && (
        <div className="pipeline-section">
          {/* Toolbar */}
          <div className="pipeline-toolbar">
            <div className="pipeline-toolbar-left">
              <button className="btn btn--primary" onClick={handleScan} disabled={scanning}>
                {scanning ? '⏳ Scanning...' : '📡 Scan Sources'}
              </button>
              <button className="btn btn--secondary" onClick={() => setShowAddTopic(true)}>
                + Add Topic
              </button>
              <select className="form-select form-input--sm" value={statusFilter}
                onChange={e => { setStatusFilter(e.target.value); setSelected(new Set()); }}>
                <option value="">All statuses</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="processing">Processing</option>
                <option value="completed">Completed</option>
                <option value="rejected">Rejected</option>
                <option value="error">Error</option>
              </select>
            </div>
            <div className="pipeline-toolbar-right">
              {selected.size > 0 && (
                <>
                  <span className="pipeline-selected-count">{selected.size} selected</span>
                  <button className="btn btn--success btn--sm" onClick={() => handleStatusUpdate('approved')}>
                    ✓ Approve
                  </button>
                  <button className="btn btn--danger btn--sm" onClick={() => handleStatusUpdate('rejected')}>
                    ✗ Reject
                  </button>
                  {approvedSelected > 0 && (
                    <button className="btn btn--primary btn--sm"
                      onClick={() => setShowGenDialog(true)} disabled={generating}>
                      {generating ? '⏳ Generating...' : `🚀 Generate (${approvedSelected})`}
                    </button>
                  )}
                </>
              )}
              {stats.completed > 0 && (
                <button className="btn btn--ghost btn--sm" onClick={() => handleClear('completed')}>
                  Clear completed
                </button>
              )}
            </div>
          </div>

          {/* Topics Table */}
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: 40 }}>
                  <input type="checkbox" checked={topics.length > 0 && selected.size === topics.length}
                    onChange={toggleSelectAll} />
                </th>
                <th>Title</th>
                <th>Source</th>
                <th>Category</th>
                <th>Keywords</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {topics.map(t => (
                <tr key={t.id} className="data-table-row"
                  onClick={() => toggleSelect(t.id)}
                  style={selected.has(t.id) ? { background: '#f0f0ff' } : {}}>
                  <td onClick={e => e.stopPropagation()}>
                    <input type="checkbox" checked={selected.has(t.id)}
                      onChange={() => toggleSelect(t.id)} />
                  </td>
                  <td className="data-table-title">
                    {t.title}
                    {t.error && <span className="pipeline-error-hint" title={t.error}>⚠️</span>}
                    {t.article_slug && (
                      <span className="data-table-dek">→ {t.article_slug}</span>
                    )}
                  </td>
                  <td style={{ fontSize: '0.82rem' }}>{t.source_name}</td>
                  <td style={{ fontSize: '0.82rem', textTransform: 'capitalize' }}>{t.category}</td>
                  <td style={{ fontSize: '0.78rem', color: '#6c6c80', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {(t.seo?.primary_keywords || []).slice(0, 2).join(', ')}
                  </td>
                  <td><StatusBadge status={t.status} /></td>
                  <td className="data-table-date">
                    {new Date(t.discovered_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
              {topics.length === 0 && (
                <tr><td colSpan={7} className="data-table-empty">
                  {statusFilter ? `No ${statusFilter} topics` : 'No topics yet — click "Scan Sources" to discover news'}
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* ---- Sources Tab ---- */}
      {tab === 'sources' && (
        <div className="pipeline-section">
          <div className="pipeline-toolbar">
            <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>RSS Feeds & Sitemaps</h3>
            <button className="btn btn--primary btn--sm" onClick={() => setShowAddSource(true)}>
              + Add Source
            </button>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>URL</th>
                <th>Category</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {(config?.sources?.rss_feeds || []).map((s, i) => (
                <tr key={`rss-${i}`}>
                  <td>{i + 1}</td>
                  <td style={{ fontWeight: 500 }}>{s.name}</td>
                  <td style={{ fontSize: '0.78rem', color: '#6366f1', maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    <a href={s.url} target="_blank" rel="noopener">{s.url}</a>
                  </td>
                  <td style={{ textTransform: 'capitalize' }}>{s.category}</td>
                  <td><span className="badge badge--green">RSS</span></td>
                </tr>
              ))}
              {(config?.sources?.sitemaps || []).map((s, i) => (
                <tr key={`sm-${i}`}>
                  <td>{(config?.sources?.rss_feeds?.length || 0) + i + 1}</td>
                  <td style={{ fontWeight: 500 }}>{s.name}</td>
                  <td style={{ fontSize: '0.78rem', color: '#6366f1' }}>
                    <a href={s.url} target="_blank" rel="noopener">{s.url}</a>
                  </td>
                  <td style={{ textTransform: 'capitalize' }}>{s.category}</td>
                  <td><span className="badge badge--yellow">Sitemap</span></td>
                </tr>
              ))}
              {(!config?.sources?.rss_feeds?.length && !config?.sources?.sitemaps?.length) && (
                <tr><td colSpan={5} className="data-table-empty">No sources configured</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* ---- Settings Tab ---- */}
      {tab === 'settings' && (
        <div className="pipeline-section">
          <div className="pipeline-settings-grid">
            <div className="sidebar-section">
              <div className="sidebar-section-title">LLM Providers</div>
              {config?.llm_providers?.map(p => (
                <div key={p.id} style={{ marginBottom: 12 }}>
                  <div style={{ fontWeight: 600, fontSize: '0.88rem', display: 'flex', alignItems: 'center', gap: 8 }}>
                    {p.name}
                    {p.configured
                      ? <span className="badge badge--green">Configured</span>
                      : <span style={{ fontSize: '0.75rem', color: '#ef4444' }}>Not configured</span>
                    }
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#6c6c80', marginTop: 2 }}>
                    Models: {p.models.map(m => m.name).join(', ')}
                  </div>
                </div>
              ))}
            </div>

            <div className="sidebar-section">
              <div className="sidebar-section-title">Image Models</div>
              {config?.image_models?.map(m => (
                <div key={m.id} style={{ marginBottom: 8 }}>
                  <div style={{ fontWeight: 500, fontSize: '0.88rem' }}>
                    {m.name} {m.default && <span className="badge badge--green">Default</span>}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#6c6c80', fontFamily: 'monospace' }}>{m.id}</div>
                </div>
              ))}
              <div style={{ marginTop: 12, fontSize: '0.82rem' }}>
                Replicate: {config?.image_generation_configured
                  ? <span className="badge badge--green">Configured</span>
                  : <span style={{ color: '#ef4444' }}>Token not set</span>
                }
              </div>
            </div>

            <div className="sidebar-section">
              <div className="sidebar-section-title">Defaults</div>
              <dl className="meta-list">
                <dt>LLM Provider</dt><dd>{config?.defaults?.llm_provider}</dd>
                <dt>LLM Model</dt><dd>{config?.defaults?.llm_model}</dd>
                <dt>Image Model</dt><dd>{config?.defaults?.image_model}</dd>
                <dt>Word Count</dt><dd>{config?.defaults?.word_count}</dd>
              </dl>
            </div>
          </div>
        </div>
      )}

      {/* ---- Generate Dialog ---- */}
      {showGenDialog && (
        <div className="dialog-overlay" onClick={() => setShowGenDialog(false)}>
          <div className="dialog" style={{ width: 520 }} onClick={e => e.stopPropagation()}>
            <div className="dialog-title">🚀 Generate Articles</div>
            <div className="dialog-message">
              Generate {approvedSelected} article(s). This will use paid APIs.
              <br />
              <strong>Estimated cost: ~${(approvedSelected * 0.05).toFixed(2)}</strong>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
              <div className="form-group">
                <label className="form-label">LLM Provider</label>
                <select className="form-select" value={genProvider}
                  onChange={e => {
                    setGenProvider(e.target.value);
                    const models = config?.llm_providers?.find(p => p.id === e.target.value)?.models || [];
                    if (models.length) setGenModel(models[0].id);
                  }}>
                  {config?.llm_providers?.filter(p => p.configured).map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">LLM Model</label>
                <select className="form-select" value={genModel}
                  onChange={e => setGenModel(e.target.value)}>
                  {currentModels.map(m => (
                    <option key={m.id} value={m.id}>{m.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Image Model</label>
                <select className="form-select" value={genImageModel}
                  onChange={e => setGenImageModel(e.target.value)}>
                  {config?.image_models?.map(m => (
                    <option key={m.id} value={m.id}>{m.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Word Count</label>
                <input type="number" className="form-input" value={genWordCount}
                  onChange={e => setGenWordCount(parseInt(e.target.value) || 1200)}
                  min={500} max={5000} step={100} />
              </div>
            </div>

            <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.88rem', marginBottom: 16 }}>
              <input type="checkbox" checked={genSkipImage}
                onChange={e => setGenSkipImage(e.target.checked)} />
              Skip image generation (save ~$0.03/article)
            </label>

            <div className="dialog-actions">
              <button className="btn btn--secondary" onClick={() => setShowGenDialog(false)}>Cancel</button>
              <button className="btn btn--primary" onClick={handleGenerate}>
                🚀 Generate {approvedSelected} Article(s)
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ---- Add Topic Dialog ---- */}
      {showAddTopic && (
        <div className="dialog-overlay" onClick={() => setShowAddTopic(false)}>
          <div className="dialog" onClick={e => e.stopPropagation()}>
            <div className="dialog-title">Add Topic Manually</div>
            <div className="dialog-message">Add a news topic for article generation. SEO keywords will be researched automatically.</div>

            <div className="form-group" style={{ marginBottom: 12 }}>
              <label className="form-label">Topic Title *</label>
              <input className="form-input" value={newTitle} onChange={e => setNewTitle(e.target.value)}
                placeholder="e.g., Sensex hits all-time high of 80,000" />
            </div>
            <div className="form-row" style={{ marginBottom: 12 }}>
              <div className="form-group">
                <label className="form-label">Category</label>
                <select className="form-select" value={newCategory} onChange={e => setNewCategory(e.target.value)}>
                  {['markets','earnings','companies','technology','banking','energy','consumer','industrials','healthcare','global-markets','ipos','policy-regulation'].map(c => (
                    <option key={c} value={c}>{c.replace('-', ' ')}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Source URL (optional)</label>
                <input className="form-input" value={newUrl} onChange={e => setNewUrl(e.target.value)}
                  placeholder="https://..." />
              </div>
            </div>

            <div className="dialog-actions">
              <button className="btn btn--secondary" onClick={() => setShowAddTopic(false)}>Cancel</button>
              <button className="btn btn--primary" onClick={handleAddTopic} disabled={!newTitle.trim()}>
                Add Topic
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ---- Add Source Dialog ---- */}
      {showAddSource && (
        <div className="dialog-overlay" onClick={() => setShowAddSource(false)}>
          <div className="dialog" onClick={e => e.stopPropagation()}>
            <div className="dialog-title">Add News Source</div>

            <div className="form-group" style={{ marginBottom: 12 }}>
              <label className="form-label">Source Name *</label>
              <input className="form-input" value={sourceName} onChange={e => setSourceName(e.target.value)}
                placeholder="e.g., Economic Times - Markets" />
            </div>
            <div className="form-group" style={{ marginBottom: 12 }}>
              <label className="form-label">Feed URL *</label>
              <input className="form-input" value={sourceUrl} onChange={e => setSourceUrl(e.target.value)}
                placeholder="https://example.com/rss.xml" />
            </div>
            <div className="form-row" style={{ marginBottom: 12 }}>
              <div className="form-group">
                <label className="form-label">Category</label>
                <select className="form-select" value={sourceCategory} onChange={e => setSourceCategory(e.target.value)}>
                  {['markets','earnings','companies','technology','banking','energy','consumer','industrials','healthcare','global-markets','ipos','policy-regulation'].map(c => (
                    <option key={c} value={c}>{c.replace('-', ' ')}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Type</label>
                <select className="form-select" value={sourceType} onChange={e => setSourceType(e.target.value)}>
                  <option value="rss">RSS Feed</option>
                  <option value="sitemap">Sitemap</option>
                </select>
              </div>
            </div>

            <div className="dialog-actions">
              <button className="btn btn--secondary" onClick={() => setShowAddSource(false)}>Cancel</button>
              <button className="btn btn--primary" onClick={handleAddSource}
                disabled={!sourceName.trim() || !sourceUrl.trim()}>
                Add Source
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
