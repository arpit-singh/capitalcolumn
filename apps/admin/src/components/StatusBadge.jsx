const STATUS_CONFIG = {
  draft: { label: 'Draft', className: 'badge--draft' },
  in_review: { label: 'In Review', className: 'badge--review' },
  scheduled: { label: 'Scheduled', className: 'badge--scheduled' },
  published: { label: 'Published', className: 'badge--published' },
  archived: { label: 'Archived', className: 'badge--archived' },
  rejected: { label: 'Rejected', className: 'badge--rejected' },
};

export default function StatusBadge({ status }) {
  const config = STATUS_CONFIG[status] || { label: status, className: '' };
  return <span className={`status-badge ${config.className}`}>{config.label}</span>;
}
