/* AwemaFork — rend l'instance autonome après un fork.
   Le template est publié sous codescooper/AwemA---Agence-Web-Marketing-Africaine ; un fork a un AUTRE
   propriétaire. Ce script déduit owner/repo du fork courant et réécrit les liens « upstream » vers le fork,
   pour que les boutons Secrets/Variables/Actions/dépôt pointent vers LE dépôt de l'agence.

   Détection (par ordre de fiabilité) :
     1. connexion GitHub déjà saisie (localStorage 'awema-gh') ;
     2. URL GitHub Pages : <owner>.github.io/<repo>/… ;
     3. AWEMA_CONFIG.github (config.js).
   API : window.AwemaFork.info() -> {owner, repo} | null ; .upstream ; .repoUrl(suffix).
*/
window.AwemaFork = (function () {
  var UP_OWNER = 'codescooper', UP_REPO = 'AwemA---Agence-Web-Marketing-Africaine';

  function info() {
    try { var c = JSON.parse(localStorage.getItem('awema-gh') || '{}'); if (c.owner && c.repo) return { owner: c.owner, repo: c.repo }; } catch (e) {}
    var h = location.hostname || '', seg = location.pathname.split('/').filter(Boolean);
    if (/\.github\.io$/i.test(h)) {
      var owner = h.replace(/\.github\.io$/i, '');
      // Pages de projet : owner.github.io/<repo>/… ; Pages racine : owner.github.io → repo = owner.github.io
      var repo = (seg.length && seg[0].indexOf('.') === -1) ? seg[0] : (owner + '.github.io');
      if (owner) return { owner: owner, repo: repo };
    }
    var g = (window.AWEMA_CONFIG && window.AWEMA_CONFIG.github) || {};
    if (g.owner && g.repo) return { owner: g.owner, repo: g.repo };
    return null;
  }

  function repoUrl(suffix) {
    var ni = info() || { owner: UP_OWNER, repo: UP_REPO };
    return 'https://github.com/' + ni.owner + '/' + ni.repo + (suffix || '');
  }

  function rewrite() {
    var ni = info();
    if (!ni || (ni.owner === UP_OWNER && ni.repo === UP_REPO)) return;  // on EST l'upstream, ou inconnu → rien à faire
    var from = UP_OWNER + '/' + UP_REPO, to = ni.owner + '/' + ni.repo;
    var sel = 'a[href*="' + from + '"]';
    try {
      document.querySelectorAll(sel).forEach(function (a) {
        // Ne réécrit PAS les liens « rejoindre la bêta / contact » du projet amont (data-upstream).
        if (a.hasAttribute('data-upstream')) return;
        a.href = a.href.split(from).join(to);
      });
    } catch (e) {}
  }

  if (document.readyState !== 'loading') rewrite();
  else document.addEventListener('DOMContentLoaded', rewrite);

  return { info: info, repoUrl: repoUrl, upstream: { owner: UP_OWNER, repo: UP_REPO } };
})();
