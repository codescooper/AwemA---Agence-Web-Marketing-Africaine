/* AwemaGH — GitHub = back-end (ADR-007).
   Permet au navigateur d'ÉCRIRE dans le dépôt de l'utilisateur via l'API REST GitHub,
   puis de déclencher une Action (build + agents). Le résultat est servi par GitHub Pages.

   Auth : un PAT à granularité fine (mono-dépôt, Contents R/W + Actions R/W), saisi UNE fois,
   stocké en localStorage (jamais dans le dépôt). Mode manuel conservé en repli.

   API : AwemaGH.connected() · AwemaGH.openConnect(cb) · AwemaGH.ensure(cb) ·
         AwemaGH.saveFile(path, contenu, message) · AwemaGH.runWorkflow(fichier) ·
         AwemaGH.disconnect() · AwemaGH.who()
*/
window.AwemaGH = (function () {
  var LS = 'awema-gh';
  var API = 'https://api.github.com';
  function cfg() { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { return {}; } }
  function connected() { var c = cfg(); return !!(c.token && c.owner && c.repo); }
  function branch() { return cfg().branch || 'main'; }
  function who() { var c = cfg(); return connected() ? (c.owner + '/' + c.repo + '@' + branch()) : null; }
  function disconnect() { localStorage.removeItem(LS); }
  function b64(s) { return btoa(unescape(encodeURIComponent(s))); }

  function api(path, opts) {
    var c = cfg();
    opts = opts || {};
    return fetch(API + path, Object.assign({}, opts, {
      headers: Object.assign({
        'Authorization': 'Bearer ' + c.token,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
      }, opts.headers || {})
    }));
  }
  async function repoOK() { var c = cfg(); var r = await api('/repos/' + c.owner + '/' + c.repo); return r.ok; }
  async function sha(path) {
    var c = cfg();
    var r = await api('/repos/' + c.owner + '/' + c.repo + '/contents/' + path + '?ref=' + branch());
    if (r.status === 200) { var j = await r.json(); return j.sha; }
    return null;
  }
  // Écrit (ou met à jour) un fichier. contenu = string ou objet (sérialisé en JSON joli).
  async function saveFile(path, contenu, message) {
    var c = cfg();
    if (!connected()) throw new Error('GitHub non connecté');
    var body = (typeof contenu === 'string') ? contenu : JSON.stringify(contenu, null, 2);
    var s = await sha(path);
    var payload = { message: message || ('AWEMA : maj ' + path), content: b64(body), branch: branch() };
    if (s) payload.sha = s;
    var r = await api('/repos/' + c.owner + '/' + c.repo + '/contents/' + path, { method: 'PUT', body: JSON.stringify(payload) });
    if (!r.ok) throw new Error('GitHub ' + r.status + ' — ' + (await r.text()).slice(0, 180));
    return r.json();
  }
  // Déclenche un workflow (ex. 'agents.yml' ou 'build.yml') sur main. Best-effort (non bloquant).
  async function runWorkflow(fichier) {
    var c = cfg();
    try {
      var r = await api('/repos/' + c.owner + '/' + c.repo + '/actions/workflows/' + fichier + '/dispatches',
        { method: 'POST', body: JSON.stringify({ ref: branch() }) });
      return r.ok;
    } catch (e) { return false; }
  }

  // ——— Modale de connexion (une fois) ———
  function injCss() {
    if (document.getElementById('awgh-css')) return;
    var s = document.createElement('style'); s.id = 'awgh-css';
    s.textContent = [
      '.awgh-ov{position:fixed;inset:0;z-index:10000;background:rgba(4,10,26,.72);backdrop-filter:blur(4px);',
      'display:none;align-items:center;justify-content:center;padding:20px}',
      '.awgh-ov.on{display:flex}',
      '.awgh{width:min(460px,100%);background:var(--card,#13234a);border:1px solid var(--bord,rgba(255,255,255,.14));',
      'border-radius:18px;padding:22px;color:var(--tx,#eaf0fb);font-family:Poppins,system-ui,sans-serif;',
      'box-shadow:0 30px 80px -20px rgba(0,0,0,.7)}',
      '.awgh h3{font-family:Montserrat,Poppins,sans-serif;font-size:18px;margin:0 0 4px}',
      '.awgh p{font-size:12.5px;color:var(--muted,#9db0d6);margin:0 0 12px;line-height:1.55}',
      '.awgh label{display:block;font-size:11px;color:var(--muted,#9db0d6);text-transform:uppercase;letter-spacing:.05em;margin:10px 0 4px}',
      '.awgh input{width:100%;padding:10px 12px;border-radius:10px;border:1px solid var(--bord,rgba(255,255,255,.14));',
      'background:rgba(0,0,0,.25);color:#fff;font:inherit;font-size:13.5px}',
      '.awgh .r{display:flex;gap:10px;margin-top:16px}',
      '.awgh button{flex:1;border:none;border-radius:11px;padding:11px;cursor:pointer;font:700 13px Poppins,sans-serif}',
      '.awgh .go{background:linear-gradient(135deg,#4BA3FF,#7C5CFF);color:#fff}',
      '.awgh .x{background:transparent;border:1px solid var(--bord,rgba(255,255,255,.14));color:var(--tx,#eaf0fb)}',
      '.awgh .msg{font-size:12px;margin-top:10px;min-height:16px}',
      '.awgh a{color:#4BA3FF}'
    ].join('');
    document.head.appendChild(s);
  }
  function openConnect(cb) {
    injCss();
    var c = cfg();
    var g = (window.AWEMA_CONFIG && window.AWEMA_CONFIG.github) || {};
    var ov = document.createElement('div'); ov.className = 'awgh-ov on';
    ov.innerHTML =
      '<div class="awgh"><h3>🔗 Connecter GitHub (une seule fois)</h3>' +
      '<p>AWEMA enregistre tes données <b>directement dans ton dépôt</b> et lance le traitement en arrière-plan. ' +
      'Crée un <b>jeton à granularité fine</b> limité à ton dépôt — ' +
      '<a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener">créer le jeton ↗</a><br>' +
      '<small>Permissions : <b>Contents</b> = Read/Write, <b>Actions</b> = Read/Write. Le jeton reste sur ton appareil, jamais dans le dépôt.</small></p>' +
      '<label>Propriétaire (owner)</label><input id="awgh-o" value="' + (c.owner || g.owner || '') + '" placeholder="ton-pseudo">' +
      '<label>Dépôt (repo)</label><input id="awgh-r" value="' + (c.repo || g.repo || '') + '" placeholder="mon-depot">' +
      '<label>Branche (où écrire)</label><input id="awgh-b" value="' + (c.branch || g.branch || 'main') + '" placeholder="main">' +
      '<label>Jeton (token, commence par github_pat_…)</label><input id="awgh-t" type="password" placeholder="github_pat_…">' +
      '<div class="msg" id="awgh-m"></div>' +
      '<div class="r"><button class="x" id="awgh-x">Annuler</button><button class="go" id="awgh-g">Connecter</button></div></div>';
    document.body.appendChild(ov);
    function close() { ov.remove(); }
    ov.querySelector('#awgh-x').onclick = close;
    ov.querySelector('#awgh-g').onclick = async function () {
      var o = ov.querySelector('#awgh-o').value.trim(), r = ov.querySelector('#awgh-r').value.trim(),
          bch = ov.querySelector('#awgh-b').value.trim() || 'main', t = ov.querySelector('#awgh-t').value.trim();
      var m = ov.querySelector('#awgh-m');
      if (!o || !r || !t) { m.style.color = '#FF7D9C'; m.textContent = 'Remplis owner, repo et jeton.'; return; }
      m.style.color = '#9db0d6'; m.textContent = 'Vérification…';
      localStorage.setItem(LS, JSON.stringify({ owner: o, repo: r, branch: bch, token: t }));
      try {
        if (await repoOK()) { m.style.color = '#34E5C4'; m.textContent = '✅ Connecté à ' + o + '/' + r; setTimeout(function () { close(); cb && cb(true); }, 600); }
        else { m.style.color = '#FF7D9C'; m.textContent = '❌ Accès refusé : vérifie le jeton et son dépôt.'; disconnect(); }
      } catch (e) { m.style.color = '#FF7D9C'; m.textContent = '❌ ' + e.message; disconnect(); }
    };
  }
  // Garantit une connexion puis exécute cb (ouvre la modale si besoin).
  function ensure(cb) { if (connected()) cb(true); else openConnect(cb); }

  return { connected: connected, who: who, disconnect: disconnect, openConnect: openConnect, ensure: ensure, saveFile: saveFile, runWorkflow: runWorkflow };
})();
