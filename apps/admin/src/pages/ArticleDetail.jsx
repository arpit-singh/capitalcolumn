import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { get, patch, post } from '../lib/api';
import StatusBadge from '../components/StatusBadge';
import ConfirmDialog from '../components/ConfirmDialog';

/**
 * Markdown-to-HTML converter for article preview.
 * Supports: headings, bold, italic, code, links, lists, tables, blockquotes, HRs.
 */
function renderMarkdown(md) {
  if (!md) return '';

  // Escape HTML first
  let raw = md
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  const lines = raw.split('\n');
  const blocks = [];
  let i = 0;

  function closeList() {
    // close any open list
  }

  while (i < lines.length) {
    const line = lines[i];

    // --- Horizontal rule ---
    if (/^-{3,}$/.test(line.trim()) || /^\*{3,}$/.test(line.trim())) {
      blocks.push('<hr class="article-divider" />');
      i++; continue;
    }

    // --- Table block (| ... | lines) ---
    if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
        tableLines.push(lines[i]);
        i++;
      }
      blocks.push(renderTable(tableLines));
      continue;
    }

    // --- Blockquote ---
    if (line.startsWith('&gt; ') || line === '&gt;') {
      const quoteLines = [];
      while (i < lines.length && (lines[i].startsWith('&gt; ') || lines[i] === '&gt;')) {
        quoteLines.push(lines[i].replace(/^&gt;\s?/, ''));
        i++;
      }
      const quoteContent = quoteLines.map(l => inlineFmt(l)).join('<br/>');
      // Check if it's a "Key Stat" callout
      if (quoteContent.includes('<strong>Key Stat')) {
        blocks.push(`<div class="callout-stat">${quoteContent}</div>`);
      } else {
        blocks.push(`<blockquote class="pull-quote">${quoteContent}</blockquote>`);
      }
      continue;
    }

    // --- Headings ---
    if (line.startsWith('### ')) {
      blocks.push(`<h3>${inlineFmt(line.slice(4))}</h3>`);
      i++; continue;
    }
    if (line.startsWith('## ')) {
      blocks.push(`<h2>${inlineFmt(line.slice(3))}</h2>`);
      i++; continue;
    }
    if (line.startsWith('# ')) {
      blocks.push(`<h1>${inlineFmt(line.slice(2))}</h1>`);
      i++; continue;
    }

    // --- Unordered list ---
    if (/^[-*]\s/.test(line)) {
      const items = [];
      while (i < lines.length && /^[-*]\s/.test(lines[i])) {
        items.push(`<li>${inlineFmt(lines[i].slice(2))}</li>`);
        i++;
      }
      blocks.push(`<ul>${items.join('')}</ul>`);
      continue;
    }

    // --- Ordered list ---
    if (/^\d+\.\s/.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        items.push(`<li>${inlineFmt(lines[i].replace(/^\d+\.\s/, ''))}</li>`);
        i++;
      }
      blocks.push(`<ol>${items.join('')}</ol>`);
      continue;
    }

    // --- Blank line ---
    if (line.trim() === '') {
      i++; continue;
    }

    // --- Regular paragraph ---
    blocks.push(`<p>${inlineFmt(line)}</p>`);
    i++;
  }

  return blocks.join('\n');
}

/** Render a GFM pipe table from lines */
function renderTable(tableLines) {
  if (tableLines.length < 2) return tableLines.map(l => `<p>${inlineFmt(l)}</p>`).join('');

  const parseCells = (line) => line.split('|').slice(1, -1).map(c => c.trim());

  const headers = parseCells(tableLines[0]);
  // Skip separator line (| --- | --- |)
  const startRow = tableLines[1].includes('---') ? 2 : 1;
  const rows = tableLines.slice(startRow).map(parseCells);

  let html = '<div class="table-wrap"><table class="data-table">';
  html += '<thead><tr>' + headers.map(h => `<th>${inlineFmt(h)}</th>`).join('') + '</tr></thead>';
  html += '<tbody>';
  rows.forEach((cells, idx) => {
    const cls = idx % 2 === 1 ? ' class="alt-row"' : '';
    html += `<tr${cls}>` + cells.map(c => `<td>${inlineFmt(c)}</td>`).join('') + '</tr>';
  });
  html += '</tbody></table></div>';
  return html;
}

