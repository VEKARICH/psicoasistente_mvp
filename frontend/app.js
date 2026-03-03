(function () {
  const API_BASE = '';
  const TOKEN_KEY = 'psico_jwt_token';
  const USER_KEY = 'psico_user';
  const DISCLAIMER = 'Esto no sustituye terapia profesional. Si estás en crisis o en peligro, busca ayuda profesional o servicios de emergencia de tu país.';

  function qs(selector) {
    return document.querySelector(selector);
  }

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function setSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  function getUser() {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch { return null; }
  }

  async function apiFetch(path, options = {}) {
    const token = getToken();
    const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    const text = await res.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch { data = { raw: text }; }
    if (!res.ok) {
      const error = new Error(data?.detail || `HTTP ${res.status}`);
      error.status = res.status;
      error.payload = data;
      throw error;
    }
    return data;
  }

  function setStatus(message, type = 'info') {
    const out = qs('#status-output') || qs('#response-meta');
    if (!out) return;
    out.textContent = message;
    if (out.id === 'response-meta') {
      out.style.color = type === 'error' ? '#fca5a5' : (type === 'success' ? '#86efac' : '');
    }
  }

  function redirectToChat() {
    window.location.href = '/chat';
  }

  function redirectToLogin() {
    window.location.href = '/';
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatDate(dateStr) {
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr || '';
    }
  }

  function appendMessage({ role, content, created_at, safety_flag, intent }) {
    const box = qs('#messages');
    if (!box) return;
    const div = document.createElement('div');
    div.className = `msg ${role}` + (safety_flag === 'CRISIS' ? ' crisis' : '');
    div.innerHTML = `
      <div class="meta">
        <strong>${role === 'user' ? 'Tú' : 'Asistente'}</strong>
        ${created_at ? `· ${escapeHtml(formatDate(created_at))}` : ''}
        ${intent ? `· intent=${escapeHtml(intent)}` : ''}
        ${safety_flag ? `· safety_flag=${escapeHtml(safety_flag)}` : ''}
      </div>
      <div class="body">${escapeHtml(content).replace(/\n/g, '<br>')}</div>
    `;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  async function loadHealth() {
    const el = qs('#health-status');
    if (!el) return;
    try {
      const data = await apiFetch('/health', { method: 'GET', headers: {} });
      el.textContent = `/health: status=${data.status} · tts_configured=${data.tts_configured}`;
    } catch (e) {
      el.textContent = `/health error: ${e.message}`;
    }
  }

  async function initAuthPage() {
    const existingToken = getToken();
    if (existingToken) {
      try {
        await apiFetch('/auth/me', { method: 'GET' });
        redirectToChat();
        return;
      } catch {
        clearSession();
      }
    }

    qs('#global-disclaimer').textContent = DISCLAIMER;

    const registerForm = qs('#register-form');
    const loginForm = qs('#login-form');

    registerForm?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(registerForm);
      const payload = {
        full_name: (fd.get('full_name') || '').toString().trim() || null,
        email: (fd.get('email') || '').toString().trim(),
        password: (fd.get('password') || '').toString(),
      };
      setStatus('Registrando...');
      try {
        const data = await apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(payload) });
        setSession(data.access_token, data.user);
        setStatus('Registro exitoso. Redirigiendo...', 'success');
        redirectToChat();
      } catch (err) {
        setStatus(`Error registro: ${err.message}`, 'error');
      }
    });

    loginForm?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(loginForm);
      const payload = {
        email: (fd.get('email') || '').toString().trim(),
        password: (fd.get('password') || '').toString(),
      };
      setStatus('Iniciando sesión...');
      try {
        const data = await apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(payload) });
        setSession(data.access_token, data.user);
        setStatus('Login exitoso. Redirigiendo...', 'success');
        redirectToChat();
      } catch (err) {
        setStatus(`Error login: ${err.message}`, 'error');
      }
    });
  }

  async function ensureAuth() {
    const token = getToken();
    if (!token) {
      redirectToLogin();
      throw new Error('No autenticado');
    }
    try {
      const me = await apiFetch('/auth/me', { method: 'GET' });
      localStorage.setItem(USER_KEY, JSON.stringify(me));
      return me;
    } catch (e) {
      clearSession();
      redirectToLogin();
      throw e;
    }
  }

  async function loadHistory() {
    const box = qs('#messages');
    if (!box) return;
    box.innerHTML = '';
    try {
      const items = await apiFetch('/chat/history', { method: 'GET' });
      if (!items.length) {
        appendMessage({ role: 'assistant', content: `Hola. Estoy aquí para acompañarte con orientación general.

${DISCLAIMER}`, created_at: new Date().toISOString() });
        return;
      }
      items.forEach(appendMessage);
    } catch (e) {
      appendMessage({ role: 'assistant', content: `No se pudo cargar historial: ${e.message}`, created_at: new Date().toISOString() });
    }
  }

  async function autoPlayAudio(audioUrl) {
    if (!audioUrl) return;
    const audio = qs('#assistant-audio');
    if (!audio) return;
    audio.src = audioUrl;
    try {
      await audio.play();
    } catch (e) {
      console.warn('Autoplay bloqueado por el navegador:', e);
      setStatus('Respuesta recibida. El navegador bloqueó auto-play; usa play manual si aparece.', 'info');
    }
  }

  async function initChatPage() {
    const me = await ensureAuth();
    const userEmail = qs('#user-email');
    if (userEmail) userEmail.textContent = me.email;

    await loadHealth();
    await loadHistory();

    qs('#logout-btn')?.addEventListener('click', () => {
      clearSession();
      redirectToLogin();
    });

    qs('#refresh-history-btn')?.addEventListener('click', async () => {
      setStatus('Recargando historial...');
      await loadHistory();
      setStatus('Historial actualizado.', 'success');
    });

    const form = qs('#chat-form');
    const input = qs('#message-input');
    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = (input.value || '').trim();
      if (!message) return;

      appendMessage({ role: 'user', content: message, created_at: new Date().toISOString() });
      input.value = '';
      input.focus();
      setStatus('Procesando mensaje...');

      try {
        const data = await apiFetch('/chat/message', {
          method: 'POST',
          body: JSON.stringify({ message }),
        });
        appendMessage({
          role: 'assistant',
          content: data.reply_text,
          created_at: new Date().toISOString(),
          safety_flag: data.safety_flag,
          intent: data.intent,
        });

        const meta = [];
        if (data.safety_flag) meta.push(`safety_flag=${data.safety_flag}`);
        if (data.audio_url) meta.push(`audio_url=${data.audio_url}`);
        if (data.audio_error) meta.push(`audio_error=${data.audio_error}`);
        setStatus(meta.join(' · ') || 'Respuesta recibida.', data.audio_error ? 'error' : 'success');

        if (data.audio_url) {
          await autoPlayAudio(data.audio_url);
        }
      } catch (err) {
        appendMessage({ role: 'assistant', content: `Error: ${err.message}`, created_at: new Date().toISOString() });
        setStatus(`Error enviando mensaje: ${err.message}`, 'error');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const page = document.body?.dataset?.page;
    if (page === 'auth') {
      await initAuthPage();
    } else if (page === 'chat') {
      try {
        await initChatPage();
      } catch (e) {
        console.error(e);
      }
    }
  });
})();