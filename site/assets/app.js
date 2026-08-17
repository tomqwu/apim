(() => {
  "use strict";

  const main = document.querySelector("#main-content");
  const nav = document.querySelector("[data-nav]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const searchDialog = document.querySelector("[data-search-dialog]");
  const globalSearch = document.querySelector("[data-global-search]");
  const globalResults = document.querySelector("[data-global-results]");
  const toast = document.querySelector("[data-toast]");
  const modalBackground = [...document.querySelectorAll(".skip-link, [data-site-header], #main-content, [data-site-footer]")];

  const state = {
    manifest: null,
    library: { query: "", section: "All", type: "all" },
    renderToken: 0,
    searchReturnFocus: null,
    toastTimer: null,
  };

  const sectionDescriptions = {
    Studies: "The assessment narrative: context, requirements, platform deep dives, comparisons, roadmap, risks, and unresolved questions.",
    Compare: "A gated evaluation model with explicit weights, acceptance tests, evidence requirements, and provisional scorecards.",
    Architecture: "Current, transition, and target-state views across network, security, operations, observability, hybrid placement, and recovery.",
    Research: "Official sources, claim states, assumptions, and terminology that keep the assessment traceable.",
    "PoC & Examples": "Synthetic APIs, runnable gateway configurations, automation, and test plans for proving—or disproving—the architecture.",
    Migration: "Workload classification, migration patterns, wave planning, decommission controls, and a repeatable migration factory.",
    Workshops: "Facilitated study plans, an evidence-oriented question bank, and vendor validation packs.",
    Decisions: "Architecture decisions that keep hypotheses distinct from approved direction.",
    Templates: "Reusable structures for decisions, requirements, inventory, migration assessment, workshops, and PoC evidence.",
    Reports: "Delivery inventories and reproducible validation records for the repository itself.",
  };

  const featuredSections = [
    { name: "Studies", label: "Study", route: "library", filter: "Studies" },
    { name: "Compare", label: "Decide", route: "compare", filter: "Compare" },
    { name: "Architecture", label: "Model", route: "architecture", filter: "Architecture" },
    { name: "PoC & Examples", label: "Prove", route: "lab", filter: "PoC & Examples" },
    { name: "Research", label: "Trace", route: "library", filter: "Research" },
    { name: "Workshops", label: "Align", route: "library", filter: "Workshops" },
  ];

  function escapeHtml(value = "") {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function slug(value = "") {
    return String(value)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "") || "section";
  }

  function formatBytes(bytes = 0) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  }

  function formatType(type = "resource") {
    const labels = {
      markdown: "Study note",
      mermaid: "Diagram",
      csv: "Dataset",
      yaml: "Configuration",
      openapi: "API contract",
      presentation: "Presentation",
      pdf: "PDF",
      image: "Visual",
      shell: "Script",
      python: "Code",
      javascript: "Code",
      dockerfile: "Container",
      html: "HTML",
    };
    return labels[type] || type;
  }

  function itemHref(item) {
    return `#/doc/${encodeURIComponent(item.id)}`;
  }

  function setPageTitle(title) {
    document.title = title === "API Management Studies" ? title : `${title} — API Management Studies`;
  }

  function announce(message) {
    clearTimeout(state.toastTimer);
    toast.textContent = message;
    toast.hidden = false;
    state.toastTimer = setTimeout(() => {
      toast.hidden = true;
    }, 3200);
  }

  function closeMenu() {
    nav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
  }

  function setActiveNav(route) {
    document.querySelectorAll("[data-route-link]").forEach((link) => {
      if (link.dataset.routeLink === route) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  function parseRoute() {
    const [rawPath, rawQuery = ""] = location.hash.replace(/^#\/?/, "").split("?", 2);
    const parts = rawPath.split("/").filter(Boolean).map(decodeURIComponent);
    const params = new URLSearchParams(rawQuery);
    if (!parts.length) return { name: "overview", parts: [], params };
    return { name: parts[0], parts: parts.slice(1), params };
  }

  function sectionCount(name) {
    return state.manifest.items.filter((item) => item.section === name).length;
  }

  function metricMarkup(value, label) {
    return `<div class="metric"><strong class="metric-value">${escapeHtml(value)}</strong><span class="metric-label">${escapeHtml(label)}</span></div>`;
  }

  function chartMarkup(name, data, options = {}) {
    const charts = window.ApiStudyCharts;
    if (!charts || typeof charts.render !== "function") {
      return `<p class="visual-empty">Visualization data is available in the source manifest.</p>`;
    }
    try {
      return charts.render(name, data, options);
    } catch (error) {
      return `<p class="visual-empty">This visualization could not be rendered.</p>`;
    }
  }

  function visualPanel(index, eyebrow, title, note, body, extraClass = "") {
    return `
      <article class="visual-panel ${escapeHtml(extraClass)}">
        <header class="visual-panel-heading">
          <span class="section-index">${escapeHtml(index)} / ${escapeHtml(eyebrow)}</span>
          <h2>${escapeHtml(title)}</h2>
          <p>${escapeHtml(note)}</p>
        </header>
        <div class="visual-panel-body">${body}</div>
      </article>`;
  }

  function resourceRow(item, index) {
    return `
      <a class="resource-row" href="${itemHref(item)}">
        <span class="resource-meta">${String(index + 1).padStart(3, "0")}</span>
        <div>
          <h2>${escapeHtml(item.title)}</h2>
        </div>
        <p>${escapeHtml(item.summary)}</p>
        <span class="resource-meta resource-type">${escapeHtml(formatType(item.type))}</span>
        <span class="row-arrow" aria-hidden="true">↗</span>
      </a>`;
  }

  function studyCard({ name, label, route, filter }, index) {
    const count = sectionCount(name);
    const href = route === "library" ? `#/library?section=${encodeURIComponent(filter)}` : `#/${route}`;
    return `
      <a class="study-card" href="${href}">
        <span class="card-label">${String(index + 1).padStart(2, "0")} / ${escapeHtml(label)}</span>
        <span class="card-count">${count}</span>
        <h3>${escapeHtml(name)}</h3>
        <p>${escapeHtml(sectionDescriptions[name])}</p>
      </a>`;
  }

  function renderOverview() {
    const { stats, generatedAt } = state.manifest;
    const visuals = state.manifest.visuals || {};
    const audiences = state.manifest.audiences || [];
    const generated = new Date(generatedAt);
    const dateLabel = Number.isNaN(generated.getTime())
      ? "current repository state"
      : generated.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });

    setPageTitle("API Management Studies");
    setActiveNav("overview");
    main.innerHTML = `
      <div class="page-shell">
        <section class="page-hero" aria-labelledby="overview-title">
          <div class="hero-copy">
            <div>
              <p class="eyebrow">Living research system</p>
              <h1 class="display-title" id="overview-title">Study the platform. <em>Prove the system.</em></h1>
            </div>
            <p class="hero-deck">A navigable evidence base for API management research, architecture, platform comparison, proofs of concept, migration planning, and presentation-ready decisions.</p>
          </div>
          <aside class="hero-aside">
            <p>This portal is generated directly from the repository. Source notes remain portable Markdown, Mermaid, CSV, YAML, code, and downloadable presentation material.</p>
            <div class="hero-actions">
              <a class="action-link is-primary" href="#/present/0">Start presentation <span aria-hidden="true">→</span></a>
              <a class="action-link" href="#/library">Explore the library <span aria-hidden="true">↗</span></a>
              <span class="resource-meta">Indexed ${escapeHtml(dateLabel)}</span>
            </div>
          </aside>
        </section>

        ${window.ApiStudyAudiences?.band ? window.ApiStudyAudiences.band(audiences) : ""}

        <section class="metric-strip" aria-label="Repository facts">
          ${metricMarkup(stats.studies, "assessment chapters")}
          ${metricMarkup(stats.diagrams, "architecture diagrams")}
          ${metricMarkup(stats.criteria, "decision criteria")}
          ${metricMarkup(stats.sources, "official sources")}
          ${metricMarkup(stats.questions, "workshop questions")}
          ${metricMarkup(stats.apiContracts, "API contracts")}
        </section>

        <section class="overview-visuals" aria-label="Assessment state at a glance">
          <div class="overview-visual">
            <span class="section-index">Evidence state</span>
            ${chartMarkup("donut", visuals.criteria?.statuses || [], { title: "Criteria status", total: visuals.criteria?.total, centerLabel: "criteria", compact: true })}
          </div>
          <div class="overview-visual">
            <span class="section-index">Research balance</span>
            ${chartMarkup("sourceBalance", visuals.sources || {}, { title: "Sources by vendor", compact: true })}
          </div>
          <div class="overview-visual">
            <span class="section-index">Execution proof</span>
            ${chartMarkup("pocStatus", visuals.poc || {}, { title: "PoC status", compact: true })}
          </div>
        </section>

        <section class="content-section" aria-labelledby="streams-title">
          <div class="section-heading">
            <span class="section-index">02 / Study streams</span>
            <h2 id="streams-title">One repository, six ways into the evidence.</h2>
            <p>Use the curated paths for orientation. Use Library when you need the complete source record.</p>
          </div>
          <div class="study-grid">
            ${featuredSections.map(studyCard).join("")}
          </div>
        </section>

        <section class="content-section" aria-labelledby="method-title">
          <div class="section-heading">
            <span class="section-index">03 / Method</span>
            <h2 id="method-title">From claim to decision, without hiding uncertainty.</h2>
            <p>The material is intentionally explicit about what is known, inferred, assumed, tested, and still open.</p>
          </div>
          <div class="lab-sequence">
            <div class="lab-step"><span class="card-label">01 / Frame</span><strong>Define the decision</strong><p>Separate business outcomes, gateway concerns, and integration-runtime responsibilities.</p></div>
            <div class="lab-step"><span class="card-label">02 / Trace</span><strong>Collect evidence</strong><p>Link material claims to official sources, workshop findings, or reproducible execution.</p></div>
            <div class="lab-step"><span class="card-label">03 / Prove</span><strong>Test the architecture</strong><p>Exercise the thin gateway baseline, failure modes, security controls, and migration patterns.</p></div>
            <div class="lab-step"><span class="card-label">04 / Decide</span><strong>Score with restraint</strong><p>Resolve mandatory gates first and leave unevidenced scores explicitly unknown.</p></div>
          </div>
        </section>

        <section class="evidence-band" aria-label="Evidence principle">
          <div>
            <p class="eyebrow">Evidence principle</p>
            <h2>Unknown stays unknown.</h2>
          </div>
          <div>
            <span class="section-index">${stats.mandatoryGates} mandatory gates / ${stats.criteria} total criteria</span>
            <blockquote>“A polished answer is not stronger than a traceable one. The portal makes the evidence state visible.”</blockquote>
            <a class="slide-source" href="#/compare">Open the decision model <span aria-hidden="true">↗</span></a>
          </div>
        </section>
      </div>`;
  }

  function renderAudiences() {
    setPageTitle("Audience briefings");
    setActiveNav("audiences");
    main.innerHTML = window.ApiStudyAudiences?.directory
      ? window.ApiStudyAudiences.directory(state.manifest.audiences || [])
      : `<div class="page-shell"><div class="error-state"><h1>Audience paths unavailable.</h1></div></div>`;
  }

  async function renderAudienceDiagram() {
    const target = document.querySelector("[data-audience-diagram]");
    if (!target) return;
    try {
      const text = await fetchText(target.dataset.audienceDiagram);
      await mermaidMarkup(text, target);
    } catch (error) {
      target.innerHTML = `<p class="visual-empty">Open the architecture gallery to inspect this model.</p>`;
    }
  }

  function renderAudience(id) {
    const audiences = state.manifest.audiences || [];
    const audience = window.ApiStudyAudiences?.getById?.(audiences, id);
    if (!audience) return renderNotFound("That audience briefing is not configured.");
    setPageTitle(`${audience.label} briefing`);
    setActiveNav("audiences");
    main.innerHTML = window.ApiStudyAudiences.detail(
      audience,
      audiences,
      state.manifest.items || [],
      state.manifest.visuals || {},
      window.ApiStudyCharts,
    );
    renderAudienceDiagram();
  }

  function renderVisualAtlas() {
    setPageTitle("Visual Atlas");
    setActiveNav("visuals");
    main.innerHTML = window.ApiStudyCharts?.atlas
      ? window.ApiStudyCharts.atlas(state.manifest.visuals || {})
      : `<div class="page-shell"><div class="error-state"><h1>Visual data unavailable.</h1></div></div>`;
  }

  function parseLibraryQuery() {
    const raw = location.hash.split("?")[1] || "";
    const params = new URLSearchParams(raw);
    state.library.query = "";
    state.library.type = "all";
    state.library.section = params.get("section") || "All";
  }

  function filterItems(query, section, type) {
    const terms = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    return state.manifest.items.filter((item) => {
      if (section !== "All" && item.section !== section) return false;
      if (type !== "all" && item.type !== type) return false;
      if (!terms.length) return true;
      const haystack = `${item.title} ${item.summary} ${item.section} ${(item.tags || []).join(" ")} ${item.searchText || ""}`.toLowerCase();
      return terms.every((term) => haystack.includes(term));
    });
  }

  function updateLibraryResults() {
    const results = filterItems(state.library.query, state.library.section, state.library.type);
    const list = document.querySelector("[data-library-results]");
    const count = document.querySelector("[data-result-count]");
    if (!list || !count) return;
    count.textContent = `${results.length} result${results.length === 1 ? "" : "s"}`;
    list.innerHTML = results.length
      ? results.map(resourceRow).join("")
      : `<div class="empty-state"><h2>No material matches that view.</h2><p>Clear a filter or try a broader evidence term.</p></div>`;
  }

  function renderLibrary() {
    parseLibraryQuery();
    const sections = ["All", ...Object.keys(sectionDescriptions).filter((section) => sectionCount(section) > 0)];
    const types = [...new Set(state.manifest.items.map((item) => item.type))].sort();
    setPageTitle("Library");
    setActiveNav("library");
    main.innerHTML = `
      <div class="page-shell">
        <header class="page-intro">
          <div>
            <p class="eyebrow">Complete source record</p>
            <h1>Library</h1>
            <p class="lede">Search every study, evidence record, diagram, dataset, contract, example, workshop, migration guide, decision, template, and report.</p>
          </div>
          <p class="intro-note">The index is generated from filenames and first-level titles. New supported content appears here automatically after the next build.</p>
        </header>
        <section aria-label="Library controls">
          <div class="library-tools">
            <input type="search" value="${escapeHtml(state.library.query)}" placeholder="Search title, text, tag, or platform…" aria-label="Search library" data-library-search>
            <select aria-label="Filter by resource type" data-library-type>
              <option value="all">All formats</option>
              ${types.map((type) => `<option value="${escapeHtml(type)}" ${state.library.type === type ? "selected" : ""}>${escapeHtml(formatType(type))}</option>`).join("")}
            </select>
            <span class="result-count" data-result-count></span>
          </div>
          <div class="filter-row" aria-label="Filter by collection">
            ${sections.map((section) => `<button class="filter-chip" type="button" data-section-filter="${escapeHtml(section)}" aria-pressed="${state.library.section === section}">${escapeHtml(section)}${section === "All" ? "" : ` · ${sectionCount(section)}`}</button>`).join("")}
          </div>
          <div class="resource-list" data-library-results></div>
        </section>
      </div>`;
    updateLibraryResults();
    const search = document.querySelector("[data-library-search]");
    search.addEventListener("input", (event) => {
      state.library.query = event.target.value;
      updateLibraryResults();
    });
    document.querySelector("[data-library-type]").addEventListener("change", (event) => {
      state.library.type = event.target.value;
      updateLibraryResults();
    });
    document.querySelectorAll("[data-section-filter]").forEach((button) => {
      button.addEventListener("click", () => {
        state.library.section = button.dataset.sectionFilter;
        document.querySelectorAll("[data-section-filter]").forEach((chip) => chip.setAttribute("aria-pressed", String(chip === button)));
        updateLibraryResults();
      });
    });
  }

  function findByPath(path) {
    return state.manifest.items.find((item) => item.path === path);
  }

  async function renderDiagramPreviews() {
    const targets = [...document.querySelectorAll("[data-diagram-preview]")];
    const load = async (target) => {
      if (target.dataset.rendered === "true") return;
      target.dataset.rendered = "true";
      try {
        const text = await fetchText(target.dataset.diagramPreview);
        await mermaidMarkup(text, target);
      } catch (error) {
        target.innerHTML = `<p class="visual-empty">Preview unavailable. Open the source diagram to inspect it.</p>`;
      }
    };
    if (!("IntersectionObserver" in window)) {
      await Promise.all(targets.map(load));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        load(entry.target);
      });
    }, { rootMargin: "240px" });
    targets.forEach((target) => observer.observe(target));
  }

  function renderCompare() {
    const stats = state.manifest.stats;
    const visuals = state.manifest.visuals || {};
    const criteriaState = visuals.criteria || {};
    const criteriaTotal = Number(criteriaState.total) || stats.criteria || 0;
    const criteriaStatuses = Array.isArray(criteriaState.statuses) ? criteriaState.statuses : [];
    const unknownState = criteriaStatuses.find((item) => String(item.label).toLowerCase() === "unknown");
    const unknownCriteria = unknownState ? Number(unknownState.value) || 0 : (criteriaStatuses.length ? 0 : criteriaTotal);
    const evidencedCriteria = Math.max(criteriaTotal - unknownCriteria, 0);
    const evidenceCoverage = criteriaTotal ? Math.round((evidencedCriteria / criteriaTotal) * 100) : 0;
    const evidenceSummary = unknownCriteria === criteriaTotal
      ? `All ${criteriaTotal} criteria currently remain “unknown” in the evidence ledger.`
      : `${unknownCriteria} of ${criteriaTotal} criteria remain “unknown”; ${evidencedCriteria} have a recorded evidence state.`;
    const criteria = findByPath("decision-matrix/criteria.csv");
    const platformPaths = [
      "docs/10-kong-deep-dive.md",
      "docs/19-azure-apim-assessment.md",
      "docs/21-apigee-assessment.md",
      "docs/23-mulesoft-current-state-baseline.md",
    ];
    const platforms = platformPaths.map(findByPath).filter(Boolean);
    setPageTitle("Compare");
    setActiveNav("compare");
    main.innerHTML = `
      <div class="page-shell">
        <header class="page-intro">
          <div>
            <p class="eyebrow">Decision model</p>
            <h1>Compare</h1>
            <p class="lede">Test platform fit against mandatory gates and weighted criteria. The current scorecards stay unscored until evidence is sufficient.</p>
          </div>
          <p class="intro-note">A leading hypothesis is useful. A hidden assumption is not. Product conclusions remain provisional until the stated acceptance tests are met.</p>
        </header>

        <section class="content-section">
          <div class="compare-summary">
            <div class="compare-score">
              <span class="eyebrow">Evidence coverage</span>
              <strong>${escapeHtml(evidenceCoverage)}%</strong>
              <p>${escapeHtml(evidenceSummary)} This is a baseline for disciplined validation, not a completed ranking.</p>
            </div>
            <div class="compare-copy">
              <div>
                <span class="section-index">${stats.mandatoryGates} mandatory / ${stats.criteria} total</span>
                <h2>Pass the gates before weighting preference.</h2>
              </div>
              <div class="category-bars">${chartMarkup("stackedBars", visuals.criteria?.categories || [], { title: "Criteria by category", keys: ["mandatory", "weighted"], compact: true })}</div>
              ${criteria ? `<a class="action-link" href="${itemHref(criteria)}">Open all criteria <span aria-hidden="true">↗</span></a>` : ""}
            </div>
          </div>
        </section>

        <section class="content-section" aria-labelledby="decision-views-title">
          <div class="section-heading">
            <span class="section-index">01 / Decision views</span>
            <h2 id="decision-views-title">See what can—and cannot—be concluded.</h2>
            <p>The visual model separates candidate status, evidence confidence, research balance, and gate structure.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualPanel("A", "Variants", "Exact deployment models", "Family-level scores would hide topology and entitlement differences.", chartMarkup("statusMatrix", visuals.variants || [], { title: "Variant status" }), "is-wide")}
            ${visualPanel("B", "Evidence", "Confidence ladder", "Higher confidence requires execution under representative conditions.", chartMarkup("evidenceLadder", visuals.methodology?.evidenceLevels || [], { title: "Evidence levels" }))}
            ${visualPanel("C", "Research", "Official-source balance", "Volume is visible; criterion-level traceability still determines fitness for scoring.", chartMarkup("sourceBalance", visuals.sources || {}, { title: "Sources by vendor" }))}
          </div>
        </section>

        <section class="content-section" aria-labelledby="platforms-title">
          <div class="section-heading">
            <span class="section-index">02 / Platform lenses</span>
            <h2 id="platforms-title">Keep the alternatives explicit.</h2>
            <p>Each platform is assessed in its actual deployment model, with version, licensing, and operational boundaries visible.</p>
          </div>
          <div class="study-grid">
            ${platforms.map((item, index) => `
              <a class="study-card" href="${itemHref(item)}">
                <span class="card-label">${String(index + 1).padStart(2, "0")} / Assessment</span>
                <h3>${escapeHtml(item.title)}</h3>
                <p>${escapeHtml(item.summary)}</p>
              </a>`).join("")}
          </div>
        </section>
      </div>`;
  }

  function renderArchitecture() {
    const diagrams = state.manifest.items.filter((item) => item.type === "mermaid");
    setPageTitle("Architecture");
    setActiveNav("architecture");
    main.innerHTML = `
      <div class="page-shell">
        <header class="page-intro">
          <div>
            <p class="eyebrow">System views</p>
            <h1>Architecture</h1>
            <p class="lede">Trace the system from current state through transition and target state, then inspect the security, network, operations, observability, hybrid, and recovery views.</p>
          </div>
          <p class="intro-note">Every diagram remains editable Mermaid source. The browser renders it on demand and the source stays available for review.</p>
        </header>
        <section class="content-section">
          <div class="section-heading">
            <span class="section-index">${String(diagrams.length).padStart(2, "0")} / Diagrams</span>
            <h2>Different views of one evolving system.</h2>
            <p>Use each diagram with its companion architecture note; diagrams are models, not deployment evidence.</p>
          </div>
          <div class="architecture-grid">
            ${diagrams.map((item, index) => `
              <a class="architecture-card" href="${itemHref(item)}">
                <div class="architecture-preview" data-diagram-preview="${escapeHtml(item.contentUrl)}" aria-label="Preview of ${escapeHtml(item.title)}"><p>Rendering model…</p></div>
                <span class="card-label">${String(index + 1).padStart(2, "0")} / Mermaid source</span>
                <h2>${escapeHtml(item.title)}</h2>
                <p>${escapeHtml(item.summary)}</p>
              </a>`).join("")}
          </div>
        </section>
      </div>`;
    renderDiagramPreviews();
  }

  function renderLab() {
    const stats = state.manifest.stats;
    const visuals = state.manifest.visuals || {};
    const preferred = [
      "poc/README.md",
      "poc/test-plan.md",
      "poc/security-tests.md",
      "poc/performance-tests.md",
      "poc/failure-tests.md",
      "poc/migration-tests.md",
    ].map(findByPath).filter(Boolean);
    const contracts = state.manifest.items.filter((item) => item.type === "openapi");
    setPageTitle("PoC Lab");
    setActiveNav("lab");
    main.innerHTML = `
      <div class="page-shell">
        <header class="page-intro">
          <div>
            <p class="eyebrow">Executable evidence</p>
            <h1>PoC Lab</h1>
            <p class="lede">A synthetic environment for turning platform and architecture claims into observable, repeatable tests.</p>
          </div>
          <p class="intro-note">The baseline proves only what its scripts and captured evidence exercise. Enterprise, SaaS, network, and production controls remain gated tests.</p>
        </header>

        <section class="content-section">
          <div class="lab-sequence">
            <div class="lab-step"><span class="card-label">01 / Define</span><strong>${stats.apiContracts} contracts</strong><p>Synthetic API surfaces establish stable, inspectable test inputs.</p></div>
            <div class="lab-step"><span class="card-label">02 / Configure</span><strong>Two runtime paths</strong><p>Docker provides the thin baseline; Kubernetes models the target direction.</p></div>
            <div class="lab-step"><span class="card-label">03 / Exercise</span><strong>${stats.pocScenarios} scenarios</strong><p>Security, failure, performance, hybrid, API operations, and migration tests.</p></div>
            <div class="lab-step"><span class="card-label">04 / Record</span><strong>Evidence first</strong><p>Acceptance criteria distinguish execution proof from product documentation.</p></div>
          </div>
          <div class="lab-visuals">
            ${visualPanel("A", "Scenario state", "Execution is deliberately explicit", "Automated, scripted, and not-run tests are reported separately.", chartMarkup("pocStatus", visuals.poc || {}, { title: "PoC scenario state" }), "is-wide")}
            ${visualPanel("B", "Evidence path", "A passing harness is not a production pilot", "Each result should move confidence only as far as its environment and artifacts support.", chartMarkup("evidenceLadder", visuals.methodology?.evidenceLevels || [], { title: "Evidence confidence" }))}
          </div>
          <div class="lab-grid">
            ${preferred.map((item, index) => `
              <a class="lab-card" href="${itemHref(item)}">
                <span class="card-label">${String(index + 1).padStart(2, "0")} / ${escapeHtml(formatType(item.type))}</span>
                <h2>${escapeHtml(item.title)}</h2>
                <p>${escapeHtml(item.summary)}</p>
              </a>`).join("")}
          </div>
        </section>

        <section class="content-section" aria-labelledby="contracts-title">
          <div class="section-heading">
            <span class="section-index">02 / Contracts</span>
            <h2 id="contracts-title">The API surface under test.</h2>
            <p>Open any contract to inspect its operations, version, and raw OpenAPI definition.</p>
          </div>
          <div class="resource-list">
            ${contracts.map(resourceRow).join("")}
          </div>
        </section>
      </div>`;
  }

  async function fetchText(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Unable to load ${url} (${response.status})`);
    return response.text();
  }

  function markdownToHtml(markdown) {
    if (!window.marked || !window.DOMPurify) return `<pre class="code-view">${escapeHtml(markdown)}</pre>`;
    const raw = window.marked.parse(markdown, { gfm: true, breaks: false });
    return window.DOMPurify.sanitize(raw, { USE_PROFILES: { html: true } });
  }

  function normalizeRepoPath(basePath, href) {
    const clean = href.split("#")[0].split("?")[0];
    const stack = basePath.split("/").slice(0, -1);
    clean.split("/").forEach((part) => {
      if (!part || part === ".") return;
      if (part === "..") stack.pop();
      else stack.push(part);
    });
    return stack.join("/");
  }

  function enhanceMarkdown(container, item) {
    const rail = document.querySelector("[data-document-rail]");
    const headings = [...container.querySelectorAll("h2, h3")];
    const used = new Set();
    headings.forEach((heading) => {
      let id = slug(heading.textContent);
      while (used.has(id)) id = `${id}-section`;
      used.add(id);
      heading.id = id;
    });
    if (rail) {
      rail.innerHTML = headings.slice(0, 12).map((heading) => `<a href="#${escapeHtml(heading.id)}">${escapeHtml(heading.textContent)}</a>`).join("") || "<span>No subsections</span>";
      rail.addEventListener("click", (event) => {
        const link = event.target.closest('a[href^="#"]');
        if (!link) return;
        event.preventDefault();
        document.getElementById(link.getAttribute("href").slice(1))?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }

    container.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      event.preventDefault();
      document.getElementById(link.getAttribute("href").slice(1))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    container.querySelectorAll("a[href]").forEach((link) => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#") || /^(https?:|mailto:|tel:)/i.test(href)) {
        if (/^https?:/i.test(href || "")) {
          link.target = "_blank";
          link.rel = "noreferrer";
        }
        return;
      }
      const repoPath = normalizeRepoPath(item.path, href);
      const target = findByPath(repoPath);
      link.href = target ? itemHref(target) : `content/${repoPath}`;
    });

    container.querySelectorAll("img[src]").forEach((image) => {
      const src = image.getAttribute("src");
      if (!src || /^(https?:|data:)/i.test(src)) return;
      image.src = `content/${normalizeRepoPath(item.path, src)}`;
      image.loading = "lazy";
    });

    container.querySelectorAll("table").forEach((table) => {
      const wrapper = document.createElement("div");
      wrapper.className = "table-wrap";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });
  }

  async function renderInlineMermaid(container) {
    const blocks = [...container.querySelectorAll("pre code.language-mermaid")];
    for (const code of blocks) {
      const source = code.textContent || "";
      const original = code.closest("pre");
      if (!original || !source.trim()) continue;
      const figure = document.createElement("figure");
      figure.className = "inline-diagram";
      const frame = document.createElement("div");
      frame.className = "diagram-frame";
      frame.innerHTML = "<p>Rendering model…</p>";
      const details = document.createElement("details");
      const summary = document.createElement("summary");
      summary.textContent = "Show Mermaid source";
      const sourceView = document.createElement("pre");
      sourceView.className = "code-view";
      const sourceCode = document.createElement("code");
      sourceCode.textContent = source;
      sourceView.appendChild(sourceCode);
      details.append(summary, sourceView);
      figure.append(frame, details);
      original.replaceWith(figure);
      await mermaidMarkup(source, frame);
    }
  }

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      const next = text[index + 1];
      if (char === '"' && quoted && next === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = !quoted;
      } else if (char === "," && !quoted) {
        row.push(field);
        field = "";
      } else if ((char === "\n" || char === "\r") && !quoted) {
        if (char === "\r" && next === "\n") index += 1;
        row.push(field);
        if (row.some((value) => value.length)) rows.push(row);
        row = [];
        field = "";
      } else {
        field += char;
      }
    }
    if (field.length || row.length) {
      row.push(field);
      rows.push(row);
    }
    return rows;
  }

  function csvMarkup(text) {
    const rows = parseCsv(text);
    if (!rows.length) return "<p>The dataset is empty.</p>";
    const width = Math.max(...rows.map((row) => row.length));
    const normalized = rows.map((row) => [...row, ...Array(Math.max(0, width - row.length)).fill("")]);
    return `
      <div class="table-wrap">
        <table class="data-table">
          <thead><tr>${normalized[0].map((cell) => `<th scope="col">${escapeHtml(cell)}</th>`).join("")}</tr></thead>
          <tbody>${normalized.slice(1).map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join("")}</tr>`).join("")}</tbody>
        </table>
      </div>`;
  }

  function openApiMarkup(text, item) {
    const version = text.match(/^openapi:\s*["']?([^\s"']+)/m)?.[1] || "OpenAPI";
    const apiVersion = text.match(/^\s{2}version:\s*["']?(.+?)["']?\s*$/m)?.[1] || "unspecified";
    const operations = [...text.matchAll(/^\s{4}(get|post|put|patch|delete|options|head):\s*$/gim)].map((match) => match[1].toUpperCase());
    const paths = [...text.matchAll(/^\s{2}(\/[^:]+):\s*$/gm)].map((match) => match[1]);
    return `
      <section class="metric-strip" aria-label="API contract facts">
        ${metricMarkup(version, "specification")}
        ${metricMarkup(apiVersion, "API version")}
        ${metricMarkup(paths.length, "paths")}
        ${metricMarkup(operations.length, "operations")}
        ${metricMarkup(new Set(operations).size, "methods")}
        ${metricMarkup(formatBytes(item.size), "source size")}
      </section>
      <h2>Operations</h2>
      ${paths.length ? `<ul>${paths.map((path) => `<li><code>${escapeHtml(path)}</code></li>`).join("")}</ul>` : "<p>No paths were detected.</p>"}
      <h2>OpenAPI source</h2>
      <pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
  }

  async function mermaidMarkup(text, target) {
    if (!window.mermaid) {
      target.innerHTML = `<pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
      return;
    }
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        fontFamily: "Inter, Arial, sans-serif",
        themeVariables: {
          background: "#fbfaf5",
          primaryColor: "#e9e4d8",
          primaryTextColor: "#151714",
          primaryBorderColor: "#151714",
          lineColor: "#62675f",
          secondaryColor: "#f3f0e7",
          tertiaryColor: "#d84a2d",
          clusterBkg: "#f3f0e7",
          clusterBorder: "#8c8e87",
        },
      });
      const id = `mermaid-${Date.now()}-${Math.random().toString(16).slice(2)}`;
      const result = await window.mermaid.render(id, text);
      target.innerHTML = window.DOMPurify ? window.DOMPurify.sanitize(result.svg, { USE_PROFILES: { svg: true, svgFilters: true } }) : result.svg;
    } catch (error) {
      target.innerHTML = `<div class="error-state"><h1>Diagram source could not render.</h1><p>${escapeHtml(error.message)}</p><pre class="code-view"><code>${escapeHtml(text)}</code></pre></div>`;
    }
  }

  function documentScaffold(item) {
    return `
      <article class="document-shell">
        <header class="document-header">
          <div>
            <nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/library">Library</a> / ${escapeHtml(item.section)}</nav>
            <h1>${escapeHtml(item.title)}</h1>
          </div>
          <aside class="document-meta-panel">
            <dl>
              <dt>Format</dt><dd>${escapeHtml(formatType(item.type))}</dd>
              <dt>Source</dt><dd>${escapeHtml(item.path)}</dd>
              <dt>Size</dt><dd>${escapeHtml(formatBytes(item.size))}</dd>
            </dl>
            <div class="tag-list">${(item.tags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div>
            <a class="action-link" href="${escapeHtml(item.contentUrl)}" download>Download source <span aria-hidden="true">↓</span></a>
          </aside>
        </header>
        <div class="document-body-grid">
          <nav class="document-rail" aria-label="On this page" data-document-rail><span>Loading sections…</span></nav>
          <div class="reading-column" data-document-content><div class="loading-state"><span class="loading-index">··</span><p>Loading source…</p></div></div>
          <aside class="side-note">Repository source remains the canonical record. Presentation views are curated interpretations of this material.</aside>
        </div>
      </article>`;
  }

  function documentVisualContext(item) {
    const charts = window.ApiStudyCharts;
    return charts?.documentContext ? charts.documentContext(item, state.manifest.visuals || {}) : "";
  }

  async function renderDocument(id) {
    const item = state.manifest.items.find((candidate) => candidate.id === id);
    if (!item) return renderNotFound("That resource is not in the generated index.");
    const token = ++state.renderToken;
    setPageTitle(item.title);
    setActiveNav(item.section === "Architecture" ? "architecture" : item.section === "Compare" ? "compare" : item.section === "PoC & Examples" ? "lab" : "library");
    main.innerHTML = documentScaffold(item);
    const target = document.querySelector("[data-document-content]");
    try {
      if (["pdf", "presentation", "video", "image"].includes(item.type)) {
        if (item.type === "image") {
          target.innerHTML = `<figure><img src="${escapeHtml(item.contentUrl)}" alt="${escapeHtml(item.title)}" style="max-width:100%;height:auto"><figcaption>${escapeHtml(item.summary)}</figcaption></figure>`;
        } else {
          target.innerHTML = `<div class="empty-state"><h2>${escapeHtml(formatType(item.type))} resource</h2><p>${escapeHtml(item.summary)}</p><a class="action-link is-primary" href="${escapeHtml(item.contentUrl)}" target="_blank" rel="noreferrer">Open resource <span aria-hidden="true">↗</span></a></div>`;
        }
        return;
      }
      const text = await fetchText(item.contentUrl);
      if (token !== state.renderToken) return;
      if (item.type === "markdown") {
        target.innerHTML = `${documentVisualContext(item)}<div class="prose">${markdownToHtml(text)}</div>`;
        enhanceMarkdown(target.querySelector(".prose"), item);
        await renderInlineMermaid(target.querySelector(".prose"));
      } else if (item.type === "csv") {
        target.innerHTML = `${documentVisualContext(item)}${csvMarkup(text)}`;
        document.querySelector("[data-document-rail]").innerHTML = "<span>Filterable dataset</span>";
      } else if (item.type === "mermaid") {
        target.innerHTML = `<div class="diagram-frame" data-diagram-frame><p>Rendering diagram…</p></div><h2>Mermaid source</h2><pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
        document.querySelector("[data-document-rail]").innerHTML = "<span>Rendered model</span><a href=\"#diagram-source\">Source</a>";
        document.querySelector("[data-document-rail] a").addEventListener("click", (event) => {
          event.preventDefault();
          document.getElementById("diagram-source")?.scrollIntoView({ behavior: "smooth", block: "start" });
        });
        target.querySelector("h2").id = "diagram-source";
        await mermaidMarkup(text, target.querySelector("[data-diagram-frame]"));
      } else if (item.type === "openapi") {
        target.innerHTML = `<div class="prose">${openApiMarkup(text, item)}</div>`;
        enhanceMarkdown(target.querySelector(".prose"), item);
      } else if (item.type === "html") {
        target.innerHTML = `<div class="empty-state"><h2>HTML presentation or prototype</h2><p>Open this resource in a separate tab to use its native interactions.</p><a class="action-link is-primary" href="${escapeHtml(item.contentUrl)}" target="_blank" rel="noreferrer">Open HTML <span aria-hidden="true">↗</span></a></div>`;
      } else {
        target.innerHTML = `<pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
        document.querySelector("[data-document-rail]").innerHTML = `<span>${escapeHtml(formatType(item.type))} source</span>`;
      }
    } catch (error) {
      target.innerHTML = `<div class="error-state"><h1>Source unavailable.</h1><p>${escapeHtml(error.message)}</p></div>`;
    }
  }

  function presentationVisualMarkup(slide, source) {
    const visuals = state.manifest.visuals || {};
    const options = { presentation: true, compact: true, title: slide.metricLabel };
    switch (slide.visual) {
      case "composition": return chartMarkup("composition", visuals.library || {}, options);
      case "methodologyFlow": return chartMarkup("methodologyFlow", visuals.methodology?.steps || [], options);
      case "stackedBars": return chartMarkup("stackedBars", visuals.criteria?.categories || [], { ...options, keys: ["mandatory", "weighted"] });
      case "statusMatrix": return chartMarkup("statusMatrix", visuals.variants || [], options);
      case "architectureDiagram": return source ? `<div class="slide-diagram" data-slide-diagram="${escapeHtml(source.contentUrl)}"><p>Rendering system model…</p></div>` : "";
      case "donut": return chartMarkup("donut", visuals.criteria?.statuses || [], { ...options, total: visuals.criteria?.total, centerLabel: "criteria" });
      case "sourceBalance": return chartMarkup("sourceBalance", visuals.sources || {}, options);
      case "pocStatus": return chartMarkup("pocStatus", visuals.poc || {}, options);
      case "roadmap": return chartMarkup("roadmap", visuals.roadmap || {}, options);
      case "governance": return chartMarkup("governance", visuals.governance || {}, options);
      default: return "";
    }
  }

  async function renderPresentationDiagram() {
    const target = document.querySelector("[data-slide-diagram]");
    if (!target) return;
    try {
      const text = await fetchText(target.dataset.slideDiagram);
      await mermaidMarkup(text, target);
    } catch (error) {
      target.innerHTML = `<p class="visual-empty">Open the supporting source to inspect this model.</p>`;
    }
  }

  function presentationContext(audienceId = "") {
    const allSlides = state.manifest.presentation || [];
    const audience = audienceId
      ? window.ApiStudyAudiences?.getById?.(state.manifest.audiences || [], audienceId)
      : null;
    const slides = window.ApiStudyAudiences?.presentationSlides
      ? window.ApiStudyAudiences.presentationSlides(audience, allSlides)
      : allSlides;
    return { audience, slides };
  }

  function presentationExitHref(audience) {
    return audience ? `#/audiences/${encodeURIComponent(audience.id)}` : "#/overview";
  }

  function renderPresentation(rawIndex, audienceId = "") {
    const { audience, slides } = presentationContext(audienceId);
    if (!slides.length) return renderNotFound("No presentation story is configured.");
    let index = Number.parseInt(rawIndex, 10);
    if (Number.isNaN(index)) index = 0;
    index = Math.min(Math.max(index, 0), slides.length - 1);
    const slide = slides[index];
    const source = state.manifest.items.find((item) => item.id === slide.sourceId);
    document.body.classList.add("is-presenting");
    setPageTitle(`${index + 1}. ${slide.title}${audience ? ` — ${audience.shortLabel}` : ""}`);
    setActiveNav("");
    main.innerHTML = `
      <section class="presentation-stage" aria-label="Presentation slide ${index + 1} of ${slides.length}">
        <article class="presentation-slide">
          <div class="slide-main">
            <span class="eyebrow">${escapeHtml(slide.eyebrow)}${audience ? ` / ${escapeHtml(audience.shortLabel)} lens` : ""}</span>
            <div class="slide-narrative">
              <h1 class="slide-title">${escapeHtml(slide.title)}</h1>
              <div class="slide-visual">${presentationVisualMarkup(slide, source)}</div>
            </div>
            <span class="slide-counter">${audience ? `${escapeHtml(audience.shortLabel)} briefing · ` : ""}${String(index + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}</span>
          </div>
          <aside class="slide-aside">
            <div class="slide-metric"><strong>${escapeHtml(slide.metric)}</strong><span>${escapeHtml(slide.metricLabel)}</span></div>
            ${audience ? `<div class="slide-audience-cue"><span>Close this room with</span><p>${escapeHtml(audience.action)}</p></div>` : ""}
            <p class="slide-body">${escapeHtml(slide.body)}</p>
            ${source ? `<a class="slide-source" href="${itemHref(source)}">Open supporting source <span aria-hidden="true">↗</span></a>` : ""}
          </aside>
        </article>
        <div class="slide-controls" aria-label="Presentation controls">
          <button type="button" data-slide-prev aria-label="Previous slide" ${index === 0 ? "disabled" : ""}>←</button>
          <button type="button" data-slide-next aria-label="Next slide" ${index === slides.length - 1 ? "disabled" : ""}>→</button>
          <button type="button" data-fullscreen aria-label="Toggle fullscreen">⛶</button>
          <a href="${presentationExitHref(audience)}" aria-label="Exit presentation">×</a>
        </div>
        <span class="slide-progress" style="width:${((index + 1) / slides.length) * 100}%"></span>
      </section>`;

    document.querySelector("[data-slide-prev]").addEventListener("click", () => moveSlide(-1));
    document.querySelector("[data-slide-next]").addEventListener("click", () => moveSlide(1));
    document.querySelector("[data-fullscreen]").addEventListener("click", toggleFullscreen);
    renderPresentationDiagram();
  }

  function moveSlide(delta) {
    const route = parseRoute();
    if (route.name !== "present") return;
    const hasAudience = route.parts.length > 1;
    const audienceId = hasAudience ? route.parts[0] : "";
    const current = Number.parseInt(route.parts[hasAudience ? 1 : 0] || "0", 10) || 0;
    const { audience, slides } = presentationContext(audienceId);
    const next = Math.min(Math.max(current + delta, 0), slides.length - 1);
    if (next !== current) location.hash = audience ? `#/present/${audience.id}/${next}` : `#/present/${next}`;
  }

  async function toggleFullscreen() {
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
      else await document.exitFullscreen();
    } catch (error) {
      announce("Fullscreen is unavailable in this browser view.");
    }
  }

  function renderNotFound(message = "That page could not be found.") {
    setPageTitle("Not found");
    setActiveNav("");
    main.innerHTML = `<div class="page-shell"><div class="error-state"><p class="eyebrow">404 / Not found</p><h1>Off the study map.</h1><p>${escapeHtml(message)}</p><a class="action-link" href="#/overview">Return to overview <span aria-hidden="true">→</span></a></div></div>`;
  }

  function focusRouteHeading() {
    const heading = main.querySelector("h1");
    if (!heading) return;
    heading.setAttribute("tabindex", "-1");
    requestAnimationFrame(() => heading.focus({ preventScroll: true }));
  }

  function route() {
    if (!state.manifest) return;
    closeMenu();
    closeSearch(false);
    const current = parseRoute();
    if (current.name !== "present") document.body.classList.remove("is-presenting");
    switch (current.name) {
      case "overview": renderOverview(); break;
      case "audiences": current.parts[0] ? renderAudience(current.parts[0]) : renderAudiences(); break;
      case "visuals": renderVisualAtlas(); break;
      case "library": renderLibrary(); break;
      case "compare": renderCompare(); break;
      case "architecture": renderArchitecture(); break;
      case "lab": renderLab(); break;
      case "doc": renderDocument(current.parts[0]); break;
      case "present": current.parts.length > 1 ? renderPresentation(current.parts[1], current.parts[0]) : renderPresentation(current.parts[0]); break;
      default: renderNotFound();
    }
    window.scrollTo(0, 0);
    focusRouteHeading();
  }

  function scoreSearchItem(item, query) {
    const term = query.toLowerCase().trim();
    if (!term) return 1;
    const words = term.split(/\s+/).filter(Boolean);
    const title = item.title.toLowerCase();
    const tags = (item.tags || []).join(" ").toLowerCase();
    const summary = item.summary.toLowerCase();
    const text = (item.searchText || "").toLowerCase();
    if (!words.every((word) => `${title} ${tags} ${summary} ${text}`.includes(word))) return -1;
    return words.reduce((score, word) => score + (title.includes(word) ? 8 : 0) + (tags.includes(word) ? 4 : 0) + (summary.includes(word) ? 2 : 0) + (text.includes(word) ? 1 : 0), 0);
  }

  function updateGlobalSearch() {
    const query = globalSearch.value;
    const audienceItems = (state.manifest.audiences || []).map((audience) => ({
      id: audience.id,
      title: `${audience.label} briefing`,
      summary: `${audience.framing} ${audience.decision}`,
      section: "Audience",
      type: "briefing",
      tags: [audience.group, audience.verb, ...(audience.questions || [])],
      searchText: `${audience.action} ${(audience.sourcePaths || []).join(" ")}`,
      href: `#/audiences/${encodeURIComponent(audience.id)}`,
    }));
    const candidates = [
      ...audienceItems.map((item) => ({ item, href: item.href, boost: 2 })),
      ...state.manifest.items.map((item) => ({ item, href: itemHref(item), boost: 0 })),
    ];
    const results = candidates
      .map((entry) => {
        const score = scoreSearchItem(entry.item, query);
        return { ...entry, score: score < 0 ? -1 : score + entry.boost };
      })
      .filter((entry) => entry.score >= 0)
      .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
      .slice(0, 12);
    globalResults.innerHTML = results.length
      ? results.map(({ item, href }) => `
          <a class="search-result" href="${escapeHtml(href)}">
            <span class="resource-meta">${escapeHtml(item.section)}</span>
            <strong>${escapeHtml(item.title)}</strong>
            <span class="resource-meta">${item.type === "briefing" ? "Briefing" : escapeHtml(formatType(item.type))}</span>
          </a>`).join("")
      : `<div class="empty-state" style="padding:2rem 1rem"><h2>No match.</h2><p>Try a platform, capability, or evidence term.</p></div>`;
  }

  function openSearch() {
    state.searchReturnFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    modalBackground.forEach((element) => { element.inert = true; });
    searchDialog.hidden = false;
    document.body.style.overflow = "hidden";
    globalSearch.value = "";
    updateGlobalSearch();
    setTimeout(() => globalSearch.focus(), 0);
  }

  function closeSearch(restoreFocus = true) {
    if (searchDialog.hidden) return;
    searchDialog.hidden = true;
    modalBackground.forEach((element) => { element.inert = false; });
    if (!document.body.classList.contains("is-presenting")) document.body.style.overflow = "";
    if (restoreFocus && state.searchReturnFocus && document.contains(state.searchReturnFocus)) state.searchReturnFocus.focus();
    state.searchReturnFocus = null;
  }

  function trapSearchFocus(event) {
    if (searchDialog.hidden || event.key !== "Tab") return false;
    const focusable = [...searchDialog.querySelectorAll("button:not([disabled]), input:not([disabled]), a[href]")]
      .filter((element) => !element.hidden && element.getClientRects().length);
    if (!focusable.length) return false;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
      return true;
    }
    if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
      return true;
    }
    return false;
  }

  async function init() {
    try {
      const response = await fetch("content-manifest.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`Manifest request returned ${response.status}`);
      state.manifest = await response.json();
      route();
    } catch (error) {
      setPageTitle("Build required");
      main.innerHTML = `<div class="page-shell"><div class="error-state"><p class="eyebrow">Site data unavailable</p><h1>Build the content index first.</h1><p>${escapeHtml(error.message)}</p><p>Run <code>make site</code>, then serve the generated <code>_site</code> directory.</p></div></div>`;
    }
  }

  menuToggle.addEventListener("click", () => {
    const open = !nav.classList.contains("is-open");
    nav.classList.toggle("is-open", open);
    menuToggle.setAttribute("aria-expanded", String(open));
  });
  document.querySelector("[data-search-trigger]").addEventListener("click", openSearch);
  document.querySelectorAll("[data-search-close]").forEach((button) => button.addEventListener("click", () => closeSearch()));
  globalSearch.addEventListener("input", updateGlobalSearch);
  window.addEventListener("hashchange", route);
  document.addEventListener("keydown", (event) => {
    if (trapSearchFocus(event)) return;
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openSearch();
      return;
    }
    if (event.key === "Escape") {
      if (!searchDialog.hidden) closeSearch();
      else if (document.body.classList.contains("is-presenting")) {
        const current = parseRoute();
        const { audience } = presentationContext(current.parts.length > 1 ? current.parts[0] : "");
        location.hash = presentationExitHref(audience);
      }
      return;
    }
    if (document.body.classList.contains("is-presenting")) {
      const interactive = event.target instanceof Element && event.target.closest("a, button, input, select, textarea, summary, [contenteditable='true']");
      if (interactive) return;
      if (["ArrowRight", "PageDown", " "].includes(event.key)) {
        event.preventDefault();
        moveSlide(1);
      } else if (["ArrowLeft", "PageUp"].includes(event.key)) {
        event.preventDefault();
        moveSlide(-1);
      } else if (event.key.toLowerCase() === "f") {
        event.preventDefault();
        toggleFullscreen();
      }
    }
  });

  init();
})();
