import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { LoginPage } from "./auth/LoginPage";
import { useAuth } from "./auth/AuthContext";
import { DocsPage } from "./pages/DocsPage";
import { DocPage } from "./pages/DocPage";
import { UsersPage } from "./pages/UsersPage";
import { AdminPage } from "./pages/AdminPage";
import { roleAtLeast } from "./api/roles";

function TopBar() {
  const { session, logout } = useAuth();
  const location = useLocation();
  const link = (to: string, label: string) => (
    <Link to={to} className={location.pathname.startsWith(to) ? "active" : ""}>
      {label}
    </Link>
  );
  return (
    <header className="topbar">
      <div className="brand">
        AgenticDocer <span className="sub">文档评审台</span>
      </div>
      <nav>
        {link("/docs", "文档")}
        {session && roleAtLeast(session.role, "admin") ? link("/users", "用户与权限") : null}
        {session && roleAtLeast(session.role, "admin") ? link("/admin", "监控") : null}
      </nav>
      {session ? (
        <div className="userchip">
          <span>{session.username}</span>
          <span className="role">{session.role}</span>
          <button className="ghost" onClick={() => void logout()}>
            退出
          </button>
        </div>
      ) : null}
    </header>
  );
}

export function App() {
  const { session, loading } = useAuth();
  if (loading) {
    return <div className="loading">正在载入…</div>;
  }
  if (!session) {
    return <LoginPage />;
  }
  return (
    <>
      <TopBar />
      <Routes>
        <Route path="/" element={<Navigate to="/docs" replace />} />
        <Route path="/docs" element={<DocsPage />} />
        <Route path="/docs/:docId" element={<DocPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="*" element={<Navigate to="/docs" replace />} />
      </Routes>
    </>
  );
}
