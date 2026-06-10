import { useState } from 'react';

export default function ConfirmDialog({ title, message, inputLabel, onConfirm, onCancel }) {
  const [inputValue, setInputValue] = useState('');

  return (
    <div className="dialog-overlay" onClick={onCancel}>
      <div className="dialog" onClick={(e) => e.stopPropagation()}>
        <h3 className="dialog-title">{title}</h3>
        <p className="dialog-message">{message}</p>
        {inputLabel && (
          <div className="dialog-input-group">
            <label className="dialog-label">{inputLabel}</label>
            <textarea
              className="dialog-textarea"
              rows={3}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              autoFocus
            />
          </div>
        )}
        <div className="dialog-actions">
          <button className="btn btn--secondary" onClick={onCancel}>Cancel</button>
          <button
            className="btn btn--danger"
            onClick={() => onConfirm(inputValue)}
            disabled={inputLabel && !inputValue.trim()}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
