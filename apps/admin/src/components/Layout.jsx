import { NavLink, useLocation } from 'react-router-dom';
import { logout, getUser } from '../lib/api';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/articles', label: 'Articles', icon: '📝' },
  { to: '/pipeline', label: 'Pipeline', icon: '🤖' },
  { to: '/media', label: 'Media', icon: '🖼️' },
];

export default function Layout({ children }) {
  const user = getUser();
  const location = useLocation();

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="sidebar-brand">
          <span className="sidebar-brand-icon">⚡</span>
          <span className="sidebar-brand-text">CapitalColumn</span>
          <span className="sidebar-brand-sub">Admin</span>
        </div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `sidebar-link${isActive ? ' sidebar-link--active' : ''}`
              }
            >
              <span className="sidebar-link-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          {user && (
            <div className="sidebar-user">
              <div className="sidebar-user-name">{user.full_name}</div>
              <div className="sidebar-user-role">{user.role}</div>
            </div>
          )}
          <button className="sidebar-logout" onClick={logout}>
            Sign out
          </button>
        </div>
      </aside>
      <main className="admin-main">
        <header className="admin-topbar">
          <h1 className="topbar-title">
            {NAV_ITEMS.find((i) => location.pathname.startsWith(i.to))?.label || 'Admin'}
          </h1>
        </header>
        <div className="admin-content">{children}</div>
      </main>
    </div>
  );
}