/** Handle inline markdown: **bold**, *italic*, `code`, [text](url) */
function inlineFmt(text) {
  return text
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

export default function ArticleDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [dialog, setDialog] = useState(null);

  // Edit form state
  const [form, setForm] = useState({});

  useEffect(() => { loadArticle(); }, [id]);

  async function loadArticle() {
    setLoading(true);
    try {
      const data = await get(`/admin/articles/${id}`);
      setArticle(data);
      setForm({
        title: data.title,
        dek: data.dek || '',
        summary: data.summary || '',
        body_markdown: data.body_markdown,
        seo_title: data.seo_title || '',
        seo_description: data.seo_description || '',
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function showMessage(msg) {
    setMessage(msg);
    setTimeout(() => setMessage(''), 3000);
  }

  async function handleSave() {
    setSaving(true);
    try {
      const payload = { ...form };
      if (form.seo_title || form.seo_description) {
        payload.seo = { seo_title: form.seo_title, seo_description: form.seo_description };
        delete payload.seo_title;
        delete payload.seo_description;
      }
      await patch(`/admin/articles/${id}`, payload);
      await loadArticle();
      setEditing(false);
      showMessage('Article saved');
    } catch (err) {
      showMessage(`Error: ${err.message}`);
    } finally {
      setSaving(false);
    }
  }

  async function handlePublish() {
    try {
      await post(`/admin/articles/${id}/publish`);
      await loadArticle();
      showMessage('Article published!');
    } catch (err) {
      const msg = typeof err === 'object' ? (err.message || err.detail || JSON.stringify(err)) : String(err);
      showMessage(`Publish failed: ${msg}`);
    }
  }

  async function handleApprove() {
    try {
      await post(`/admin/articles/${id}/approve`);
      await loadArticle();
      showMessage('Article approved');
    } catch (err) {
      showMessage(`Error: ${err.message}`);
    }
  }

  async function handleReject(reason) {
    try {
      await post(`/admin/articles/${id}/reject?reason=${encodeURIComponent(reason)}`);
      await loadArticle();
      setDialog(null);
      showMessage('Article rejected');
    } catch (err) {
      showMessage(`Error: ${err.message}`);
    }
  }

  async function handleCorrection(note) {
    try {
      await post(`/admin/articles/${id}/correction?correction_note=${encodeURIComponent(note)}`);
      await loadArticle();
      setDialog(null);
      showMessage('Correction added');
    } catch (err) {
      showMessage(`Error: ${err.message}`);
    }
  }

  if (loading) return <div className="loading">Loading article…</div>;
  if (!article) return <div className="loading">Article not found</div>;

  return (
    <div className="article-detail">
      {message && <div className="toast">{message}</div>}

      {dialog === 'reject' && (
        <ConfirmDialog
          title="Reject Article"
          message="Provide a reason for rejecting this article."
          inputLabel="Rejection reason"
          onConfirm={handleReject}
          onCancel={() => setDialog(null)}
        />
      )}
      {dialog === 'correction' && (
        <ConfirmDialog
          title="Add Correction"
          message="Describe the correction made to this article."
          inputLabel="Correction note"
          onConfirm={handleCorrection}
          onCancel={() => setDialog(null)}
        />
      )}

      {/* Header */}
      <div className="detail-header">
        <button className="btn btn--ghost" onClick={() => navigate('/articles')}>← Back</button>
        <div className="detail-header-actions">
          {!editing ? (
            <>
              <button className="btn btn--secondary" onClick={() => setEditing(true)}>Edit</button>
              {article.status !== 'published' && (
                <button className="btn btn--primary" onClick={handlePublish}>Publish</button>
              )}
              {!article.is_editor_reviewed && (
                <button className="btn btn--success" onClick={handleApprove}>Approve</button>
              )}
              <button className="btn btn--warning" onClick={() => setDialog('correction')}>Correction</button>
              {article.status !== 'rejected' && (
                <button className="btn btn--danger" onClick={() => setDialog('reject')}>Reject</button>
              )}
            </>
          ) : (
            <>
              <button className="btn btn--secondary" onClick={() => setEditing(false)}>Cancel</button>
              <button className="btn btn--primary" onClick={handleSave} disabled={saving}>
                {saving ? 'Saving…' : 'Save'}
              </button>
            </>
          )}
        </div>
      </div>

      <div className="detail-body">
        {/* Main content */}
        <div className="detail-main">
          {editing ? (
            <div className="edit-form">
              <div className="form-group">
                <label className="form-label">Title</label>
                <input className="form-input" value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Dek / Subtitle</label>
                <input className="form-input" value={form.dek}
                  onChange={(e) => setForm({ ...form, dek: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Summary</label>
                <textarea className="form-textarea" rows={3} value={form.summary}
                  onChange={(e) => setForm({ ...form, summary: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Body (Markdown)</label>
                <textarea className="form-textarea form-textarea--code" rows={20} value={form.body_markdown}
                  onChange={(e) => setForm({ ...form, body_markdown: e.target.value })} />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">SEO Title</label>
                  <input className="form-input" value={form.seo_title}
                    onChange={(e) => setForm({ ...form, seo_title: e.target.value })} />
                </div>
                <div className="form-group">
                  <label className="form-label">SEO Description</label>
                  <input className="form-input" value={form.seo_description}
                    onChange={(e) => setForm({ ...form, seo_description: e.target.value })} />
                </div>
              </div>
            </div>
          ) : (
            <div className="article-preview">
              <h2 className="preview-title">{article.title}</h2>
              {article.dek && <p className="preview-dek">{article.dek}</p>}
              {article.featured_image && (
                <div className="preview-image">
                  <img src={article.featured_image.public_url} alt={article.featured_image.alt_text || article.title} />
                </div>
              )}
              <div className="preview-body" dangerouslySetInnerHTML={{ __html: renderMarkdown(article.body_markdown) }} />
            </div>
          )}

          {/* Sources */}
          {article.sources?.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">Sources ({article.sources.length})</h3>
              <div className="sources-list">
                {article.sources.map((s) => (
                  <div key={s.id} className="source-card">
                    <div className="source-card-name">
                      {s.is_primary_source && <span className="badge badge--green">Primary</span>}
                      {s.source_name}
                    </div>
                    <div className="source-card-meta">
                      {s.publisher && <span>{s.publisher}</span>}
                      <span className="source-card-type">{s.source_type.replace('_', ' ')}</span>
                    </div>
                    <a href={s.source_url} target="_blank" rel="noopener" className="source-card-link">
                      {s.source_url.length > 60 ? s.source_url.slice(0, 60) + '…' : s.source_url}
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <aside className="detail-sidebar">
          <div className="sidebar-section">
            <h4 className="sidebar-section-title">Status</h4>
            <StatusBadge status={article.status} />
          </div>
          <div className="sidebar-section">
            <h4 className="sidebar-section-title">Metadata</h4>
            <dl className="meta-list">
              <dt>Type</dt><dd>{article.article_type}</dd>
              <dt>Category</dt><dd>{article.category?.name || '—'}</dd>
              <dt>Reading Time</dt><dd>{article.reading_time_minutes} min</dd>
              <dt>Language</dt><dd>{article.language}</dd>
              <dt>Slug</dt><dd className="meta-slug">{article.slug}</dd>
            </dl>
          </div>
          <div className="sidebar-section">
            <h4 className="sidebar-section-title">AI Provenance</h4>
            <dl className="meta-list">
              <dt>AI Generated</dt><dd>{article.is_ai_generated ? 'Yes' : 'No'}</dd>
              <dt>Editor Reviewed</dt><dd>{article.is_editor_reviewed ? 'Yes' : 'No'}</dd>
              <dt>Fact Check</dt><dd>{article.fact_check_status?.replace('_', ' ')}</dd>
              {article.ai_pipeline_name && <><dt>Pipeline</dt><dd>{article.ai_pipeline_name}</dd></>}
              {article.confidence_score && <><dt>Confidence</dt><dd>{article.confidence_score}</dd></>}
            </dl>
          </div>
          <div className="sidebar-section">
            <h4 className="sidebar-section-title">Dates</h4>
            <dl className="meta-list">
              <dt>Created</dt><dd>{new Date(article.created_at).toLocaleString()}</dd>
              <dt>Updated</dt><dd>{new Date(article.updated_at).toLocaleString()}</dd>
              {article.published_at && <><dt>Published</dt><dd>{new Date(article.published_at).toLocaleString()}</dd></>}
            </dl>
          </div>
          {article.correction_note && (
            <div className="sidebar-section sidebar-section--warning">
              <h4 className="sidebar-section-title">Correction</h4>
              <p className="correction-note">{article.correction_note}</p>
              {article.last_corrected_at && (
                <time className="correction-date">{new Date(article.last_corrected_at).toLocaleString()}</time>
              )}
            </div>
          )}
          {article.tags?.length > 0 && (
            <div className="sidebar-section">
              <h4 className="sidebar-section-title">Tags</h4>
              <div className="tag-chips">
                {article.tags.map((t) => <span key={t.id} className="tag-chip">{t.name}</span>)}
              </div>
            </div>
          )}
          {article.tickers?.length > 0 && (
            <div className="sidebar-section">
              <h4 className="sidebar-section-title">Tickers</h4>
              <div className="tag-chips">
                {article.tickers.map((t) => <span key={t.id} className="tag-chip tag-chip--ticker">{t.ticker}</span>)}
              </div>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
