import React, { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://localhost:8000/api";

interface MessageItem {
  id_: string;
  author_login: string;
  text: string;
  created_at: string;
}

interface UserItem {
  login: string;
  roles: string[];
}

export default function App() {
  const [token, setToken] = useState<string>(localStorage.getItem("token") || "");
  const [currentLogin, setCurrentLogin] = useState<string>(localStorage.getItem("login") || "");
  const [currentRoles, setCurrentRoles] = useState<string[]>(
    JSON.parse(localStorage.getItem("roles") || "[]")
  );

  const [isRegisterMode, setIsRegisterMode] = useState<boolean>(true);
  const [loginInput, setLoginInput] = useState<string>("");
  const [passwordInput, setPasswordInput] = useState<string>("");
  const [authError, setAuthError] = useState<string>("");
  const [authSuccess, setAuthSuccess] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [messageInput, setMessageInput] = useState<string>("");
  const [usersList, setUsersList] = useState<UserItem[]>([]);
  const [actionAlert, setActionAlert] = useState<{ text: string; isError: boolean } | null>(null);

  useEffect(() => {
    if (token) {
      fetchMessages();
      if (currentRoles.includes("admin")) {
        fetchUsers();
      }
    }
  }, [token]);

  const showAlert = (text: string, isError: boolean) => {
    setActionAlert({ text, isError });
    setTimeout(() => setActionAlert(null), 4000);
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;

    setLoading(true);
    setAuthError("");
    setAuthSuccess("");

    const endpoint = isRegisterMode ? "/register" : "/login";

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login: loginInput, password: passwordInput }),
      });

      const data = await response.json();

      if (!response.ok) {
        setAuthError(data.detail || "Request error");
        return;
      }

      setAuthSuccess(data.message);
      setToken(data.access_token);
      setCurrentLogin(data.login);
      setCurrentRoles(data.roles);

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("login", data.login);
      localStorage.setItem("roles", JSON.stringify(data.roles));
    } catch {
      setAuthError("API connect error");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken("");
    setCurrentLogin("");
    setCurrentRoles([]);
    localStorage.clear();
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch(`${API_URL}/messages`, {
        headers: { token },
      });
      const data = await response.json();
      if (response.ok) {
        setMessages(data.messages);
      }
    } catch {
      console.error("Messages loading error");
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim() || loading) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/messages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          token,
        },
        body: JSON.stringify({ text: messageInput }),
      });

      if (response.ok) {
        setMessageInput("");
        fetchMessages();
      } else {
        const data = await response.json();
        showAlert(data.detail || "Sending error", true);
      }
    } catch {
      showAlert("Sending error", true);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMessage = async (messageId: string) => {
    if (loading) return;
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/messages/${messageId}`, {
        method: "DELETE",
        headers: { token },
      });

      const data = await response.json();

      if (!response.ok) {
        showAlert(`Error ${response.status}: ${data.detail}`, true);
        return;
      }

      showAlert("Message deleted", false);
      fetchMessages();
    } catch {
      showAlert("Delete error", true);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_URL}/users`, {
        headers: { token },
      });
      const data = await response.json();
      if (response.ok) {
        setUsersList(data.users);
      }
    } catch {
      console.error("Users loading error");
    }
  };

  const handleToggleModerator = async (targetLogin: string, currentRolesList: string[]) => {
    if (loading) return;
    setLoading(true);

    const isModerator = currentRolesList.includes("moderator");
    const updatedRoles = isModerator ? ["user"] : ["user", "moderator"];

    try {
      const response = await fetch(`${API_URL}/roles`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          token,
        },
        body: JSON.stringify({
          target_login: targetLogin,
          roles: updatedRoles,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        showAlert(`Roles updated: ${targetLogin}`, false);
        fetchUsers();
      } else {
        showAlert(`Error ${response.status}: ${data.detail}`, true);
      }
    } catch {
      showAlert("Roles update error", true);
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="container">
        <div className="auth-box">
          <div className="auth-title">
            {isRegisterMode ? "Registration" : "login"}
          </div>

          <div className="tabs">
            <button
              type="button"
              className={`tab-btn ${isRegisterMode ? "active" : ""}`}
              onClick={() => {
                setIsRegisterMode(true);
                setAuthError("");
                setAuthSuccess("");
              }}
            >
              Registration
            </button>
            <button
              type="button"
              className={`tab-btn ${!isRegisterMode ? "active" : ""}`}
              onClick={() => {
                setIsRegisterMode(false);
                setAuthError("");
                setAuthSuccess("");
              }}
            >
              Login
            </button>
          </div>

          {}
          <div className="status-slot">
            {authError && <div className="status-banner status-error">{authError}</div>}
            {authSuccess && <div className="status-banner status-success">{authSuccess}</div>}
          </div>

          <form onSubmit={handleAuthSubmit}>
            <div className="form-group">
              <label>Login</label>
              <input
                type="text"
                value={loginInput}
                onChange={(e) => setLoginInput(e.target.value)}
                required
                placeholder="Alfredo"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={passwordInput}
                onChange={(e) => setPasswordInput(e.target.value)}
                required
                placeholder="••••••••"
                disabled={loading}
              />
            </div>
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? "Sending..." : isRegisterMode ? "Create account" : "login"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="navbar">
        <div className="user-info">
          <span>User: </span>
          <strong>{currentLogin}</strong>
          {currentRoles.map((role) => (
            <span
              key={role}
              className={`badge ${
                role === "admin" ? "badge-admin" : role === "moderator" ? "badge-moderator" : ""
              }`}
            >
              {role}
            </span>
          ))}
        </div>
        <button onClick={handleLogout} className="btn-logout" disabled={loading}>
          Logout
        </button>
      </div>

      <div className="status-slot">
        {actionAlert && (
          <div className={`status-banner ${actionAlert.isError ? "status-error" : "status-success"}`}>
            {actionAlert.text}
          </div>
        )}
      </div>

      <div className="workspace-grid">
        <div className="panel">
          <div className="panel-header">
            <span className="panel-title">Messages</span>
            <button
              type="button"
              onClick={fetchMessages}
              disabled={loading}
              style={{ background: "none", border: "none", color: "#60a5fa", cursor: "pointer", fontSize: "12px" }}
            >
              Update
            </button>
          </div>

          <div className="messages-container">
            {messages.length === 0 ? (
              <div style={{ color: "#777", fontSize: "13px" }}>No messages.</div>
            ) : (
              messages.map((item) => (
                <div key={item.id_} className="message-row">
                  <div>
                    <div className="msg-author">
                      {item.author_login}
                      <span className="msg-time">
                        {new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>
                    <div className="msg-content">{item.text}</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleDeleteMessage(item.id_)}
                    className="btn-delete"
                    disabled={loading}
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>

          <form onSubmit={handleSendMessage} className="chat-controls">
            <input
              type="text"
              placeholder="Message..."
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              {loading ? "..." : "Submit"}
            </button>
          </form>
        </div>

        <div className="panel">
          <div className="panel-header">
            <span className="panel-title">Roles manage</span>
          </div>

          {!currentRoles.includes("admin") ? (
            <div style={{ fontSize: "13px", color: "#777", padding: "20px 0", textAlign: "center" }}>
              Administrator rule required
            </div>
          ) : (
            <div className="users-table">
              {usersList.map((user) => {
                if (user.login === "admin") return null;
                const isMod = user.roles.includes("moderator");

                return (
                  <div key={user.login} className="user-row">
                    <div>
                      <div className="user-meta-login">{user.login}</div>
                      <div className="user-meta-roles">{user.roles.join(", ")}</div>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleToggleModerator(user.login, user.roles)}
                      className="btn-role-action"
                      disabled={loading}
                    >
                      {isMod ? "Remove moderator" : "Make moderator"}
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}