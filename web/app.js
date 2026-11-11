// Rossmax Connect: vanilla-JS port of the designer's Make app. No dependencies.
// Routes: #/login, #/residents, #/residents/RM-20418, #/devices, #/settings
// Force a list state with ?state=loading|empty|error on #/residents and #/devices.
// Routes also work as a query (/?route=/devices&session=test) so any #hash in the URL is left alone.
(function () {
  const D = window.TEST_DATA;
  const app = document.getElementById("app");
  const SESSION_KEY = "rossmax-test-session";
  // pointer modes (CMP-11): a mouse opens the sidebar on hover; touch uses the toggle; a device with both gets both
  const hoverMQ = matchMedia("(hover: hover) and (pointer: fine)");
  const touchMQ = matchMedia("(any-pointer: coarse)");
  const phoneMQ = matchMedia("(max-width: 767px)");   // phones (FND-16): the sidebar becomes a bottom tab bar
  const isPhone = () => phoneMQ.matches;
  const navMode = () => isPhone() ? { hover: false, toggle: false } : { hover: hoverMQ.matches, toggle: touchMQ.matches || !hoverMQ.matches };
  const navPinned = () => navMode().toggle && S.navExpanded;   // opened with the toggle: pushes the page over
  const navAuto = () => navMode().hover && !navPinned();      // mouse: opens over the page on hover or focus
  const navOpen = () => navPinned() || (navAuto() && S.navPeek);
  const NAV_KEY = "rossmax-nav-pinned";   // touch: the toggle pinned the sidebar open (1) or not (unset / 0); remembered across sign-ins
  try { localStorage.removeItem("rossmax-nav-expanded"); } catch (e) { /* older versions forced this to expanded at every sign-in */ }

  // ---------- icons (paths copied from the design) ----------
  const P = {
    alert: '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5"/><path d="M12 16.2v.1"/>',
    home: '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    bluetooth: '<path d="m6 7.5 12 9L12 21V3l6 4.5-12 9"/>',
    logout: '<path d="M10 17l5-5-5-5"/><path d="M15 12H3"/><path d="M15 3h5v18h-5"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    chevronDown: '<path d="m7 10 5 5 5-5"/>',
    chevronRight: '<path d="m9 18 6-6-6-6"/>',
    arrowLeft: '<path d="m15 18-6-6 6-6"/>',
    chevronsLeft: '<path d="m11 17-5-5 5-5"/><path d="m18 17-5-5 5-5"/>',
    chevronsRight: '<path d="m6 17 5-5-5-5"/><path d="m13 17 5-5-5-5"/>',
    bed: '<path d="M3 19v-8h18v8"/><path d="M3 15h18"/><path d="M6 11V7h5a3 3 0 0 1 3 3v1"/>',
    device: '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 6h6M10 18h4"/>',
    wifi: '<path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8 15.5a6 6 0 0 1 8 0"/><circle cx="12" cy="19" r=".8" fill="currentColor" stroke="none"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    filter: '<path d="M4 5h16l-6 7.5V19l-4 1.5v-8L4 5z"/>',
    filterOff: '<path d="M8 4h12v2.17a2 2 0 0 1-.59 1.41l-3.91 3.92m-.5 3.5v4l-6 2v-8.5L4.52 8.57A2 2 0 0 1 4 7.23V5"/><path d="M3 3l18 18"/>',
    unlink: '<path d="m9.5 14.5 5-5"/><path d="M7 17H5a4 4 0 0 1 0-8h3M17 7h2a4 4 0 0 1 0 8h-3"/><path d="m4 4 16 16"/>',
    trash: '<path d="M4 7h16M9 7V4h6v3M7 7l1 14h8l1-14M10 11v6M14 11v6"/>',
    more: '<circle cx="5" cy="12" r="1.9" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.9" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.9" fill="currentColor" stroke="none"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    heart: '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>',
    eye: '<path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z"/><circle cx="12" cy="12" r="2.5"/>',
    eyeOff: '<path d="m3 3 18 18"/><path d="M10.6 6.1A9 9 0 0 1 12 6c6 0 9.5 6 9.5 6a14 14 0 0 1-2.1 2.8M6.5 6.5C4 8 2.5 12 2.5 12s3.5 6 9.5 6a9 9 0 0 0 3-.5"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
    thermometer: '<path d="M14 14.8V5a4 4 0 0 0-8 0v9.8a6 6 0 1 0 8 0Z"/><path d="M10 7v10"/>',
    activity: '<path d="M3 12h4l2-6 4 12 2-6h6"/>',
    scale: '<rect x="3" y="4" width="18" height="17" rx="3"/><path d="M8 9a4.5 4.5 0 0 1 8 0M12 9l2-2"/>',
    pressure: '<path d="M4 13h3l2-5 3 9 2-4h6"/><path d="M12 22s8-4.4 8-11a4.5 4.5 0 0 0-8-2.8A4.5 4.5 0 0 0 4 11c0 6.6 8 11 8 11Z"/>',
  };
  const ic = (name, size = 20) =>
    `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[name]}</svg>`;
  function deviceTypeIcon(type) {
    const t = type.toLowerCase();
    if (t.includes("pressure")) return "pressure";
    if (t.includes("oximeter") || t.includes("oxygen")) return "activity";
    if (t.includes("scale") || t.includes("weight")) return "scale";
    if (t.includes("thermometer") || t.includes("temperature")) return "thermometer";
    return "device";
  }

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const residentById = (id) => D.residents.find((r) => r.id === id);
  const initialsOf = (name) => name.split(" ").map((v) => v[0]).join("");

  // ---------- state ----------
  const S = {
    zone: "North Wing",
    email: D.login.email,
    password: D.login.password,
    loginErr: {},   // sign-in field -> error message (CMP-2)
    filterSheet: false,   // phones: the Filters sheet is open
    pwVisible: false,
    remember: true,
    search: "",
    page: 1,
    pageSize: 10,
    wards: [],        // selected care areas (empty = all)
    navPeek: false,   // mouse: the rail is open over the page right now
    navExpanded: localStorage.getItem(NAV_KEY) === "1",   // collapsed icon rail by default; the toggle (touch) pins it open, and that is remembered
    openDd: null,     // id of the open dropdown: "ward" | "zone" | "size-top" | "size-bottom"
    wardQuery: "",
    profileOpen: false,
    readingsFor: null,
    readings: [],
    saved: false,
    devices: D.devices.map((d) => ({ ...d })),
    scanning: false,
    discoverable: true,
    toast: "",
    cfg: { ...D.server },
    unlocked: false, unlockOpen: false, confirmOpen: false, tested: false, testing: false, cfgSaved: false, showToken: false, pin: "",
  };
  let toastTimer;
  const isLoggedIn = () => localStorage.getItem(SESSION_KEY) === "1";

  function parseRoute() {
    const qs = new URLSearchParams(location.search);
    if (qs.get("session") === "test") localStorage.setItem(SESSION_KEY, "1");
    const raw = location.hash.startsWith("#/") ? location.hash.slice(1) : qs.get("route") || "/residents";
    const [path, query] = raw.split("?");
    const params = new URLSearchParams(query || "");
    return { parts: path.split("/").filter(Boolean), state: params.get("state") || qs.get("state") };
  }

  // Toasts stay for --toast-duration (CMP-17) and pause while the pointer is over them.
  let toastClear = null;
  const toastMs = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--toast-duration")) || 6000;
  function armToast(clear) {
    toastClear = clear;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastClear = null; clear(); render(); }, toastMs());
  }
  function notify(msg) {
    S.toast = msg;
    render();
    armToast(() => { S.toast = ""; });
  }
  document.addEventListener("mouseover", (e) => { if (toastClear && e.target.closest(".toast")) clearTimeout(toastTimer); });
  document.addEventListener("mouseout", (e) => {
    const t = e.target.closest(".toast");
    if (toastClear && t && !t.contains(e.relatedTarget)) armToast(toastClear);
  });

  // ---------- dates and times (CNT-1, CNT-2): ISO 8601; relative wording only within 24 hours, with the exact time attached ----------
  const LOADED = Date.now();
  const pad = (n) => String(n).padStart(2, "0");
  const isoLocal = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  const isoFull = (d) => { const o = -d.getTimezoneOffset(); return `${isoLocal(d).replace(" ", "T")}:00${o >= 0 ? "+" : "-"}${pad(Math.floor(Math.abs(o) / 60))}:${pad(Math.abs(o) % 60)}`; };
  const relText = (d) => {
    const min = Math.floor((Date.now() - d) / 60000);
    if (min < 1) return "Just now";
    if (min < 60) return `${min} min ago`;
    if (min < 24 * 60) return `${Math.floor(min / 60)} h ago`;
    return isoLocal(d);   // older than a day: the date and time itself
  };
  const syncedAt = (minAgo) => new Date(LOADED - minAgo * 60000);
  // relative wording always comes with the exact time, visible (CNT-2): "2 min ago · 15:08"; the date is added when it is not today
  const whenText = (d) => {
    const rel = relText(d), exact = isoLocal(d);
    if (rel === exact) return exact;
    return `${rel} · ${exact.slice(0, 10) === isoLocal(new Date()).slice(0, 10) ? exact.slice(11) : exact}`;
  };
  const timeHtml = (d) => `<time datetime="${isoFull(d)}" data-rel>${whenText(d)}</time>`;
  setInterval(() => app.querySelectorAll("time[data-rel]").forEach((t) => { t.textContent = whenText(new Date(t.getAttribute("datetime"))); }), 60000);   // keep "N min ago" current without re-rendering

  // ---------- sign-in validation (CMP-2): on leaving a field and on submit; the error sits under the field ----------
  const LOGIN_RULES = {
    email: (v) => !v.trim() ? "Enter your staff ID or email address."
      : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) || /^[A-Za-z]{2,4}-?\d{3,6}$/.test(v.trim()) ? ""
      : "Enter a staff ID such as RN-1042, or an email address such as name@example.org.",
    password: (v) => !v ? "Enter your password." : "",
  };
  const fieldErrAttrs = (k) => S.loginErr[k] ? ` aria-invalid="true" aria-describedby="login-${k}-err"` : "";
  const fieldErrHtml = (k) => S.loginErr[k] ? `<div class="field-error" id="login-${k}-err">${ic("alert", 16)}<span>${esc(S.loginErr[k])}</span></div>` : "";
  // update one field's error in place (a full re-render while focus moves between fields would lose the focus)
  function showLoginErr(k) {
    const input = app.querySelector(`#login-${k}`);
    if (!input) return;
    const label = input.closest(".login-label");
    const old = app.querySelector(`#login-${k}-err`);
    if (old) old.remove();
    if (S.loginErr[k]) {
      input.setAttribute("aria-invalid", "true"); input.setAttribute("aria-describedby", `login-${k}-err`);
      label.insertAdjacentHTML("afterend", fieldErrHtml(k));
    } else { input.removeAttribute("aria-invalid"); input.removeAttribute("aria-describedby"); }
  }
  app.addEventListener("focusout", (e) => {   // leaving a field checks its format; an empty field is only reported on submit
    const k = e.target.dataset && e.target.dataset.bind;
    if (!LOGIN_RULES[k] || !e.target.closest("#login-form")) return;
    const msg = S[k] === "" && !S.loginErr[k] ? "" : LOGIN_RULES[k](S[k]);
    if (msg !== (S.loginErr[k] || "")) { S.loginErr[k] = msg; showLoginErr(k); }
  });

  // ---------- shared pieces ----------
  const toastHtml = (msg) => `<div class="toast" role="status"><span class="toast__check">${ic("check", 13)}</span>${esc(msg)}</div>`;

  const logo = (light) => `
    <div class="logo${light ? " logo--light" : ""}">
      <div class="logo__mark">${ic("heart", 21)}</div>
      <div class="logo__text"><div class="logo__name">Rossmax Connect</div><div class="logo__sub">Care gateway</div></div>
    </div>`;

  function header(title, sub, right) {
    return `<header class="page-header"><div><h1>${esc(title)}</h1><p>${esc(sub)}</p></div>${right || ""}</header>`;
  }
  const gatewayPill = `<span class="status-pill"><span></span> Gateway connected</span>`;

  function stateBlock(state, emptyMsg) {
    if (state === "loading") return `<div class="state" role="status" aria-live="polite"><div class="spinner" aria-hidden="true"></div>Loading…</div>`;
    if (state === "error") return `<div class="state state--error" role="alert"><strong>Couldn't load data.</strong> Check the gateway connection and try again.<br><br><button class="secondary-btn" data-action="reload">Retry</button></div>`;
    if (state === "empty") return `<div class="state">${emptyMsg}</div>`;
    return null;
  }

  const navToggleHtml = () => `${ic(S.navExpanded ? "chevronsLeft" : "chevronsRight")}<span class="nav-label">${S.navExpanded ? "Collapse menu" : "Expand menu"}</span>`;
  function shell(page, body, overlay) {
    const nav = [["residents", "home", "Residents"], ["devices", "bluetooth", "Devices"]]
      .map(([id, icon, label]) => `
        <button class="nav-item${page === id ? " active" : ""}" data-action="nav" data-to="${id}" title="${label}" aria-label="${label}"${page === id ? ' aria-current="page"' : ""}>
          ${ic(icon, 20)}<span class="nav-label">${label}</span>${id === "devices" ? `<span class="nav-badge">${S.devices.length}</span>` : ""}
        </button>`).join("");
    const menu = S.profileOpen ? `
      <div class="profile-menu">
        <div class="profile-menu__head">Staff menu</div>
        <button class="profile-menu-item" data-action="nav" data-to="settings">
          ${ic("shield", 17)}<span><strong>System setup</strong><small>Administrator access</small></span>${ic("chevronRight", 15)}
        </button>
        <button class="profile-menu-item profile-menu-item--phone" data-action="logout">${ic("logout", 17)}<span><strong>Sign out</strong><small>${D.user.name}</small></span></button>
      </div>` : "";
    const toggleLabel = S.navExpanded ? "Collapse navigation" : "Expand navigation";
    const toggleRow = navMode().toggle ? `<div class="sidebar__toggle-row"><button type="button" class="nav-item sidebar__toggle" data-action="nav-toggle" aria-expanded="${S.navExpanded}" aria-label="${toggleLabel}" title="${toggleLabel}">${navToggleHtml()}</button></div>` : "";
    return `
      <div class="app-shell${navOpen() ? " nav-expanded" : ""}${navAuto() ? " nav-auto" : ""}">
        <aside class="sidebar">
          <div class="sidebar__logo">${logo(true)}</div>
          <nav class="sidebar__nav" aria-label="Main">
            ${nav}
          </nav>
          ${toggleRow}
          <div class="sidebar__foot">
            ${menu}
            <button type="button" class="profile${S.profileOpen ? " open" : ""}${page === "settings" ? " current" : ""}" data-action="profile" aria-haspopup="menu" aria-expanded="${S.profileOpen}" aria-label="Staff menu: ${D.user.name}, ${D.user.role}" title="${D.user.name}">
              <span class="profile__avatar">${D.user.initials}</span>
              <span class="profile__who"><span class="profile__name truncate">${D.user.name}</span><span class="profile__role">${D.user.role}</span></span>
              <span class="profile__tab-label">Account</span>
            </button>
            <button class="nav-item" data-action="logout" title="Sign out" aria-label="Sign out">${ic("logout", 20)}<span class="nav-label">Sign out</span></button>
          </div>
        </aside>
        <main class="main">${body}</main>
      </div>${overlay || ""}${S.toast ? toastHtml(S.toast) : ""}`;
  }

  // ---------- screens ----------
  function loginScreen() {
    return `
      <main class="login-shell">
        <section class="login-brand">
          <div class="login-brand__inner">
            ${logo(true)}
            <div class="login-brand__copy">
              <div class="login-brand__icon">${ic("bluetooth", 28)}</div>
              <h1>Connected care,<br>for every resident.</h1>
              <p>Securely connect Rossmax medical devices and keep resident readings flowing to your care systems.</p>
            </div>
            <div class="login-brand__status"><i></i> All systems operational</div>
          </div>
          <div class="pulse-ring pulse-ring-one"></div><div class="pulse-ring pulse-ring-two"></div><div class="pulse-ring pulse-ring-three"></div><div class="pulse-ring pulse-ring-four"></div>
        </section>
        <section class="login-form-side">
          <div class="login-form-wrap">
            <div class="login-mobile-logo">${logo(false)}</div>
            <div>
              <div class="login-eyebrow">Staff access</div>
              <h2>Welcome back</h2>
              <p class="login-sub">Sign in with your community staff credentials.</p>
            </div>
            <form class="login-form" id="login-form" novalidate>
              <label class="login-label"><span>Staff ID or email</span>
                <input class="field" id="login-email" type="text" data-bind="email" value="${esc(S.email)}" autocomplete="username" spellcheck="false"${fieldErrAttrs("email")} /></label>
              ${fieldErrHtml("email")}
              <label class="login-label"><span>Password</span>
                <div class="pw-wrap">
                  <input class="field" id="login-password" type="${S.pwVisible ? "text" : "password"}" data-bind="password" value="${esc(S.password)}" autocomplete="current-password"${fieldErrAttrs("password")} />
                  <button type="button" class="pw-toggle" data-action="pw" aria-label="${S.pwVisible ? "Hide" : "Show"} password">${ic(S.pwVisible ? "eyeOff" : "eye")}</button>
                </div></label>
              ${fieldErrHtml("password")}
              <div class="login-row">
                <button type="button" class="remember${S.remember ? " on" : ""}" data-action="remember" role="checkbox" aria-checked="${S.remember}">
                  <span class="remember__box">${S.remember ? ic("check", 14) : ""}</span>Remember this device
                </button>
                <button type="button" class="link-btn">Need help?</button>
              </div>
              <button class="primary-btn" type="submit">Sign in securely ${ic("chevronRight", 18)}</button>
            </form>
            <p class="login-foot">Authorized care staff only. All activity is logged<br>and protected under your organization’s security policy.</p>
          </div>
        </section>
      </main>`;
  }

  // Single-select custom dropdown. Replaces every native <select> so the list looks and aligns the same everywhere.
  function dropdown({ id, value, options, aria, variant = "", up = false, prefix = "", footer = "" }) {
    const open = S.openDd === id;
    const cur = options.find((o) => String(o.value) === String(value)) || options[0];
    const opt = (o) => {
      const on = String(o.value) === String(cur.value);
      return `<button type="button" class="dd__option${on ? " selected" : ""}" role="option" aria-selected="${on}" data-action="dd-pick" data-dd="${id}" data-value="${esc(o.value)}"><span>${esc(o.label)}</span>${on ? ic("check") : ""}</button>`;
    };
    return `<div class="dd${variant ? " dd--" + variant : ""}${up ? " dd--up" : ""}${open ? " open" : ""}" data-dd="${id}">
        <button type="button" class="dd__trigger" data-action="dd-open" data-dd="${id}" aria-haspopup="listbox" aria-expanded="${open}" aria-label="${esc(aria)}: ${esc(cur.label)}"><span class="dd__label">${prefix ? `<span class="dd__prefix">${esc(prefix)}</span>` : ""}${esc(cur.label)}</span></button>
        ${ic("chevronDown").replace("<svg", '<svg class="dd__chevron"')}
        ${open ? `<div class="dd__panel"><div class="dd__list" role="listbox" aria-label="${esc(aria)}">${options.map(opt).join("")}</div>${footer ? `<div class="dd__footer">${esc(footer)}</div>` : ""}</div>` : ""}
      </div>`;
  }

  // Care-area filter: multi-select with a search box (same pattern as the staff settings page in EncoreMed).
  function careAreaFilter() {
    const open = S.openDd === "ward";
    const picked = D.careAreas.filter((w) => S.wards.includes(w));
    const q = S.wardQuery.trim().toLowerCase();
    const opts = D.careAreas.filter((w) => w.toLowerCase().includes(q));
    const label = picked.length ? picked.join(", ") : "All care areas";
    const option = (w) => {
      const on = picked.includes(w);
      return `<button type="button" class="ms__option${on ? " selected" : ""}" role="option" aria-selected="${on}" data-action="ward-toggle" data-value="${esc(w)}"><span class="ms__check">${on ? ic("check") : ""}</span><span>${esc(w)}</span></button>`;
    };
    return `
          <div class="ms${open ? " open" : ""}${picked.length ? " has-value" : ""}" data-dd="ward">
            <button type="button" class="ms__trigger filter-field" data-action="ward-open" aria-haspopup="listbox" aria-expanded="${open}" aria-label="Care areas: ${esc(label)}" title="${esc(label)}">
              <span class="ms__label${picked.length ? "" : " placeholder"}">${esc(label)}</span>
            </button>
            ${picked.length ? `<button type="button" class="ms__clear" data-action="ward-clear" aria-label="Clear care areas">${ic("close")}</button>` : ""}
            ${ic("chevronDown").replace("<svg", '<svg class="ms__chevron"')}
            ${open ? `
            <div class="ms__panel">
              <div class="ms__search">
                <input class="ms__search-input" type="text" role="searchbox" autocomplete="off" aria-label="Search care areas" data-bind="wardQuery" value="${esc(S.wardQuery)}" />
                ${ic("search")}
              </div>
              <div class="ms__list" role="listbox" aria-multiselectable="true" aria-label="Care areas">
                ${opts.length ? opts.map(option).join("") : '<div class="ms__empty">No results found</div>'}
              </div>
            </div>` : ""}
          </div>`;
  }

  // Page number buttons: a sliding window of up to PAGER_WINDOW consecutive pages around the current one.
  // First / Last cover the ends, so there are no pinned first/last numbers and no ellipses; the row is never wider than 5 numbers.
  const PAGER_WINDOW = 5;
  function pageItems(cur, pages) {
    const size = Math.min(PAGER_WINDOW, pages);
    const start = Math.min(Math.max(cur - Math.floor(size / 2), 1), pages - size + 1);
    return Array.from({ length: size }, (_, i) => start + i);
  }

  function paginationBar(total, from, shown, pages, pos) {
    const cur = S.page;
    const nav = (label, target, icon, disabled, first) => `
      <button type="button" class="pager__btn pager__btn--nav" data-action="page" data-page="${target}" aria-label="${label} page"${disabled ? " disabled" : ""}>
        ${first ? icon + `<span>${label}</span>` : `<span>${label}</span>` + icon}
      </button>`;
    const items = pageItems(cur, pages).map((n) => `<button type="button" class="pager__btn${n === cur ? " current" : ""}" data-action="page" data-page="${n}" aria-label="Page ${n}"${n === cur ? ' aria-current="page"' : ""}>${n}</button>`).join("");
    return `
      <div class="table-foot table-foot--${pos}" data-pos="${pos}">
        <div class="table-foot__left">
          <span>Showing <strong>${from + 1}–${from + shown}</strong> of <strong>${total}</strong></span>
          <div class="rows-select"><span>Rows per page</span>
            ${dropdown({ id: "size-" + pos, variant: "sm", up: pos === "bottom", value: S.pageSize, aria: "Rows per page", options: [5, 10, 20].map((n) => ({ value: n, label: String(n) })) })}
          </div>
        </div>
        <nav class="pager" aria-label="Pagination">
          ${nav("First", 1, ic("chevronsLeft"), cur === 1, true)}
          ${nav("Previous", cur - 1, ic("arrowLeft"), cur === 1, true)}
          ${items}
          ${nav("Next", cur + 1, ic("chevronRight"), cur === pages, false)}
          ${nav("Last", pages, ic("chevronsRight"), cur === pages, false)}
        </nav>
      </div>`;
  }

  function residentsScreen(state) {
    const list = D.residents.filter(
      (p) => (S.wards.length === 0 || S.wards.includes(p.ward)) && p.zone === S.zone && p.name.toLowerCase().includes(S.search.toLowerCase())
    );
    const forced = stateBlock(state, "No residents to show.");
    // Pagination: slice the filtered list; clamp the page if filters shrank the list.
    const size = Number(S.pageSize) || 10;
    const pages = Math.max(1, Math.ceil(list.length / size));
    S.page = Math.min(Math.max(1, S.page), pages);
    // phones (CMP-10, FND-16): no page buttons; "Load more" adds the next page below the rows already shown
    const phone = isPhone();
    const from = phone ? 0 : (S.page - 1) * size;
    const pageRows = list.slice(from, phone ? S.page * size : from + size);
    const loadMore = `<div class="load-more"><span class="load-more__count" role="status">Showing <strong>1–${pageRows.length}</strong> of <strong>${list.length}</strong></span>${pageRows.length < list.length ? `<button type="button" class="secondary-btn" data-action="load-more">Load more</button>` : ""}</div>`;
    const rows = pageRows.map((p) => `
      <button class="resident-row resident-cols" data-action="resident" data-id="${p.id}">
        <span class="resident__who">
          <span class="resident__avatar" style="background-color:var(--avatar-tint-${p.tint})">${p.initials}</span>
          <span><strong class="resident__name">${esc(p.name)}</strong><small class="resident__meta">${p.id} · ${p.age} yrs · ${p.sex}</small></span>
        </span>
        <span class="resident__area"><strong>${p.ward}</strong><small>${p.zone}</small></span>
        <span class="resident__room">${ic("bed", 17)}${p.room} / ${p.bed}</span>
        <span class="resident__readings${p.device === "Not started" ? " none" : ""}"><i></i>${p.device}</span>
        <span class="resident__start">${ic("chevronRight", 18)}<span class="sr-only">Start reading session for ${esc(p.name)}</span></span>
      </button>`).join("");
    const body = `
      ${header("Resident readings", "Find a resident and capture multiple device measurements",
        `<div class="header-actions">${gatewayPill}<button class="icon-button" aria-label="Network">${ic("wifi")}</button></div>`)}
      <div class="content-scroll">
        <div class="section-head">
          <div><h2>Start a resident reading session</h2><p>Search by name or location, then capture all available device readings in one session.</p></div>
          <div class="count"><strong>${forced ? 0 : D.residents.filter((p) => p.zone === S.zone).length}</strong><span>Total residents</span></div>
        </div>
        <div class="filters-zone">
          ${dropdown({ id: "zone", variant: "field", prefix: "Zone:", value: S.zone, aria: "Assigned zone", footer: "Available zones are set by your access role.", options: D.zones.map((z) => ({ value: z, label: z })) })}
        </div>
        <div class="zone-note">${ic("bed", 14)} Showing residents in <strong>${S.zone}</strong> based on your assigned access.</div>
        <div class="filters">
          <div class="search-wrap">${ic("search", 18)}
            <label class="sr-only" for="search">Search residents</label>
            <input id="search" class="filter-field" data-bind="search" value="${esc(S.search)}" placeholder="Search resident name..." autocomplete="off" />
            ${S.search ? `<button type="button" class="search__clear" data-action="search-clear" aria-label="Clear search">${ic("close")}</button>` : ""}</div>
          ${careAreaFilter()}
          <button type="button" class="secondary-btn filters__open" data-action="filters-open" aria-haspopup="dialog">${ic("filter", 16)}Filters${S.wards.length ? `<span class="filters__count">${S.wards.length}</span>` : ""}</button>
          <button type="button" class="filters__clear" data-action="filters-clear" aria-label="Clear all filters" title="Clear all filters"${S.search.trim() || S.wards.length ? "" : " disabled"}>${ic("filterOff")}</button>
        </div>
        <div class="table-card">
          ${forced || !list.length || phone ? "" : paginationBar(list.length, from, pageRows.length, pages, "top")}
          <div class="table-head resident-cols"><span>Resident</span><span>Care area</span><span>Suite / Room</span><span>Today’s readings</span><span></span></div>
          ${forced || rows || '<div class="empty-note">No residents match these filters.</div>'}
          ${forced || !list.length ? "" : phone ? loadMore : paginationBar(list.length, from, pageRows.length, pages, "bottom")}
        </div>
      </div>`;
    return shell("residents", body, S.filterSheet ? filterSheet() : "");
  }

  // Filters sheet (phones, FND-16): zone and care area as plain choice lists in a bottom sheet
  function filterSheet() {
    const matching = D.residents.filter((p) => (S.wards.length === 0 || S.wards.includes(p.ward)) && p.zone === S.zone && p.name.toLowerCase().includes(S.search.toLowerCase())).length;
    const choice = (role, checked, action, value, label) =>
      `<button type="button" class="choice" role="${role}" aria-checked="${checked}" data-action="${action}" data-value="${esc(value)}"><span class="choice__mark" aria-hidden="true">${role === "checkbox" && checked ? ic("check", 12) : ""}</span>${esc(label)}</button>`;
    return `
      <div class="modal-backdrop"><div class="modal-card modal-card--wide" role="dialog" aria-modal="true" aria-labelledby="fs-title">
        <h2 id="fs-title">Filters</h2>
        <fieldset class="choice-group" role="radiogroup" aria-label="Zone"><legend>Zone</legend>
          ${D.zones.map((z) => choice("radio", z === S.zone, "sheet-zone", z, z)).join("")}</fieldset>
        <p>Available zones are set by your access role.</p>
        <fieldset class="choice-group"><legend>Care area</legend>
          ${[...new Set(D.residents.map((p) => p.ward))].map((w) => choice("checkbox", S.wards.includes(w), "sheet-ward", w, w)).join("")}</fieldset>
        <div class="sheet-actions">
          <button type="button" class="secondary-btn" data-action="sheet-clear">Clear all</button>
          <button type="button" class="primary-btn" data-action="filters-cancel" data-autofocus>Show ${matching} resident${matching === 1 ? "" : "s"}</button>
        </div>
      </div></div>`;
  }

  function readingsScreen(id) {
    const r = residentById(id);
    if (!r) return shell("residents", header("Resident readings", "Resident not found") + `<div class="content-scroll"><div class="state">No resident with ID ${esc(id)}. <a href="#/residents">Back to residents</a></div></div>`);
    const count = S.readings.filter((x) => x.status === "captured").length;
    const cards = S.readings.map((x) => {
      const cap = x.status === "captured";
      let value;
      if (cap) {
        const pressure = x.id === "pressure";
        value = `<div class="reading-value__row"><div>
            <span class="reading-value__num">${esc(x.value)}</span>
            ${pressure && x.secondary ? `<span class="reading-value__slash">/</span><span class="reading-value__num">${esc(x.secondary)}</span>` : ""}
            <span class="reading-value__unit">${x.unit}</span></div>
            ${!pressure && x.secondary ? `<span class="reading-value__note">${esc(x.secondary)}</span>` : ""}</div>`;
      } else {
        value = `<div class="reading-value__empty">${x.status === "capturing" ? "Waiting for device reading…" : "No reading captured yet"}</div>`;
      }
      return `
        <article class="reading-card${cap ? " captured" : ""}">
          <div class="reading-card__top">
            <div class="reading-card__id">
              <div class="reading-icon${cap ? " captured" : ""}">${ic(deviceTypeIcon(x.label), 21)}</div>
              <div><h3>${x.label}</h3><p>${x.detail}</p></div>
            </div>
            <span class="reading-status ${x.status}"><span></span>${cap ? "Captured" : x.status === "capturing" ? "Connecting…" : "Ready"}</span>
          </div>
          <div class="reading-value">${value}</div>
          <div class="reading-card__foot">
            <div class="reading-source">${ic("bluetooth", 13)}${x.source}</div>
            <button class="capture-btn" data-action="capture" data-id="${x.id}"${x.status === "capturing" ? " disabled" : ""}>${cap ? "Retake" : "Capture reading"}</button>
          </div>
        </article>`;
    }).join("");
    const body = `
      ${header("Resident readings", "Capture readings from paired Rossmax devices", `<span class="status-pill"><span></span> ${count} of ${S.readings.length} captured</span>`)}
      <div class="content-scroll"><div class="reading-wrap">
        <button class="back-btn" data-action="nav" data-to="residents">${ic("arrowLeft", 16)}Back to residents</button>
        <div class="card resident-card">
          <div class="resident-card__who">
            <div class="resident-card__avatar">${initialsOf(r.name)}</div>
            <div><div class="resident-card__name">${esc(r.name)}</div><div class="resident-card__meta">${r.id} · ${r.ward} · Suite ${r.room} / Room ${r.bed}</div></div>
          </div>
          <div class="resident-card__session"><small>Reading session</small><strong>Started <time datetime="${isoFull(S.sessionStart)}">${isoLocal(S.sessionStart)}</time></strong></div>
        </div>
        <div class="section-head section-head--tight reading-head">
          <div><h2>Capture measurements</h2><p>Take multiple readings for this resident using devices already paired to the gateway.</p></div>
          <button class="secondary-btn" data-action="capture-all"${count === S.readings.length ? " disabled" : ""}>${ic("bluetooth", 16)}Capture remaining</button>
        </div>
        <div class="reading-grid">${cards}</div>
        <div class="save-bar">
          <div class="save-bar__info"><div class="save-bar__check">${ic("check", 18)}</div>
            <div><strong>${count} readings ready</strong><small>Review measurements before sending to the resident record.</small></div></div>
          <button class="primary-btn min-160" data-action="save-readings"${count === 0 ? " disabled" : ""}>Save to resident record</button>
        </div>
      </div></div>`;
    return shell("residents", body, S.saved ? toastHtml(`${count} readings saved to ${r.name}`) : "");
  }

  function devicesScreen(state) {
    const forced = stateBlock(state, "No devices paired to this gateway.");
    const cards = S.devices.map((d) => `
      <article class="device-card">
        <div class="device-card__top">
          <div class="device-card__icon">${ic(deviceTypeIcon(d.type), 23)}</div>
          <span class="device-status${d.connected ? " connected" : ""}"><span></span>${d.connected ? "Connected" : "Offline"}</span>
        </div>
        <h3 class="truncate">${esc(d.name)}</h3>
        <p class="device-card__type">${d.type}</p>
        <div class="device-card__facts">
          <div><span>Model</span><strong>${d.model}</strong></div>
          <div><span>Serial number</span><strong>${d.serial}</strong></div>
          <div><span>Last sync</span><strong>${timeHtml(syncedAt(d.syncedMinAgo))}</strong></div>
        </div>
        <div class="battery"><span>Battery</span><span class="battery__right"><span class="battery__bar"><i style="width:${d.battery}%"></i></span><strong>${d.battery}%</strong></span></div>
        <div class="device-card__actions">
          <button class="device-action grow" data-action="unpair" data-id="${d.id}">${ic("unlink", 15)}Unpair</button>
          <button class="device-action danger" aria-label="Delete ${esc(d.name)}" data-action="remove" data-id="${d.id}">${ic("trash", 16)}</button>
        </div>
      </article>`).join("");
    const body = `
      ${header("Paired devices", "Configure Rossmax devices for this gateway", gatewayPill)}
      <div class="content-scroll">
        <div class="banner"><div class="banner__icon">${ic("check", 18)}</div>
          <div><strong>One-time device setup</strong><small>Paired devices work for every resident. No assignment needed.</small></div></div>
        <div class="device-top">
          <div class="scan-card">
            <div class="scan-card__id">
              <div class="scan-card__icon${S.scanning ? " scanning" : ""}">${ic("bluetooth", 25)}</div>
              <div><h2>${S.scanning ? "Scanning nearby devices…" : "Pair a new device"}</h2><p>Power on the device first.</p></div>
            </div>
            <button class="scan-btn" data-action="scan" aria-label="${S.scanning ? "Scanning nearby devices" : "Scan for devices"}" title="${S.scanning ? "Scanning nearby devices…" : "Scan for devices"}"${S.scanning ? " disabled" : ""}>${ic("plus", 22)}</button>
          </div>
          <div class="discover">
            <div><strong>Device discoverability</strong><small>${S.discoverable ? "Visible to nearby Rossmax devices" : "Device visibility is turned off"}</small></div>
            <button class="toggle${S.discoverable ? " on" : ""}" data-action="discoverable" role="switch" aria-checked="${S.discoverable}" aria-label="Device discoverability"><span></span></button>
          </div>
        </div>
        <div class="devices-head">
          <div><h2>Paired devices</h2><p>${S.devices.length} devices paired to this gateway</p></div>
        </div>
        <div class="device-grid">${forced ? `<div class="devices-empty">${forced}</div>` : cards || '<div class="devices-empty">No devices paired to this gateway.</div>'}</div>
      </div>`;
    const dd = S.danger && S.devices.find((d) => d.id === S.danger.id);
    const dangerModal = dd ? (S.danger.kind === "remove" ? {
      title: `Delete ${dd.name}?`, text: "The device is removed from this gateway and its pairing is lost. Readings already saved are kept. To use it again, pair it as a new device.", ok: "Delete device", icon: "trash" } : {
      title: `Unpair ${dd.name}?`, text: "The device stops sending readings to this gateway until it is paired again. Readings already saved are kept.", ok: "Unpair device", icon: "unlink" }) : null;
    const overlay = dangerModal ? `
      <div class="modal-backdrop"><div class="modal-card modal-card--wide" role="alertdialog" aria-modal="true" aria-labelledby="m3" aria-describedby="m3d">
        <div class="modal-icon modal-icon--danger">${ic(dangerModal.icon, 21)}</div>
        <h2 id="m3">${esc(dangerModal.title)}</h2>
        <p id="m3d">${dangerModal.text}</p>
        <div class="modal-actions modal-actions--end">
          <button class="secondary-btn" data-action="danger-cancel" data-autofocus>Cancel</button>
          <button class="danger-btn" data-action="danger-ok">${dangerModal.ok}</button>
        </div></div></div>` : "";
    return shell("devices", body, overlay);
  }

  function settingsScreen() {
    const off = S.unlocked ? "" : " disabled";
    const unlockModal = S.unlockOpen ? `
      <div class="modal-backdrop"><div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="m1">
        <div class="modal-icon">${ic("shield", 23)}</div>
        <h2 id="m1">Administrator authorization</h2>
        <p>Enter your administrator PIN to unlock server configuration for this session.</p>
        <label class="modal-label"><span class="label">Administrator PIN</span>
          <input class="field pin-field" type="password" inputmode="numeric" placeholder="••••••" data-bind="pin" data-autofocus value="${esc(S.pin)}" /></label>
        <div class="modal-actions">
          <button class="secondary-btn" data-action="unlock-cancel">Cancel</button>
          <button class="primary-btn" data-action="unlock-ok"${S.pin.length < 4 ? " disabled" : ""}>Authorize</button>
        </div></div></div>` : "";
    const confirmModal = S.confirmOpen ? `
      <div class="modal-backdrop"><div class="modal-card modal-card--wide" role="dialog" aria-modal="true" aria-labelledby="m2">
        <div class="modal-icon modal-icon--warn">${ic("wifi", 21)}</div>
        <h2 id="m2">Apply server changes?</h2>
        <p>Changing this configuration will briefly interrupt device synchronization. The current configuration will remain active if the new connection fails.</p>
        <div class="verified">${ic("check", 15)}New connection successfully verified</div>
        <div class="modal-actions modal-actions--end">
          <button class="secondary-btn" data-action="confirm-cancel" data-autofocus>Keep current settings</button>
          <button class="primary-btn" data-action="confirm-ok">Apply changes</button>
        </div></div></div>` : "";
    const foot = S.unlocked ? `
      <div class="left">
        <button type="button" class="secondary-btn" data-action="cfg-cancel">Cancel</button>
        <button type="button" class="secondary-btn" data-action="cfg-test">${S.testing ? "Testing connection…" : S.tested ? "Connection verified" : "Test connection"}</button>
      </div>
      <button type="submit" class="primary-btn min-150"${S.tested ? "" : " disabled"}>Save changes</button>`
      : `<div class="protected">${ic("shield", 15)}Protected system configuration</div>
         <button type="button" class="secondary-btn" data-action="unlock-open">${ic("lock", 15)}Unlock configuration</button>`;
    const body = `
      ${header("Gateway status", "System connection and configuration", gatewayPill)}
      <div class="content-scroll"><div class="settings-wrap">
        <div class="section-head"><h2>System connection</h2><p>Connection details are protected to prevent service interruption.</p></div>
        <form class="settings-card" id="cfg-form">
          <div class="settings-card__body">
            <div class="settings-card__head">
              <div class="settings-card__icon">${ic("wifi", 22)}</div>
              <div><h3>Community server</h3><p>Used to securely transmit resident readings.</p></div>
              <span class="status-pill"><span></span> Connection healthy</span>
            </div>
            ${S.unlocked ? "" : `<div class="locked-note"><div class="locked-note__icon">${ic("lock", 16)}</div>
              <div><strong>Configuration locked</strong><small>Only authorized administrators can change server details.</small></div></div>`}
            <div class="settings-grid">
              <label><span class="label">Server host</span><input class="field" data-bind="cfg.host" value="${esc(S.cfg.host)}"${off} /></label>
              <label><span class="label">Server port</span><input class="field" inputmode="numeric" data-bind="cfg.port" value="${esc(S.cfg.port)}"${off} /></label>
            </div>
            <label class="settings-token"><span class="label">Access token</span>
              <div class="pw-wrap">
                <input class="field field--mono" type="${S.showToken ? "text" : "password"}" data-bind="cfg.token" value="${esc(S.cfg.token)}"${off} />
                <button type="button" class="pw-toggle" data-action="token-eye" aria-label="${S.showToken ? "Hide" : "Show"} access token"${off}>${ic(S.showToken ? "eyeOff" : "eye")}</button>
              </div>
              <span class="settings-hint">Tokens are encrypted and stored securely on this gateway.</span></label>
          </div>
          <div class="settings-card__foot">${foot}</div>
        </form>
        <div class="gateway-card"><h3>Gateway information</h3>
          <div class="gateway-stats">
            <div><small>Gateway ID</small><strong>${D.gateway.id}</strong></div>
            <div><small>App version</small><strong>${D.gateway.version}</strong></div>
            <div><small>Last sync</small><strong>${timeHtml(syncedAt(D.gateway.syncedMinAgo))}</strong></div>
          </div></div>
        <p class="settings-note">Configuration changes are logged with administrator identity and timestamp.</p>
      </div></div>`;
    return shell("settings", body, unlockModal + confirmModal + (S.cfgSaved ? toastHtml("Configuration updated and locked") : ""));
  }

  // ---------- render ----------
  // The HTML of the current screen (render() puts it on the page; the partial updates below take pieces from it).
  function screenHtml() {
    const { parts, state } = parseRoute();
    let route = parts[0] || "residents";
    if (route !== "login" && !isLoggedIn()) route = "login";
    if (route === "login" && isLoggedIn()) route = "residents";
    let html, title;
    if (route === "login") { html = loginScreen(); title = "Sign in"; }
    else if (route === "devices") { html = devicesScreen(state); title = "Paired devices"; }
    else if (route === "settings") { html = settingsScreen(); title = "Gateway status"; }
    else if (route === "residents" && parts[1]) {
      if (S.readingsFor !== parts[1]) { S.readingsFor = parts[1]; S.readings = D.readings.map((r) => ({ ...r })); S.sessionStart = new Date(); }   // a new session starts now (CNT-2)
      html = readingsScreen(parts[1]); title = "Resident readings";
    } else { html = residentsScreen(state); title = "Resident readings"; }
    return { html, title, route, parts };
  }

  // Focus a freshly drawn control without animating its focus ring in (the ring would otherwise flash on every redraw).
  function focusQuiet(el, opts) {
    el.style.transition = "none";
    el.focus(opts);
    void el.offsetWidth;   // apply the focused style at once
    setTimeout(() => { el.style.transition = ""; }, 50);   // after the focused style has been painted
  }

  // Partial updates: change only what changed, so the field being typed in, an open sheet or an open panel is not rebuilt.
  const fromHtml = (html) => { const t = document.createElement("template"); t.innerHTML = html; return t.content; };
  function refreshResidents() {
    const next = fromHtml(screenHtml().html);
    for (const sel of [".table-card", ".count", ".filters__clear", ".filters__open", ".zone-note"]) {
      const old = app.querySelector(sel), neu = next.querySelector(sel);
      if (old && neu) old.replaceWith(neu);
    }
    const ms = app.querySelector('[data-dd="ward"]'), msNew = next.querySelector('[data-dd="ward"]');
    if (ms && msNew && !ms.classList.contains("open")) ms.replaceWith(msNew);
    const wrap = app.querySelector(".search-wrap"), x = wrap && wrap.querySelector(".search__clear"), xNew = next.querySelector(".search-wrap .search__clear");
    if (x && !xNew) x.remove(); else if (wrap && !x && xNew) wrap.append(xNew);   // the clear (x) button comes and goes; the field stays
  }
  function refreshWardList() {
    const old = app.querySelector('[data-dd="ward"] .ms__list'), neu = fromHtml(screenHtml().html).querySelector('[data-dd="ward"] .ms__list');
    if (old && neu) old.replaceWith(neu);
  }
  function refreshSheet(focusSel) {
    const card = app.querySelector(".modal-card"), neu = fromHtml(filterSheet()).querySelector(".modal-card");
    if (!card || !neu) return render();
    card.innerHTML = neu.innerHTML;   // the sheet stays open: no slide-in again
    refreshResidents();
    const el = focusSel && card.querySelector(focusSel);
    if (el) focusQuiet(el, { preventScroll: true });
  }

  function render() {
    const { html, title, route, parts } = screenHtml();

    const active = document.activeElement;
    const bind = active && active.dataset ? active.dataset.bind : null;
    const bindPos = active && active.dataset ? active.dataset.pos : null;
    let caret = null;
    try { caret = bind ? [active.selectionStart, active.selectionEnd] : null; } catch (e) { /* type=email has no selection */ }

    // Re-rendering the same screen (staff menu, toasts, search, paging...) must not throw the user back to the top:
    // remember the content scroll position and restore it. A different screen starts at the top.
    const viewKey = route + "/" + (route === "residents" && parts[1] ? parts[1] : "");
    const prevScroller = S.viewKey === viewKey ? app.querySelector(".content-scroll") : null;
    const scrollTop = prevScroller ? prevScroller.scrollTop : 0;
    const msTop = (app.querySelector(".ms__list") || {}).scrollTop || 0;
    app.innerHTML = html;
    S.viewKey = viewKey;
    if (msTop) { const l = app.querySelector(".ms__list"); if (l) l.scrollTop = msTop; }
    if (scrollTop) {
      const sc = app.querySelector(".content-scroll");
      if (sc) sc.scrollTop = scrollTop;
    }
    if (S.refocusPager) {
      const cur = app.querySelector(`.table-foot[data-pos="${S.refocusPager}"] .pager__btn.current`);
      S.refocusPager = false;
      if (cur) focusQuiet(cur, { preventScroll: true });
    }
    let refocused = false;   // an explicit focus request (S.refocus) beats the generic restore below
    if (S.refocus) {
      const el = app.querySelector(S.refocus);
      S.refocus = null;
      if (el) { focusQuiet(el, { preventScroll: true }); refocused = true; }
    }
    document.title = title + " · Rossmax Connect";

    if (refocused) return;
    if (bind) {
      const el = app.querySelector(bindPos ? `[data-bind="${bind}"][data-pos="${bindPos}"]` : `[data-bind="${bind}"]`);
      if (el && !el.disabled) { focusQuiet(el); try { if (caret && caret[0] != null) el.setSelectionRange(caret[0], caret[1]); } catch (e) { /* ignore */ } }
    } else {
      const af = app.querySelector("[data-autofocus]");
      if (af) focusQuiet(af);
    }
  }

  // ---------- readings logic ----------
  function capture(id) {
    S.readings = S.readings.map((r) => (r.id === id ? { ...r, status: "capturing" } : r));
    render();
    setTimeout(() => {
      S.readings = S.readings.map((r) => (r.id === id ? { ...r, ...D.captureValues[id], status: "captured" } : r));
      render();
    }, 1100);
  }

  // ---------- events ----------
  const go = (hash) => { location.hash = hash; };
  const actions = {
    nav: (el) => { S.profileOpen = false; const to = el.dataset.to; if (location.hash === "#/" + to) render(); else go("#/" + to); },
    page: (el) => { S.page = Number(el.dataset.page); S.refocusPager = (el.closest(".table-foot") || {dataset: {}}).dataset.pos || "bottom"; render(); },
    "ward-open": () => { S.openDd = S.openDd === "ward" ? null : "ward"; S.wardQuery = ""; S.refocus = S.openDd ? ".ms__search-input" : ".ms__trigger"; render(); },
    "dd-open": (el) => {
      const id = el.dataset.dd;
      S.openDd = S.openDd === id ? null : id; S.wardQuery = "";
      S.refocus = S.openDd ? `.dd[data-dd="${id}"] .dd__option.selected` : `.dd[data-dd="${id}"] .dd__trigger`;
      render();
    },
    "dd-pick": (el) => {
      const id = el.dataset.dd, v = el.dataset.value;
      S.openDd = null; S.refocus = `.dd[data-dd="${id}"] .dd__trigger`;
      if (id === "zone") { S.zone = v; S.page = 1; render(); }
      else if (id.startsWith("size-")) { S.pageSize = Number(v); S.page = 1; render(); }
    },
    "ward-toggle": (el) => {
      const v = el.dataset.value;
      S.wards = S.wards.includes(v) ? S.wards.filter((w) => w !== v) : [...S.wards, v];
      S.page = 1; S.refocus = `.ms__option[data-value="${v.replace(/["\\]/g, "\\$&")}"]`; render();
    },
    "search-clear": () => { S.search = ""; S.page = 1; S.refocus = "#search"; render(); },
    "filters-open": () => { S.filterSheet = true; render(); },
    "filters-cancel": () => { S.filterSheet = false; S.refocus = ".filters__open"; render(); },
    "sheet-zone": (el) => { const v = el.dataset.value; S.zone = v; S.page = 1; refreshSheet(`.choice[data-value="${v}"]`); },
    "sheet-ward": (el) => { const v = el.dataset.value; S.wards = S.wards.includes(v) ? S.wards.filter((w) => w !== v) : [...S.wards, v]; S.page = 1; refreshSheet(`.choice[data-value="${v}"]`); },
    "sheet-clear": () => { S.wards = []; S.page = 1; refreshSheet('[data-action="sheet-clear"]'); },
    "load-more": () => { S.page += 1; S.refocus = ".load-more .secondary-btn, .load-more__count"; render(); },
    "filters-clear": () => { S.search = ""; S.wards = []; S.wardQuery = ""; S.openDd = null; S.page = 1; S.refocus = "#search"; render(); },
    "ward-clear": () => { S.wards = []; S.page = 1; S.refocus = ".ms__trigger"; render(); },
    "nav-toggle": () => {
      S.navExpanded = !S.navExpanded;
      try { localStorage.setItem(NAV_KEY, S.navExpanded ? "1" : "0"); } catch (e) { /* storage blocked */ }
      syncNav();
    },
    profile: () => { S.profileOpen = !S.profileOpen; render(); },
    logout: () => { localStorage.removeItem(SESSION_KEY); S.profileOpen = false; if (location.hash === "#/login") render(); else go("#/login"); },
    pw: () => { S.pwVisible = !S.pwVisible; render(); },
    remember: () => { S.remember = !S.remember; render(); },
    reload: () => location.reload(),
    resident: (el) => go("#/residents/" + el.dataset.id),
    capture: (el) => capture(el.dataset.id),
    "capture-all": () => S.readings.filter((r) => r.status !== "captured").forEach((r, i) => setTimeout(() => capture(r.id), i * 180)),
    "save-readings": () => { S.saved = true; render(); armToast(() => { S.saved = false; }); },
    scan: () => { S.scanning = true; render(); setTimeout(() => { S.scanning = false; notify("Scan complete · 1 nearby device found"); }, 1800); },
    discoverable: () => { S.discoverable = !S.discoverable; render(); },
    // destructive actions always ask first (CMP-21); the dialog opens with focus on Cancel
    unpair: (el) => { S.danger = { kind: "unpair", id: +el.dataset.id }; render(); },
    remove: (el) => { S.danger = { kind: "remove", id: +el.dataset.id }; render(); },
    "danger-cancel": () => { const d = S.danger; S.danger = null; S.refocus = `[data-action="${d.kind}"][data-id="${d.id}"]`; render(); },
    "danger-ok": () => {
      const { kind, id } = S.danger;
      S.danger = null;
      if (kind === "unpair") { S.devices = S.devices.map((d) => (d.id === id ? { ...d, connected: false } : d)); S.refocus = `[data-action="unpair"][data-id="${id}"]`; notify("Device unpaired"); }
      else { S.devices = S.devices.filter((d) => d.id !== id); S.refocus = ".device-action"; notify("Device removed"); }
    },
    "unlock-open": () => { S.unlockOpen = true; render(); },
    "unlock-cancel": () => { S.unlockOpen = false; S.pin = ""; render(); },
    "unlock-ok": () => { S.unlocked = true; S.unlockOpen = false; S.pin = ""; render(); },
    "token-eye": () => { S.showToken = !S.showToken; render(); },
    "cfg-cancel": () => { S.unlocked = false; S.tested = false; render(); },
    "cfg-test": () => { S.testing = true; render(); setTimeout(() => { S.testing = false; S.tested = true; render(); }, 1200); },
    "confirm-cancel": () => { S.confirmOpen = false; render(); },
    "confirm-ok": () => { S.confirmOpen = false; S.unlocked = false; S.tested = false; S.cfgSaved = true; render(); setTimeout(() => { S.cfgSaved = false; render(); }, 2600); },
  };

  // ---------- sidebar (CMP-11) ----------
  // Touch: the toggle button expands and collapses it (and the choice is remembered).
  // Mouse: it rests as the icon rail and opens over the page while the pointer rests on it or keyboard focus is inside it.
  // A device with both gets both: hovering opens it, and the toggle pins it open.
  const syncNav = () => {
    const sh = app.querySelector(".app-shell");
    if (!sh) return;
    sh.classList.toggle("nav-expanded", navOpen());
    sh.classList.toggle("nav-auto", navAuto());
    const tg = sh.querySelector(".sidebar__toggle");
    if (tg) {
      const label = S.navExpanded ? "Collapse navigation" : "Expand navigation";
      tg.setAttribute("aria-expanded", String(S.navExpanded)); tg.setAttribute("aria-label", label); tg.title = label;
      tg.innerHTML = navToggleHtml();
    }
  };
  let peekTimer;
  const cssMs = (name, fallback) => parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name)) || fallback;
  const setPeek = (on, delay) => {
    clearTimeout(peekTimer);
    peekTimer = setTimeout(() => { if (S.navPeek !== on) { S.navPeek = on; syncNav(); } }, delay);
  };
  app.addEventListener("pointerover", (e) => {
    const sb = e.target.closest(".sidebar");
    if (e.pointerType === "mouse" && navAuto() && sb && !sb.contains(e.relatedTarget)) setPeek(true, cssMs("--nav-hover-open-delay", 150));
  });
  app.addEventListener("pointerout", (e) => {
    const sb = e.target.closest(".sidebar");
    if (e.pointerType !== "mouse" || !navAuto() || !sb || sb.contains(e.relatedTarget)) return;
    const ae = document.activeElement;
    if (S.profileOpen || (ae && sb.contains(ae) && ae.matches(":focus-visible"))) { clearTimeout(peekTimer); return; }   // keyboard focus or the open staff menu keeps it open
    setPeek(false, cssMs("--nav-hover-close-delay", 300));
  });
  app.addEventListener("focusin", (e) => {
    if (navAuto() && e.target.closest(".sidebar") && e.target.matches(":focus-visible")) setPeek(true, 0);
  });
  app.addEventListener("focusout", (e) => {
    const sb = e.target.closest(".sidebar");
    if (navAuto() && sb && e.relatedTarget && !sb.contains(e.relatedTarget) && !sb.matches(":hover")) setPeek(false, 0);
  });
  [hoverMQ, touchMQ, phoneMQ].forEach((mq) => mq.addEventListener("change", () => { S.navPeek = false; render(); }));   // a mouse or touch screen was connected or removed
  const closeDd = (refocus) => {
    const id = S.openDd; S.openDd = null; S.wardQuery = "";
    if (refocus && id) S.refocus = `[data-dd="${id}"] .ms__trigger, [data-dd="${id}"] .dd__trigger`;
    render();
  };
  app.addEventListener("click", (e) => {
    const el = e.target.closest("[data-action]");
    const outside = S.openDd && !e.target.closest(`[data-dd="${S.openDd}"]`);   // a click anywhere else closes the open panel
    if (outside) { S.openDd = null; S.wardQuery = ""; }
    const outsideProfile = S.profileOpen && !e.target.closest(".sidebar__foot");   // ...and the staff menu
    if (outsideProfile) S.profileOpen = false;
    if (el && actions[el.dataset.action] && !el.disabled) actions[el.dataset.action](el);
    else if (outside || outsideProfile) render();
  });
  document.addEventListener("keydown", (e) => {
    const ae = document.activeElement;
    // every dialog: Escape cancels and Tab stays inside (CMP-16, ACC-10)
    const modal = app.querySelector(".modal-card");
    if (modal) {
      if (e.key === "Escape") { e.preventDefault(); const c = modal.querySelector('[data-action$="-cancel"]'); if (c) c.click(); return; }
      if (e.key === "Tab") {
        const f = [...modal.querySelectorAll('button:not([disabled]), input:not([disabled]), select, textarea, a[href], [tabindex]:not([tabindex="-1"])')];
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (!modal.contains(ae)) { e.preventDefault(); first.focus(); }
        else if (e.shiftKey && ae === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && ae === last) { e.preventDefault(); first.focus(); }
      }
      return;
    }
    if (e.key === "Escape" && S.profileOpen) { e.preventDefault(); S.profileOpen = false; S.refocus = ".profile"; render(); return; }
    if (e.key === "Escape" && navAuto() && S.navPeek) { e.preventDefault(); setPeek(false, 0); return; }   // hover content can be dismissed without moving the pointer (WCAG 1.4.13)
    if (!S.openDd) {   // ArrowDown on a closed dropdown opens it
      if (e.key === "ArrowDown" && ae && ae.classList && ae.classList.contains("dd__trigger")) { e.preventDefault(); ae.click(); }
      return;
    }
    if (e.key === "Escape") { e.preventDefault(); closeDd(true); return; }
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      const scope = `[data-dd="${S.openDd}"]`;
      const items = [...app.querySelectorAll(`${scope} .ms__search-input, ${scope} .ms__option, ${scope} .dd__option`)];
      const i = items.indexOf(ae);
      if (i === -1) return;
      e.preventDefault();
      const next = items[Math.min(items.length - 1, Math.max(0, i + (e.key === "ArrowDown" ? 1 : -1)))];
      if (next) next.focus();
    }
  });
  app.addEventListener("focusout", (e) => {   // tabbing out of an open panel closes it
    if (S.openDd && e.relatedTarget && !e.relatedTarget.closest(`[data-dd="${S.openDd}"]`)) closeDd(false);
  });
  app.addEventListener("input", (e) => {
    const key = e.target.dataset && e.target.dataset.bind;
    if (!key) return;
    if (key.startsWith("cfg.")) S.cfg[key.slice(4)] = e.target.value;
    else S[key] = e.target.value;
    if (LOGIN_RULES[key] && S.loginErr[key] && !LOGIN_RULES[key](S[key])) { S.loginErr[key] = ""; showLoginErr(key); }   // fixed: clear at once
    if (key === "search") { S.page = 1; refreshResidents(); }
    if (key === "wardQuery") refreshWardList();
    // PIN: re-rendering would rebuild the modal and replay its fade-in on every keystroke,
    // so only toggle the Authorize button in place.
    if (key === "pin") {
      const ok = app.querySelector('[data-action="unlock-ok"]');
      if (ok) ok.disabled = S.pin.length < 4;
    }
  });
  app.addEventListener("submit", (e) => {
    e.preventDefault();
    if (e.target.id === "login-form") {
      const errs = Object.fromEntries(Object.entries(LOGIN_RULES).map(([k, rule]) => [k, rule(S[k])]));
      S.loginErr = errs;
      Object.keys(errs).forEach(showLoginErr);
      const first = Object.keys(errs).find((k) => errs[k]);
      if (first) { app.querySelector(`#login-${first}`).focus(); return; }   // move focus to the first problem
      localStorage.setItem(SESSION_KEY, "1");
      if (location.hash === "#/residents") render(); else go("#/residents");
    }
    if (e.target.id === "cfg-form" && S.tested) { S.confirmOpen = true; render(); }
  });

  // Documentation states: ?show=nav-open | login-errors | delete | filters | account opens a state that normally needs a click,
  // so it can be captured or linked (like ?state=loading|empty|error for lists).
  const SHOW = new URLSearchParams(location.search).get("show");
  if (SHOW === "nav-open") S.navPeek = true;
  if (SHOW === "login-errors") { S.email = ""; S.password = ""; S.loginErr = { email: LOGIN_RULES.email(""), password: LOGIN_RULES.password("") }; }
  if (SHOW === "delete") S.danger = { kind: "remove", id: 3 };
  if (SHOW === "filters") S.filterSheet = true;
  if (SHOW === "account") S.profileOpen = true;

  window.addEventListener("hashchange", render);
  render();
})();
