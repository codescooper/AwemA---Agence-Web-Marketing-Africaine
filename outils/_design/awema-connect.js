/* AwemaConnect — widget « coller un token → Secret GitHub », sans terminal.
   Réutilise AwemaGH (ADR-007/008) : enregistre la valeur en Secret (auto si crypto, sinon guidé),
   et propose un bouton « Synchroniser » qui déclenche un workflow. Aucune commande pour l'utilisateur.

   Usage :
     AwemaConnect.secretBox('#mount', {
       name: 'META_TOKEN',                 // nom du Secret GitHub
       label: 'Token Meta longue durée',   // libellé du champ
       placeholder: 'Colle le token ici',
       sync: 'sync-reseaux.yml',           // (optionnel) workflow à lancer après
       syncLabel: 'Synchroniser les Pages' // (optionnel) libellé du bouton sync
     });
*/
window.AwemaConnect = (function () {
  function css() {
    if (document.getElementById('awc-css')) return;
    var s = document.createElement('style'); s.id = 'awc-css';
    s.textContent = [
      '.awc{background:rgba(52,229,196,.06);border:1px solid rgba(52,229,196,.32);border-radius:14px;padding:16px;margin-top:14px}',
      '.awc .t{font-weight:700;font-size:13.5px;color:var(--tx,#eaf0fb);display:flex;align-items:center;gap:8px}',
      '.awc .row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-top:10px}',
      '.awc input{flex:1;min-width:200px;background:rgba(0,0,0,.28);border:1px solid var(--bord,rgba(255,255,255,.14));',
      'border-radius:11px;color:#fff;font:inherit;font-size:13.5px;padding:10px 12px}',
      '.awc button{border:0;border-radius:11px;padding:10px 15px;cursor:pointer;font:700 13px Poppins,system-ui,sans-serif;color:#fff;',
      'background:linear-gradient(135deg,var(--ciel,#4BA3FF),var(--violet,#7C5CFF))}',
      '.awc button.s{background:linear-gradient(135deg,#34E5C4,#22b89e);color:#06231d}',
      '.awc button:disabled{opacity:.5;cursor:default}',
      '.awc .m{font-size:12.5px;margin-top:9px;min-height:16px;color:var(--muted,#9db0d6)}',
      '.awc .hint{font-size:11.5px;color:var(--muted,#9db0d6);margin-top:6px}'
    ].join('');
    document.head.appendChild(s);
  }

  function secretBox(mountSel, opt) {
    css();
    var host = (typeof mountSel === 'string') ? document.querySelector(mountSel) : mountSel;
    if (!host) return;
    if (!window.AwemaGH) { host.innerHTML = '<div class="awc"><div class="m">Module GitHub indisponible.</div></div>'; return; }
    opt = opt || {};
    var box = document.createElement('div'); box.className = 'awc';
    box.innerHTML =
      '<div class="t">⚡ ' + (opt.title || ('Enregistrer ' + opt.name + ' dans AWEMA')) + ' <span class="hint" style="font-weight:400">— sans terminal</span></div>' +
      '<div class="row">' +
      '<input type="password" autocomplete="off" placeholder="' + (opt.placeholder || ('Colle ' + (opt.label || opt.name) + ' ici')) + '">' +
      '<button class="save">Enregistrer</button>' +
      (opt.sync ? '<button class="s sync" disabled>' + (opt.syncLabel || 'Synchroniser') + '</button>' : '') +
      '</div>' +
      '<div class="m"></div>';
    host.appendChild(box);

    var inp = box.querySelector('input'), bSave = box.querySelector('.save'),
        bSync = box.querySelector('.sync'), m = box.querySelector('.m');
    function msg(t, c) { m.textContent = t; m.style.color = c || 'var(--muted,#9db0d6)'; }

    bSave.onclick = function () {
      var v = inp.value.trim();
      if (!v) { msg('Colle d’abord la valeur.', '#FF7D9C'); return; }
      msg('Connexion à GitHub…');
      AwemaGH.ensure(function () {
        msg('Enregistrement de ' + opt.name + '…');
        AwemaGH.saveSecret(opt.name, v).then(function (res) {
          inp.value = '';
          if (res && res.ok) { msg('✅ ' + opt.name + ' enregistré automatiquement.', '#34E5C4'); }
          else { msg('Presque ! ' + opt.name + ' — un collage sur GitHub (fenêtre ouverte).', '#D4AF37'); AwemaGH.guideSecret(opt.name, v); }
          if (bSync) bSync.disabled = false;
        }).catch(function (e) { msg('❌ ' + (e.message || e), '#FF7D9C'); });
      });
    };

    if (bSync) bSync.onclick = function () {
      msg('Déclenchement de « ' + (opt.syncLabel || 'la synchro') + ' »…');
      AwemaGH.ensure(function () {
        AwemaGH.runWorkflow(opt.sync, {}, true)
          .then(function () { msg('✅ Synchro lancée — les données arrivent dans ~1-2 min.', '#34E5C4'); })
          .catch(function (e) { msg('❌ ' + (e.message || e), '#FF7D9C'); });
      });
    };
  }

  return { secretBox: secretBox };
})();
