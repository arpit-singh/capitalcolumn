import { useState, useEffect, useRef } from 'react';
import { get, post, uploadFile } from '../lib/api';

export default function MediaLibrary() {
  const [assets, setAssets] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [urlMode, setUrlMode] = useState(false);
  const [fetchUrl, setFetchUrl] = useState('');
  const [altText, setAltText] = useState('');
  const fileRef = useRef(null);

  useEffect(() => { loadMedia(); }, []);

  async function loadMedia() {
    setLoading(true);
    try {
      const res = await get('/internal/media', { limit: 100, page: 1 });
      setAssets(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function showMsg(msg) {
    setMessage(msg);
    setTimeout(() => setMessage(''), 3000);
  }

  async function handleFileUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append('file', file);
      fd.append('alt_text', altText || file.name);
      await uploadFile('/internal/media/upload', fd);
      await loadMedia();
      showMsg('Image uploaded!');
      setAltText('');
    } catch (err) {
      showMsg(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = '';
    }
  }

  async function handleUrlFetch() {
    if (!fetchUrl.trim()) return;
    setUploading(true);
    try {
      await post('/internal/media/fetch', {
        source_url: fetchUrl,
        alt_text: altText || 'Image',
      });
      await loadMedia();
      showMsg('Image fetched and stored!');
      setFetchUrl('');
      setAltText('');
    } catch (err) {
      showMsg(`Fetch failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="media-library">
      {message && <div className="toast">{message}</div>}

      <div className="media-toolbar">
        <div className="media-upload-section">
          <div className="upload-toggle">
            <button
              className={`btn btn--sm ${!urlMode ? 'btn--primary' : 'btn--secondary'}`}
              onClick={() => setUrlMode(false)}
            >Upload File</button>
            <button
              className={`btn btn--sm ${urlMode ? 'btn--primary' : 'btn--secondary'}`}
              onClick={() => setUrlMode(true)}
            >Fetch URL</button>
          </div>

          <div className="upload-form">
            <input
              className="form-input form-input--sm"
              placeholder="Alt text"
              value={altText}
              onChange={(e) => setAltText(e.target.value)}
            />
            {urlMode ? (
              <>
                <input
                  className="form-input form-input--sm"
                  placeholder="https://example.com/image.jpg"
                  value={fetchUrl}
                  onChange={(e) => setFetchUrl(e.target.value)}
                />
                <button className="btn btn--primary btn--sm" onClick={handleUrlFetch} disabled={uploading}>
                  {uploading ? 'Fetching…' : 'Fetch'}
                </button>
              </>
            ) : (
              <>
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileUpload}
                  className="form-file"
                  disabled={uploading}
                />
              </>
            )}
          </div>
        </div>
        <div className="list-meta">{total} asset{total !== 1 ? 's' : ''}</div>
      </div>

      {loading ? (
        <div className="loading">Loading media…</div>
      ) : (
        <div className="media-grid">
          {assets.map((a) => (
            <div key={a.id} className="media-card">
              <div className="media-card-image">
                <img src={a.public_url} alt={a.alt_text} loading="lazy" />
              </div>
              <div className="media-card-info">
                <div className="media-card-name" title={a.filename}>{a.filename}</div>
                <div className="media-card-meta">
                  {a.size_bytes && <span>{(a.size_bytes / 1024).toFixed(0)} KB</span>}
                  <span>{a.mime_type}</span>
                </div>
                <input
                  className="media-card-url"
                  value={a.public_url}
                  readOnly
                  onClick={(e) => { e.target.select(); navigator.clipboard?.writeText(a.public_url); }}
                  title="Click to copy URL"
                />
              </div>
            </div>
          ))}
          {assets.length === 0 && (
            <div className="media-empty">No media assets yet. Upload an image to get started.</div>
          )}
        </div>
      )}
    </div>
  );
}
