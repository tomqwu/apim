(() => {
  "use strict";

  function escapeHtml(value = "") {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function audienceHref(audience) {
    return `#/audiences/${encodeURIComponent(audience.id)}`;
  }

  function getById(audiences = [], id = "") {
    return audiences.find((audience) => audience.id === id);
  }

  function resolveSources(audience, items = []) {
    const byId = new Map(items.map((item) => [item.id, item]));
    return (audience?.sourceIds || []).map((id) => byId.get(id)).filter(Boolean);
  }

  function signalMarkup(signal) {
    return `<span class="audience-signal"><strong>${escapeHtml(signal.value)}</strong><small>${escapeHtml(signal.label)}</small></span>`;
  }

  function band(audiences = []) {
    if (!audiences.length) return "";
    return `<section class="audience-band" aria-labelledby="audience-band-title">
      <header>
        <span class="section-index">01 / Audience briefings</span>
        <h2 id="audience-band-title">Choose the room before the evidence.</h2>
        <p>One fact model; six curated paths with different decisions, depth, and closing actions.</p>
      </header>
      <nav class="audience-band-list" aria-label="Audience briefing shortcuts">
        ${audiences.map((audience, index) => `<a href="${audienceHref(audience)}">
          <span>${String(index + 1).padStart(2, "0")}</span>
          <strong>${escapeHtml(audience.shortLabel || audience.label)}</strong>
          <small>${escapeHtml(audience.verb)}</small>
        </a>`).join("")}
      </nav>
      <a class="action-link" href="#/audiences">Compare all audience lenses <span aria-hidden="true">→</span></a>
    </section>`;
  }

  function directory(audiences = []) {
    if (!audiences.length) return `<div class="page-shell"><div class="error-state"><h1>Audience paths unavailable.</h1></div></div>`;
    return `<div class="page-shell audience-directory">
      <header class="page-intro">
        <div>
          <p class="eyebrow">One evidence base / six conversations</p>
          <h1>Audience briefings</h1>
          <p class="lede">Start with the decision each role owns, then follow a short evidence path into the same canonical studies.</p>
        </div>
        <p class="intro-note">The lenses change sequence and depth—not the underlying facts. Unknown evidence remains unknown in every view.</p>
      </header>
      <section class="audience-index" aria-label="Available audience briefings">
        ${audiences.map((audience, index) => `<a class="audience-card" href="${audienceHref(audience)}">
          <span class="audience-card-index">${String(index + 1).padStart(2, "0")}</span>
          <span class="card-label">${escapeHtml(audience.group)}</span>
          <h2>${escapeHtml(audience.label)}</h2>
          <strong>${escapeHtml(audience.verb)}</strong>
          <p>${escapeHtml(audience.decision)}</p>
          <span class="audience-card-signal">${escapeHtml(audience.signals?.[0]?.value ?? "—")} · ${escapeHtml(audience.signals?.[0]?.label || "Evidence signal")}</span>
          <span class="row-arrow" aria-hidden="true">↗</span>
        </a>`).join("")}
      </section>
      <section class="audience-principle" aria-label="Audience design principle">
        <p class="eyebrow">Shared fact model</p>
        <h2>Different altitude. Same evidence.</h2>
        <p>Executives decide, directors mobilize, architects constrain, developers build and consume, SRE teams operate and recover, and platform teams enable at scale.</p>
      </section>
    </div>`;
  }

  function chart(charts, name, data, options = {}) {
    if (!charts?.render) return `<p class="visual-empty">Visualization unavailable.</p>`;
    try {
      return charts.render(name, data, options);
    } catch (error) {
      return `<p class="visual-empty">Visualization unavailable.</p>`;
    }
  }

  function visualMarkup(audience, visuals = {}, items = [], charts) {
    const compact = { compact: true };
    switch (audience.visual) {
      case "executive":
        return chart(charts, "criteriaOverview", visuals.criteria || {}, compact);
      case "directors":
        return chart(charts, "roadmap", visuals.repositoryRoadmap || {}, { title: "Repository maturity sequence" });
      case "architects": {
        const diagram = items.find((item) => item.path === "architecture/diagrams/target-state.mmd");
        return `<div class="audience-architecture-visual">
          ${diagram ? `<div class="audience-diagram" data-audience-diagram="${escapeHtml(diagram.contentUrl)}"><p>Rendering target-state reference…</p></div>` : ""}
          ${chart(charts, "statusMatrix", visuals.variants || [], { ...compact, title: "Candidate topology state" })}
        </div>`;
      }
      case "developers":
        return chart(charts, "pocStatus", visuals.poc || {}, { title: "Runnable proof state" });
      case "devops-sre":
        return `<div class="audience-visual-stack">${chart(charts, "pocStatus", visuals.poc || {}, { ...compact, title: "Execution state" })}${chart(charts, "governance", visuals.governance || {}, { ...compact, title: "Operational decision work" })}</div>`;
      case "platform-teams":
        return chart(charts, "roadmap", visuals.roadmap || {}, { title: "Implementation sequence" });
      default:
        return chart(charts, "governance", visuals.governance || {}, { title: "Decision work" });
    }
  }

  function switcher(audiences, current) {
    return `<nav class="audience-switcher" aria-label="Switch audience briefing">
      ${audiences.map((audience) => `<a href="${audienceHref(audience)}" ${audience.id === current.id ? 'aria-current="page"' : ""}>${escapeHtml(audience.shortLabel || audience.label)}</a>`).join("")}
    </nav>`;
  }

  function detail(audience, audiences = [], items = [], visuals = {}, charts) {
    if (!audience) return "";
    const sources = resolveSources(audience, items);
    return `<div class="page-shell audience-page">
      ${switcher(audiences, audience)}
      <header class="audience-hero">
        <div>
          <p class="eyebrow">${escapeHtml(audience.group)} / Audience lens</p>
          <h1>${escapeHtml(audience.label)}</h1>
          <strong class="audience-verb">${escapeHtml(audience.verb)}</strong>
          <p class="lede">${escapeHtml(audience.framing)}</p>
        </div>
        <div class="audience-decision">
          <span class="section-index">Decision to own</span>
          <p>${escapeHtml(audience.decision)}</p>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${escapeHtml(audience.presentationRoute)}">Present this briefing <span aria-hidden="true">→</span></a>
            <a class="action-link" href="${escapeHtml(audience.recommendedRoute)}">Open primary workspace <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </header>

      <section class="audience-signal-strip" aria-label="Current evidence signals">
        ${(audience.signals || []).map(signalMarkup).join("")}
      </section>

      <section class="audience-brief-grid">
        <article class="audience-questions">
          <span class="section-index">01 / Questions for the room</span>
          <h2>Resolve these before moving the decision.</h2>
          <ol>${(audience.questions || []).map((question) => `<li>${escapeHtml(question)}</li>`).join("")}</ol>
        </article>
        <article class="audience-evidence-view">
          <span class="section-index">02 / Evidence state</span>
          <h2>Read the current state without overclaiming.</h2>
          ${visualMarkup(audience, visuals, items, charts)}
        </article>
      </section>

      <section class="audience-reading" aria-labelledby="audience-reading-title">
        <header class="section-heading">
          <span class="section-index">03 / Start here</span>
          <h2 id="audience-reading-title">A sequenced evidence pack.</h2>
          <p>These are shortcuts into canonical material, not audience-specific copies.</p>
        </header>
        <div class="audience-reading-path">
          ${sources.map((item, index) => `<a href="#/doc/${encodeURIComponent(item.id)}">
            <span class="audience-reading-index">${String(index + 1).padStart(2, "0")}</span>
            <span><small>${escapeHtml(item.section)} / ${escapeHtml(item.type)}</small><strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(item.summary)}</p></span>
            <span class="row-arrow" aria-hidden="true">↗</span>
          </a>`).join("")}
        </div>
      </section>

      <section class="audience-close" aria-label="Recommended meeting outcome">
        <span class="section-index">04 / Close the meeting with</span>
        <p>${escapeHtml(audience.action)}</p>
        <a class="action-link is-primary" href="${escapeHtml(audience.presentationRoute)}">Open ${escapeHtml(audience.shortLabel)} briefing <span aria-hidden="true">→</span></a>
      </section>
    </div>`;
  }

  function presentationSlides(audience, slides = []) {
    if (!audience?.presentationSlides?.length) return slides;
    const byKey = new Map(slides.map((slide) => [slide.key, slide]));
    return audience.presentationSlides.map((key) => byKey.get(key)).filter(Boolean);
  }

  window.ApiStudyAudiences = {
    audienceHref,
    band,
    detail,
    directory,
    escapeHtml,
    getById,
    presentationSlides,
    resolveSources,
  };
})();
