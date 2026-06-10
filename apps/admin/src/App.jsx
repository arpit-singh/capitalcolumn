import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './lib/api';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ArticleList from './pages/ArticleList';
import ArticleDetail from './pages/ArticleDetail';
import MediaLibrary from './pages/MediaLibrary';
import Pipeline from './pages/Pipeline';

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout><Dashboard /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/articles"
          element={
            <ProtectedRoute>
              <Layout><ArticleList /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/articles/:id"
          element={
            <ProtectedRoute>
              <Layout><ArticleDetail /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/media"
          element={
            <ProtectedRoute>
              <Layout><MediaLibrary /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/pipeline"
          element={
            <ProtectedRoute>
              <Layout><Pipeline /></Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
