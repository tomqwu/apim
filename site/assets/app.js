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
    printSnapshot: null,
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

  function visualDisclosurePanel(index, eyebrow, title, note, body, extraClass = "", open = false) {
    return `
      <details class="visual-panel visual-disclosure ${escapeHtml(extraClass)}"${open ? " open" : ""}>
        <summary class="visual-panel-heading">
          <span class="section-index">${escapeHtml(index)} / ${escapeHtml(eyebrow)}</span>
          <h2>${escapeHtml(title)}</h2>
          <p>${escapeHtml(note)}</p>
          <span class="visual-disclosure-action" aria-hidden="true"><span class="when-closed">Open visual</span><span class="when-open">Close visual</span></span>
        </summary>
        <div class="visual-panel-body">${body}</div>
      </details>`;
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
    const variantTotal = Array.isArray(visuals.variants) ? visuals.variants.length : 0;
    const variantScope = variantTotal ? `all ${variantTotal} bounded archetypes` : "all bounded archetypes";
    const review = findByPath("reports/methodology-review.md");
    const referenceCase = findByPath("docs/41-enterprise-reference-case.md");
    const failureCasebook = findByPath("docs/42-public-failure-casebook.md");
    const industryProblems = findByPath("docs/43-api-management-industry-problems.md");
    const industryPractices = findByPath("docs/45-api-management-industry-practices.md");
    const kongMulticloud = findByPath("docs/44-kong-multicloud-study-roadmap.md");
    const kongPlatform = findByPath("docs/47-kong-enterprise-platform-strategy.md");
    const kongFacilitatorGuide = findByPath("docs/49-kong-guided-evaluation-facilitator-guide.md");
    const pocPlan = findByPath("poc/test-plan.md");
    const kongPlatformVisual = visuals.kongPlatformStrategy || {};
    const problemTotal = Number(visuals.industryProblems?.total) || 0;
    const practiceTotal = Number(visuals.industryPractices?.practiceTotal) || 0;
    const scenarioTotal = Number(visuals.industryPractices?.scenarioTotal) || 0;
    const kongWorkstreamTotal = Number(visuals.kongMulticloud?.workstreamTotal) || 0;
    const kongFitTotal = Number(kongPlatformVisual.fit?.rowTotal) || 0;
    const kongPhaseTotal = Number(kongPlatformVisual.roadmap?.rowTotal) || 0;
    const kongOutcomeTotal = Number(kongPlatformVisual.outcomes?.rowTotal) || 0;
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
              <a class="action-link is-primary" href="#/present/vp-executive/0">Start executive briefing <span aria-hidden="true">→</span></a>
              <a class="action-link" href="#/library">Explore the library <span aria-hidden="true">↗</span></a>
              <span class="resource-meta">Indexed ${escapeHtml(dateLabel)}</span>
            </div>
          </aside>
        </section>

        <section class="content-section overview-decision" aria-labelledby="overview-decision-title">
          <div class="section-heading">
            <span class="section-index">01 / Principal recommendation</span>
            <h2 id="overview-decision-title">Proceed with a bounded, reversible Kong foundation—not unproved production scale.</h2>
            <p>Treat Kong as the stakeholder-selected direction, freeze the exact self-managed hybrid option, and fund accountable foundation proof. Production fit, critical scale, support, recovery, and economics remain gated by representative evidence and explicit stop rules.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualDisclosurePanel("A", "Steering state", "The decision requested now", "The recommendation separates the stakeholder-selected direction, required benchmarks, production gates, and deferred scale commitments.", chartMarkup("recommendation", visuals.review || {}, { title: "Decision state", compact: true }), "is-wide is-only-panel", true)}
          </div>
          ${review ? `<a class="action-link" href="${itemHref(review)}">Open the principal review <span aria-hidden="true">↗</span></a>` : ""}
        </section>

        ${window.ApiStudyAudiences?.band ? window.ApiStudyAudiences.band(audiences) : ""}

        <section class="metric-strip" aria-label="Repository facts">
          ${metricMarkup(stats.studies, "assessment chapters")}
          ${metricMarkup(stats.diagrams, "architecture diagrams")}
          ${metricMarkup(stats.criteria, "decision criteria")}
          ${metricMarkup(stats.sources, "registered sources")}
          ${metricMarkup(stats.questions, "workshop questions")}
          ${metricMarkup(stats.apiContracts, "API contracts")}
          ${metricMarkup(stats.pocProtocolCases, "decision-grade experiment cases")}
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
            ${pocPlan ? `<a class="visual-source" href="${itemHref(pocPlan)}">Open scenario register <span>poc/test-plan.md ↗</span></a>` : ""}
          </div>
        </section>

        ${kongPlatform ? `
        <section class="content-section" aria-labelledby="kong-platform-strategy-title">
          <div class="section-heading">
            <span class="section-index">02 / Selected-platform posture</span>
            <h2 id="kong-platform-strategy-title">Deploy Kong as a platform service—and make self-managed control earn its cost.</h2>
            <p>The stakeholder direction concentrates work on Kong. The canonical strategy keeps that choice scenario-relative: ${kongFitTotal} fit conditions, ${kongPhaseTotal} gated phases, and ${kongOutcomeTotal} outcome contracts preserve counterfactuals, proof, a Konnect custody switch, and a true non-Kong exit.</p>
          </div>
          <div class="decision-visual-grid is-kong-platform-grid">
            ${visualDisclosurePanel("A", "Strategic fit", "Better here, under explicit conditions", "Scan all seven conditions, then inspect the complete counterfactual and proof contract for the condition that matters.", chartMarkup("kongPlatformFit", kongPlatformVisual.fit || {}, { title: "Seven outcome-fit conditions", compact: true, mode: "synopsis" }), "is-wide")}
            ${visualDisclosurePanel("B", "Adoption", "Foundation before scale", "KP0 through KP5 advance only through bounded outcome and recovery evidence; elapsed windows remain scenario assumptions.", chartMarkup("kongPlatformRoadmap", kongPlatformVisual.roadmap || {}, { title: "0–18 month evidence-gated roadmap", compact: true }), "is-wide")}
          </div>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${itemHref(kongPlatform)}">Open the Kong platform strategy <span aria-hidden="true">↗</span></a>
            <a class="action-link is-primary" href="#/present/kong-platform-journey-guided/0">Start the guided Kong evaluation <span aria-hidden="true">→</span></a>
            ${kongFacilitatorGuide ? `<a class="action-link is-primary" href="${itemHref(kongFacilitatorGuide)}">Open the facilitator guide <span aria-hidden="true">↗</span></a>` : ""}
            <a class="action-link is-primary" href="#/present/kong-platform-journey/0">Start the Kong platform journey <span aria-hidden="true">→</span></a>
            <a class="action-link" href="#/architecture">Inspect the target architecture <span aria-hidden="true">→</span></a>
            <a class="action-link" href="#/present/kong-technical-deep-dive/0">Start the technical deep dive <span aria-hidden="true">→</span></a>
            <a class="action-link" href="#/present/platform-teams/0">Start the platform-team briefing <span aria-hidden="true">→</span></a>
          </div>
        </section>` : ""}

        ${industryProblems && industryPractices && kongMulticloud ? `
        <section class="content-section" aria-labelledby="industry-agenda-title">
          <div class="section-heading">
            <span class="section-index">03 / Industry agenda</span>
            <h2 id="industry-agenda-title">Move from enduring problems to operating practices to option proof.</h2>
            <p>The cross-vendor taxonomy defines the outcomes. The practice study turns them into realistic operating cases, and the Kong roadmap converts the stakeholder-selected direction into bounded, reversible self-managed proof before production adoption.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualDisclosurePanel("A", "Problem system", `${problemTotal} problem families that outlive product packaging`, "Each problem connects enterprise exposure to the mechanisms vendors productize and the decision implication equivalent proof must resolve.", chartMarkup("problemMatrix", visuals.industryProblems || {}, { title: "Problem → mechanism map", compact: true }))}
            ${visualDisclosurePanel("B", "Operating practice", `${practiceTotal} practices across ${scenarioTotal} realistic cases`, industryPractices.summary, chartMarkup("scenarioMatrix", visuals.industryPractices || {}, { title: "Scenario → failure → best-practice control", compact: true }))}
            ${visualDisclosurePanel("C", "Kong study", `${kongWorkstreamTotal} gated workstreams`, "Exact options, owners, prerequisites, scenario ranges, and exit gates keep the selected direction reversible; Konnect and non-Kong exit remain explicit benchmarks.", chartMarkup("studyRoadmap", visuals.kongMulticloud || {}, { title: "Kong multicloud study sequence", compact: true }), "is-wide")}
          </div>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${itemHref(industryProblems)}">Open the industry problem study <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(industryPractices)}">Open practices and realistic cases <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(kongMulticloud)}">Open the Kong roadmap <span aria-hidden="true">↗</span></a>
          </div>
        </section>` : ""}

        ${referenceCase && failureCasebook ? `
        <section class="content-section" aria-labelledby="depth-title">
          <div class="section-heading">
            <span class="section-index">04 / Real-world depth</span>
            <h2 id="depth-title">Start with difficult behavior—not a feature list.</h2>
            <p>One shared enterprise case gives every option the same workloads, trust boundaries, traffic, failure history, recovery obligations, and migration constraints. Public postmortems then turn real failure mechanisms into mandatory proof.</p>
          </div>
          <div class="study-grid is-depth">
            <a class="study-card" href="${itemHref(referenceCase)}">
              <span class="card-label">01 / Synthetic reference case</span>
              <span class="card-count">RE-1</span>
              <h3>${escapeHtml(referenceCase.title)}</h3>
              <p>Six critical journeys, eight compound incidents, mixed Mule/PCF/AKS coexistence, stateful money movement, PKI, capacity, SLO, and rollback constraints.</p>
            </a>
            <a class="study-card" href="${itemHref(failureCasebook)}">
              <span class="card-label">02 / Documented incidents</span>
              <span class="card-count">${String(Number(stats.publicFailureCases || 0)).padStart(2, "0")}</span>
              <h3>${escapeHtml(failureCasebook.title)}</h3>
              <p>Configuration blast radius, latent software defects, state divergence, trust-chain compatibility, and generated-artifact failure converted into symmetric tests.</p>
            </a>
          </div>
        </section>` : ""}

        <section class="content-section" aria-labelledby="streams-title">
          <div class="section-heading">
            <span class="section-index">05 / Study streams</span>
            <h2 id="streams-title">One repository, six ways into the evidence.</h2>
            <p>Use the curated paths for orientation. Use Library when you need the complete source record.</p>
          </div>
          <div class="study-grid">
            ${featuredSections.map(studyCard).join("")}
          </div>
        </section>

        <section class="content-section" aria-labelledby="method-title">
          <div class="section-heading">
            <span class="section-index">06 / Method</span>
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
      await mermaidMarkup(text, target, "Vendor-neutral target-state architecture");
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
    targets.forEach((target) => {
      const card = target.closest(".architecture-card");
      if (!card || card.dataset.previewConfigured === "true") return;
      card.dataset.previewConfigured = "true";
      const label = target.dataset.diagramLabel || "Architecture diagram";
      card.setAttribute("aria-label", `${label}. Whole-model preview. Press Enter to open the companion note.`);
    });
    const load = async (target) => {
      if (target.dataset.rendered === "true") return;
      target.dataset.rendered = "true";
      try {
        const text = await fetchText(target.dataset.diagramPreview);
        await mermaidMarkup(text, target, target.dataset.diagramLabel || "Architecture diagram preview");
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

  async function renderKongPlatformArchitecture() {
    const target = document.querySelector("[data-kong-platform-target]");
    const model = state.manifest?.visuals?.kongPlatformStrategy?.architecture;
    if (!target) return;
    if (!model?.mermaid) {
      target.innerHTML = '<p class="visual-empty">The canonical KPS-1 model is unavailable.</p>';
      return;
    }
    await mermaidMarkup(model.mermaid, target, "KPS-1 — self-managed control and distributed runtime");
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
    const industryProblems = findByPath("docs/43-api-management-industry-problems.md");
    const industryPractices = findByPath("docs/45-api-management-industry-practices.md");
    const kongMulticloud = findByPath("docs/44-kong-multicloud-study-roadmap.md");
    const kongPlatform = findByPath("docs/47-kong-enterprise-platform-strategy.md");
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
          <p class="intro-note">A selection assumption is useful only when it can lose. Kong receives focused foundation work; production conclusions remain provisional until mandatory gates and stated acceptance tests close.</p>
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

        ${kongPlatform ? `
        <section class="content-section" aria-labelledby="selected-platform-posture-title">
          <div class="section-heading">
            <span class="section-index">01 / Selection assumption</span>
            <h2 id="selected-platform-posture-title">A Kong direction can focus investment without becoming retroactive proof.</h2>
            <p>Kong is the stakeholder-selected planning direction. The platform strategy shows why it fits the stated custody and multicloud outcomes, what would change that answer, and which evidence gates stop production fit or critical scale.</p>
          </div>
          <div class="decision-visual-grid is-kong-platform-grid">
            ${visualPanel("A", "Conditional fit", "Why Kong is better for this scenario", "Scan the seven outcome and mechanism pairs; open a condition to test its advantage, counterfactual, and proof obligation.", chartMarkup("kongPlatformFit", visuals.kongPlatformStrategy?.fit || {}, { title: "Outcome-fit contract", compact: true, mode: "synopsis" }), "is-wide")}
            ${visualPanel("B", "P1–P10", "The selected platform still has to earn every outcome", "Kong responses remain tied to measures and mandatory hold conditions; no problem is marked solved by preference.", chartMarkup("kongPlatformProblems", visuals.kongPlatformStrategy?.problems || {}, { title: "Problem-to-proof traceability", compact: true }), "is-wide")}
          </div>
          <a class="action-link is-primary" href="${itemHref(kongPlatform)}">Open the bounded Kong platform strategy <span aria-hidden="true">↗</span></a>
        </section>` : ""}

        ${industryProblems && industryPractices && kongMulticloud ? `
        <section class="content-section" aria-labelledby="problem-comparison-title">
          <div class="section-heading">
            <span class="section-index">02 / Problem frame</span>
            <h2 id="problem-comparison-title">Compare how exact options answer the same enduring problems.</h2>
            <p>The taxonomy remains canonical and cross-vendor. Kong is the bounded planning direction; Konnect and alternative platforms remain counterfactual, sensitivity, custody-switch, migration, and true-exit benchmarks.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualPanel("A", "Industry problems", "The comparison denominator", "Vendor features matter only where they change an enterprise outcome under representative conditions.", chartMarkup("problemMatrix", visuals.industryProblems || {}, { title: "Problem → mechanism → decision test", compact: true }))}
            ${visualPanel("B", "Industry practice", industryPractices.title, industryPractices.summary, chartMarkup("practiceFramework", visuals.industryPractices || {}, { title: "Problem → practice contract", compact: true }))}
            ${visualPanel("C", "Kong roadmap", "A bounded proof sequence", "The workstreams expose contract, topology, security, runtime, product, economics, migration, and exit dependencies that a gateway demo cannot close.", chartMarkup("studyRoadmap", visuals.kongMulticloud || {}, { title: "Kong workstreams and gates", compact: true }), "is-wide")}
          </div>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${itemHref(industryProblems)}">Open the canonical problem taxonomy <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(industryPractices)}">Open practices and realistic cases <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(kongMulticloud)}">Open the Kong multicloud roadmap <span aria-hidden="true">↗</span></a>
          </div>
        </section>` : ""}

        <section class="content-section" aria-labelledby="decision-views-title">
          <div class="section-heading">
            <span class="section-index">03 / Decision views</span>
            <h2 id="decision-views-title">See what can—and cannot—be concluded.</h2>
            <p>The visual model separates candidate status, evidence confidence, research balance, and gate structure.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualPanel("A", "Recommendation", "Bounded Kong direction, gated scale", "Kong is the strategic platform assumption for reversible foundation work; production fit and critical scale remain blocked until the mandatory gates close.", chartMarkup("recommendation", visuals.review || {}, { title: "Decision state" }), "is-wide")}
            ${visualPanel("B", "Options", "Bounded deployment archetypes", "Family-level scores would hide topology and entitlement differences; each archetype remains unscored until its Gate-1 bill of materials closes.", chartMarkup("statusMatrix", visuals.variants || [], { title: "Option-resolution status", nameHeader: "Option" }), "is-wide")}
            ${visualPanel("C", "Evidence", "Confidence ladder", "Higher confidence requires execution under representative conditions.", chartMarkup("evidenceLadder", visuals.methodology?.evidenceLevels || [], { title: "Evidence levels" }))}
            ${visualPanel("D", "Research", "Registered-source balance", "Volume is visible; criterion-level traceability still determines fitness for scoring.", chartMarkup("sourceBalance", visuals.sources || {}, { title: "Sources by vendor" }))}
          </div>
        </section>

        <section class="content-section" aria-labelledby="platforms-title">
          <div class="section-heading">
            <span class="section-index">04 / Platform lenses</span>
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
    const visuals = state.manifest.visuals || {};
    const industryProblems = findByPath("docs/43-api-management-industry-problems.md");
    const industryPractices = findByPath("docs/45-api-management-industry-practices.md");
    const kongMulticloud = findByPath("docs/44-kong-multicloud-study-roadmap.md");
    const kongPlatform = findByPath("docs/47-kong-enterprise-platform-strategy.md");
    const kongFacilitatorGuide = findByPath("docs/49-kong-guided-evaluation-facilitator-guide.md");
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
        ${kongPlatform ? `
        <section class="content-section" aria-labelledby="kong-platform-architecture-title">
          <div class="section-heading">
            <span class="section-index">Selected platform / target and gates</span>
            <h2 id="kong-platform-architecture-title">Self-managed control is a platform operating model, not an installation topology.</h2>
            <p>KPS-1 keeps approved configuration authority and PostgreSQL inside an enterprise management boundary while distributing request runtimes and failure containment. The roadmap and P1–P10 response keep recovery, trust, business outcome, staffing, and exit obligations visible.</p>
          </div>
          <div class="decision-visual-grid is-kong-platform-grid">
            ${visualDisclosurePanel("A", "KPS-1 target", "Self-managed control, distributed runtime", "Rendered directly from the canonical doc47 Mermaid figure; exact products, regions, replicas, entitlements, capacity, and achieved availability remain unresolved.", '<div class="kps-architecture-target diagram-frame" data-kong-platform-target data-diagram-id="KPS-1" data-diagram-summary="One reviewed configuration authority reaches an enterprise management cell while request runtimes and evidence remain close to workloads; exact products, regions, replicas, capacity, entitlements, and achieved availability remain proof obligations."><p>Rendering canonical KPS-1…</p></div>', "is-wide", true)}
            ${visualDisclosurePanel("B", "P1–P10", "Architecture remains accountable to outcomes", "Every Kong platform response retains a measure and mandatory hold condition.", chartMarkup("kongPlatformProblems", visuals.kongPlatformStrategy?.problems || {}, { title: "Problem-to-proof traceability", compact: true }), "is-wide")}
            ${visualDisclosurePanel("C", "Adoption", "Scale only through recovery and outcome proof", "Six evidence gates preserve stop, replan, Konnect custody-switch, and non-Kong exit paths.", chartMarkup("kongPlatformRoadmap", visuals.kongPlatformStrategy?.roadmap || {}, { title: "0–18 month platform sequence", compact: true }), "is-wide")}
          </div>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${itemHref(kongPlatform)}">Open the canonical platform strategy <span aria-hidden="true">↗</span></a>
            <a class="action-link is-primary" href="#/present/kong-platform-journey-guided/0">Start the guided Kong evaluation <span aria-hidden="true">→</span></a>
            ${kongFacilitatorGuide ? `<a class="action-link is-primary" href="${itemHref(kongFacilitatorGuide)}">Open the facilitator guide <span aria-hidden="true">↗</span></a>` : ""}
            <a class="action-link is-primary" href="#/present/kong-platform-journey/0">Start the Kong platform journey <span aria-hidden="true">→</span></a>
            <a class="action-link" href="#/present/kong-technical-deep-dive/0">Start the Kong technical deep dive <span aria-hidden="true">→</span></a>
          </div>
        </section>` : ""}
        ${industryProblems && industryPractices && kongMulticloud ? `
        <section class="content-section" aria-labelledby="multicloud-strategy-title">
          <div class="section-heading">
            <span class="section-index">Strategy / problem to proof</span>
            <h2 id="multicloud-strategy-title">A multicloud topology is only one layer of the decision.</h2>
            <p>Use the enduring-problem taxonomy to define what the architecture must accomplish, then use the Kong roadmap to resolve plane placement, authority, failure domains, operations, economics, migration, and exit.</p>
          </div>
          <div class="decision-visual-grid">
            ${visualDisclosurePanel("A", "Architecture pressure", "What every candidate topology must answer", "The canonical frame prevents a clean control/data-plane picture from hiding consumer, governance, evidence, operating-model, or exit obligations.", chartMarkup("problemMatrix", visuals.industryProblems || {}, { title: "Enduring problem system", compact: true }))}
            ${visualDisclosurePanel("B", "Failure cases", industryPractices.title, industryPractices.summary, chartMarkup("scenarioMatrix", visuals.industryPractices || {}, { title: "Scenario → failure → operating control", compact: true }))}
            ${visualDisclosurePanel("C", "Study sequence", "How the selected Kong direction earns production confidence", "Workstreams advance through prerequisite and exit gates; production fit and critical scale remain blocked until the canonical outcome evidence closes.", chartMarkup("studyRoadmap", visuals.kongMulticloud || {}, { title: "Kong multicloud study roadmap", compact: true }), "is-wide")}
          </div>
          <div class="hero-actions">
            <a class="action-link is-primary" href="${itemHref(industryProblems)}">Open industry problems <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(industryPractices)}">Open operating practices <span aria-hidden="true">↗</span></a>
            <a class="action-link" href="${itemHref(kongMulticloud)}">Open Kong roadmap <span aria-hidden="true">↗</span></a>
          </div>
        </section>` : ""}
        <section class="content-section">
          <div class="section-heading">
            <span class="section-index">${String(diagrams.length).padStart(2, "0")} / Diagrams</span>
            <h2>Different views of one evolving system.</h2>
            <p>Use each diagram with its companion architecture note; diagrams are models, not deployment evidence.</p>
          </div>
          <div class="architecture-grid">
            ${diagrams.map((item, index) => `
              <a class="architecture-card" href="${item.companionId ? `#/doc/${encodeURIComponent(item.companionId)}` : itemHref(item)}">
                <div class="architecture-preview" data-diagram-preview="${escapeHtml(item.contentUrl)}" data-diagram-label="${escapeHtml(item.title)}" aria-label="Preview of ${escapeHtml(item.title)}"><p>Rendering model…</p></div>
                <span class="card-label">${String(index + 1).padStart(2, "0")} / ${item.companionId ? "Companion note + source" : "Mermaid source"}</span>
                <h2>${escapeHtml(item.title)}</h2>
                <p>${escapeHtml(item.summary)}</p>
              </a>`).join("")}
          </div>
        </section>
      </div>`;
    renderDiagramPreviews();
    renderKongPlatformArchitecture();
  }

  function renderLab() {
    const stats = state.manifest.stats;
    const visuals = state.manifest.visuals || {};
    const pocPlan = findByPath("poc/test-plan.md");
    const pocStatuses = Array.isArray(visuals.poc?.byStatus) ? visuals.poc.byStatus : [];
    const pocStatusCount = (label) => Number(pocStatuses.find((item) => String(item?.label || "").toLowerCase() === label.toLowerCase())?.value) || 0;
    const pocAutomated = pocStatusCount("Automated");
    const pocNotRun = pocStatusCount("Not run");
    const pocScenarioHeadline = `${pocAutomated} baseline ${pocAutomated === 1 ? "check is" : "checks are"} automated; ${pocNotRun} ${pocNotRun === 1 ? "scenario is" : "scenarios are"} not run`;
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
            <div class="lab-step"><span class="card-label">03 / Exercise</span><strong>${stats.pocProtocolCases} atomic cases</strong><p>Real-world, portal, and observability protocols are distinct from ${stats.pocScenarios} aggregate status-register items.</p></div>
            <div class="lab-step"><span class="card-label">04 / Record</span><strong>Evidence first</strong><p>Acceptance criteria distinguish execution proof from product documentation.</p></div>
          </div>
          <div class="lab-visuals">
            ${visualPanel("A", "Scenario state", pocScenarioHeadline, "This is a local evidence boundary, not proof of production fit.", `${chartMarkup("pocStatus", visuals.poc || {})}${pocPlan ? `<a class="visual-source" href="${itemHref(pocPlan)}">Open scenario register <span>poc/test-plan.md ↗</span></a>` : ""}`)}
            ${visualPanel("B", "Evidence path", "Automation does not equal representative evidence", "Each result should move confidence only as far as its environment and artifacts support.", chartMarkup("evidenceLadder", visuals.methodology?.evidenceLevels || [], { title: "Evidence confidence" }))}
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
        const destination = document.getElementById(link.getAttribute("href").slice(1));
        revealDocumentSection(destination);
        destination?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }

    container.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#/")) return;
      const destination = document.getElementById(href.slice(1));
      if (!destination) return;
      event.preventDefault();
      revealDocumentSection(destination);
      destination.scrollIntoView({ behavior: "smooth", block: "start" });
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
      const fragmentIndex = href.indexOf("#");
      const fragment = fragmentIndex >= 0 ? href.slice(fragmentIndex + 1) : "";
      const repoPath = normalizeRepoPath(item.path, href);
      const target = findByPath(repoPath);
      link.href = target
        ? `${itemHref(target)}${fragment ? `?anchor=${encodeURIComponent(fragment)}` : ""}`
        : `content/${repoPath}${fragment ? `#${fragment}` : ""}`;
    });

    container.querySelectorAll("img[src]").forEach((image) => {
      const src = image.getAttribute("src");
      if (!src || /^(https?:|data:)/i.test(src)) return;
      image.src = `content/${normalizeRepoPath(item.path, src)}`;
      image.loading = "lazy";
    });

    container.querySelectorAll("table").forEach((table, index) => {
      table.classList.add("editorial-table");
      const profiles = sizeTableColumns(table) || [];

      const headerCells = [...table.querySelectorAll("thead th")];
      const headers = headerCells.map((cell, columnIndex) => {
        cell.scope = "col";
        cell.id = `${item.id}-table-${index + 1}-column-${columnIndex + 1}`;
        return cell.textContent.trim();
      });
      const bodyRows = [...table.querySelectorAll("tbody tr")];
      const totalProfileWidth = profiles.reduce((total, profile) => total + profile.width, 0);
      const isDefinition = headers.length === 2 && bodyRows.length <= 30;
      const isSwitchable = headers.length >= 2 && headers.length <= 6 && bodyRows.length <= 18
        || isDefinition;
      const isWideArtifact = headers.length >= 4 || totalProfileWidth >= 56;
      bodyRows.forEach((row, rowIndex) => {
        const cells = [...row.children];
        cells.forEach((cell, columnIndex) => {
          if (headers[columnIndex]) {
            cell.dataset.columnLabel = headers[columnIndex];
            cell.setAttribute("headers", headerCells[columnIndex].id);
          }
          if (isSwitchable) {
            const value = document.createElement("span");
            value.className = "table-card-value";
            while (cell.firstChild) value.appendChild(cell.firstChild);
            cell.appendChild(value);
          }
        });
        if (isSwitchable && cells.length) {
          const profiledSummaryIndex = profiles.findIndex((profile, columnIndex) => columnIndex > 0
            && ["compact", "number", "date", "identifier"].includes(profile.kind));
          const summaryIndex = isDefinition ? 1 : profiledSummaryIndex > 0 ? profiledSummaryIndex : cells.length > 1 ? 1 : -1;
          const canCollapse = !isDefinition && summaryIndex > 0;
          const initiallyExpanded = isDefinition || !canCollapse || bodyRows.length <= 3 && rowIndex === 0;
          row.dataset.rowExpanded = String(initiallyExpanded);
          cells[0].classList.add("is-row-key-cell");
          if (summaryIndex > 0) cells[summaryIndex].classList.add("is-row-summary-cell");
          if (canCollapse) {
            const rowLabel = cells[0].querySelector(".table-card-value")?.textContent.trim() || `row ${rowIndex + 1}`;
            const toggle = document.createElement("button");
            toggle.type = "button";
            toggle.className = "table-row-toggle";
            toggle.dataset.rowToggle = "";
            toggle.setAttribute("aria-expanded", String(initiallyExpanded));
            toggle.setAttribute("aria-label", `${initiallyExpanded ? "Hide" : "Show"} all fields for ${rowLabel}`);
            toggle.textContent = initiallyExpanded ? "Hide fields" : "Show all fields";
            cells[0].querySelector(".table-card-value")?.append(toggle);
          }
        }
      });

      const region = document.createElement("figure");
      region.className = "table-region article-table";
      region.classList.toggle("is-switchable", isSwitchable);
      region.classList.toggle("is-definition-table", isDefinition);
      region.classList.toggle("is-artifact-wide", isWideArtifact);
      region.classList.toggle("artifact-shell", isWideArtifact);
      region.dataset.tableMinRem = String(totalProfileWidth);
      const viewport = document.createElement("div");
      viewport.className = "table-viewport";
      const wrapper = document.createElement("div");
      wrapper.className = "table-wrap";
      wrapper.setAttribute("role", "region");
      wrapper.setAttribute("aria-label", `Table ${index + 1} in ${item.title}`);
      const hint = document.createElement("p");
      hint.className = "table-scroll-hint";
      hint.hidden = true;
      hint.innerHTML = '<span aria-hidden="true">↔</span> Scroll to compare every field';

      const toolbar = document.createElement("div");
      toolbar.className = "table-view-toolbar";
      toolbar.setAttribute("role", "toolbar");
      toolbar.setAttribute("aria-label", `Table ${index + 1} presentation`);
      const readingButton = document.createElement("button");
      readingButton.type = "button";
      readingButton.dataset.tableMode = "reading";
      readingButton.textContent = "Read rows";
      const comparisonButton = document.createElement("button");
      comparisonButton.type = "button";
      comparisonButton.dataset.tableMode = "comparison";
      comparisonButton.textContent = "Compare columns";
      const tableStatus = document.createElement("output");
      tableStatus.className = "table-view-status";
      tableStatus.setAttribute("aria-live", "polite");
      toolbar.append(readingButton, comparisonButton, tableStatus);

      table.parentNode.insertBefore(region, table);
      if (isSwitchable) region.append(toolbar);
      region.append(viewport, hint);
      viewport.appendChild(wrapper);
      wrapper.appendChild(table);
      activateArticleTable(region);
    });
  }

  function revealDocumentSection(destination) {
    const section = destination?.closest?.(".document-section");
    if (!section || section.dataset.sectionOpen === "true") return;
    section.querySelector("[data-document-section-toggle]")?.click();
  }

  function enhanceDocumentSections(container, item) {
    const headings = [...container.querySelectorAll(":scope > h2")];
    const tableTotal = container.querySelectorAll(":scope > .article-table, :scope > .table-region").length;
    const diagramTotal = container.querySelectorAll(":scope > .inline-diagram").length;
    const proseLength = container.textContent.length;
    const longForm = headings.length >= 7
      && (tableTotal >= 4 || diagramTotal >= 3 || proseLength >= 20000);
    if (!longForm) return;

    const directChildren = [...container.children];
    const groups = headings.map((heading, index) => {
      const start = directChildren.indexOf(heading);
      const next = index + 1 < headings.length ? directChildren.indexOf(headings[index + 1]) : directChildren.length;
      return { heading, children: directChildren.slice(start + 1, next) };
    });
    const controls = document.createElement("div");
    controls.className = "document-section-controls artifact-shell";
    controls.setAttribute("role", "toolbar");
    controls.setAttribute("aria-label", `${item.title} section controls`);
    controls.innerHTML = `<span>Long-form study · open only the evidence you need</span><button type="button" data-sections-expand>Expand all</button><button type="button" data-sections-collapse>Collapse all</button><output aria-live="polite"></output>`;

    const sections = groups.map(({ heading, children }, index) => {
      const headingTitle = heading.textContent.replace(/\s+/g, " ").trim();
      heading.setAttribute("aria-label", headingTitle);
      const section = document.createElement("section");
      section.className = "document-section";
      section.dataset.sectionOpen = String(index < 2);
      section.dataset.sectionTitle = headingTitle;
      const body = document.createElement("div");
      body.className = "document-section-body";
      body.id = `${heading.id}-content`;
      body.hidden = index >= 2;
      const toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "document-section-toggle";
      toggle.dataset.documentSectionToggle = "";
      toggle.setAttribute("aria-controls", body.id);
      toggle.setAttribute("aria-expanded", String(index < 2));
      toggle.setAttribute("aria-label", `${index < 2 ? "Collapse" : "Expand"} section: ${headingTitle}`);
      toggle.innerHTML = `<span class="when-closed">Open section</span><span class="when-open">Close section</span>`;
      container.insertBefore(section, heading);
      section.append(heading, body);
      heading.append(toggle);
      children.forEach((child) => body.append(child));
      return section;
    });

    sections[0].before(controls);
    container.classList.add("has-collapsible-sections");
    const status = controls.querySelector("output");
    const sync = () => {
      const openTotal = sections.filter((section) => section.dataset.sectionOpen === "true").length;
      status.value = `${openTotal} of ${sections.length} sections open`;
      status.textContent = status.value;
    };
    const setSection = (section, open) => {
      const body = section.querySelector(":scope > .document-section-body");
      const toggle = section.querySelector("[data-document-section-toggle]");
      section.dataset.sectionOpen = String(open);
      if (body) body.hidden = !open;
      toggle?.setAttribute("aria-expanded", String(open));
      toggle?.setAttribute("aria-label", `${open ? "Collapse" : "Expand"} section: ${section.dataset.sectionTitle}`);
    };
    sections.forEach((section) => {
      section.querySelector("[data-document-section-toggle]")?.addEventListener("click", () => {
        setSection(section, section.dataset.sectionOpen !== "true");
        sync();
      });
    });
    controls.querySelector("[data-sections-expand]").addEventListener("click", () => {
      sections.forEach((section) => setSection(section, true));
      sync();
    });
    controls.querySelector("[data-sections-collapse]").addEventListener("click", () => {
      sections.forEach((section) => setSection(section, false));
      sync();
    });
    sync();
  }

  function focusDocumentAnchor(anchor) {
    if (!anchor) return;
    let id = anchor;
    try {
      id = decodeURIComponent(anchor);
    } catch (error) {
      // Keep a malformed-but-literal fragment usable instead of failing the route.
    }
    const destination = document.getElementById(id);
    if (!destination) return;
    revealDocumentSection(destination);
    destination.setAttribute("tabindex", "-1");
    requestAnimationFrame(() => {
      destination.scrollIntoView({ behavior: "auto", block: "start" });
      destination.focus({ preventScroll: true });
    });
  }

  function inlineDiagramContract(original, documentTitle, index) {
    let cursor = original.previousElementSibling;
    let figureId = `${documentTitle} — diagram ${index + 1}`;
    let summary = "";
    let inspected = 0;
    while (cursor && cursor.tagName !== "H2" && inspected < 10) {
      const text = cursor.textContent.replace(/\s+/g, " ").trim();
      if (!summary) {
        const equivalent = [...cursor.querySelectorAll?.("li") || []]
          .map((item) => item.textContent.replace(/\s+/g, " ").trim())
          .find((value) => /^Accessible equivalent:/i.test(value));
        if (equivalent) summary = equivalent.replace(/^Accessible equivalent:\s*/i, "");
      }
      if (/^Figure\s+[A-Z0-9-]+\s+[—-]/i.test(text)) figureId = text;
      cursor = cursor.previousElementSibling;
      inspected += 1;
    }
    cursor = original.nextElementSibling;
    inspected = 0;
    while (!summary && cursor && cursor.tagName !== "H2" && inspected < 5) {
      const text = cursor.textContent.replace(/\s+/g, " ").trim();
      if (/^(Accessible equivalent|Figure interpretation):/i.test(text)) {
        summary = text.replace(/^(Accessible equivalent|Figure interpretation):\s*/i, "");
      }
      cursor = cursor.nextElementSibling;
      inspected += 1;
    }
    return { figureId, summary };
  }

  async function renderInlineMermaid(container, documentTitle = "Document") {
    const blocks = [...container.querySelectorAll("pre code.language-mermaid")];
    for (const [index, code] of blocks.entries()) {
      const source = code.textContent || "";
      const original = code.closest("pre");
      if (!original || !source.trim()) continue;
      const contract = inlineDiagramContract(original, documentTitle, index);
      const figure = document.createElement("figure");
      figure.className = "inline-diagram artifact-shell";
      const frame = document.createElement("div");
      frame.className = "diagram-frame";
      if (contract.summary) frame.dataset.diagramSummary = contract.summary;
      frame.dataset.diagramId = contract.figureId;
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
      await mermaidMarkup(source, frame, contract.figureId);
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

  const fieldAcronyms = new Map([
    ["api", "API"],
    ["id", "ID"],
    ["rpo", "RPO"],
    ["rps", "RPS"],
    ["rto", "RTO"],
    ["slo", "SLO"],
    ["url", "URL"],
  ]);

  function humanizeFieldName(value) {
    return String(value || "Field")
      .trim()
      .split(/[_\s-]+/)
      .filter(Boolean)
      .map((word, index) => fieldAcronyms.get(word.toLowerCase())
        || (index === 0 ? `${word.charAt(0).toUpperCase()}${word.slice(1).toLowerCase()}` : word.toLowerCase()))
      .join(" ");
  }

  function percentileLength(values, percentile = 0.85) {
    const lengths = values
      .map((value) => String(value || "").replace(/\s+/g, " ").trim().length)
      .filter(Boolean)
      .sort((left, right) => left - right);
    if (!lengths.length) return 0;
    return lengths[Math.min(lengths.length - 1, Math.floor((lengths.length - 1) * percentile))];
  }

  function tableColumnProfile(header, values) {
    const key = String(header || "").toLowerCase().replace(/[^a-z0-9]+/g, "_");
    const sampleLength = Math.max(key.length, percentileLength(values));
    const isNumeric = /(^|_)(score|weight|count|rps|size|duration|priority|capacity)($|_)/.test(key)
      && values.every((value) => !String(value).trim() || Number.isFinite(Number(value)));
    if (isNumeric) return { kind: "number", width: 8 };
    if (/(^|_)(url)($|_)/.test(key)) return { kind: "url", width: 28 };
    if (/(^|_)(date|access_date|review_date|target_date|fresh_until)($|_)/.test(key)) return { kind: "date", width: 11 };
    if (/(^|_)(id)($|_)/.test(key)) return { kind: "identifier", width: Math.min(15, Math.max(10, Math.ceil(sampleLength * 0.58))) };
    if (/(^|_)(status|state|level|type|category|vendor|product|wave|criticality|environment|classification)($|_)/.test(key)) {
      return { kind: "compact", width: Math.min(15, Math.max(10, Math.ceil(sampleLength * 0.52))) };
    }
    if (/(claim|criterion|requirement|evidence|acceptance|test|description|problem|remediation|implication|limitation|assumption|dependency|mitigation|outcome|notes|scope|responsibilit|rollback|reconciliation|decommission)/.test(key)) {
      return { kind: "narrative", width: Math.min(27, Math.max(19, Math.ceil(sampleLength * 0.42))) };
    }
    return { kind: "standard", width: Math.min(20, Math.max(10, Math.ceil(sampleLength * 0.5))) };
  }

  function sizeTableColumns(table, suppliedHeaders = null) {
    if (!table) return [];
    const headers = suppliedHeaders || [...table.querySelectorAll("thead th")].map((cell) => cell.dataset.field || cell.textContent.trim());
    if (!headers.length) return [];
    const bodyRows = [...table.querySelectorAll("tbody tr:not(.data-detail-row)")];
    const profiles = headers.map((header, index) => tableColumnProfile(
      header,
      bodyRows.map((row) => row.children[index]?.textContent || ""),
    ));
    const group = document.createElement("colgroup");
    profiles.forEach((profile) => {
      const column = document.createElement("col");
      column.className = `table-column table-column--${profile.kind}`;
      column.style.width = `${profile.width}rem`;
      group.appendChild(column);
    });
    table.querySelector("colgroup")?.remove();
    const caption = table.querySelector(":scope > caption");
    if (caption) caption.after(group);
    else table.prepend(group);
    table.style.setProperty("--table-min-width", `${profiles.reduce((total, profile) => total + profile.width, 0)}rem`);
    table.querySelectorAll("tr").forEach((row) => {
      [...row.children].forEach((cell, index) => {
        if (profiles[index]) cell.dataset.columnKind = profiles[index].kind;
      });
    });
    return profiles;
  }

  function updateTableRegion(region) {
    const wrappers = [...(region?.querySelectorAll(".table-wrap") || [])];
    const wrapper = wrappers.find((candidate) => candidate.offsetParent !== null) || wrappers[0];
    if (!wrapper) return;
    const hasHorizontalOverflow = wrapper.scrollWidth > wrapper.clientWidth + 2;
    const hasVerticalOverflow = wrapper.scrollHeight > wrapper.clientHeight + 2;
    region.classList.toggle("has-horizontal-overflow", hasHorizontalOverflow);
    region.classList.toggle("can-scroll-left", hasHorizontalOverflow && wrapper.scrollLeft > 2);
    region.classList.toggle("can-scroll-right", hasHorizontalOverflow && wrapper.scrollLeft < wrapper.scrollWidth - wrapper.clientWidth - 2);
    const hint = region.querySelector(":scope > .table-scroll-hint");
    if (hint) hint.hidden = !hasHorizontalOverflow;
    wrapper.tabIndex = hasHorizontalOverflow || hasVerticalOverflow ? 0 : -1;
  }

  function activateTableRegion(region) {
    const wrappers = [...(region?.querySelectorAll(".table-wrap") || [])];
    if (!wrappers.length) return;
    wrappers.forEach((wrapper) => wrapper.addEventListener("scroll", () => updateTableRegion(region), { passive: true }));
    requestAnimationFrame(() => updateTableRegion(region));
  }

  function setArticleTableMode(region, mode, userSelected = false) {
    if (!region?.classList.contains("is-switchable")) return;
    const reading = mode === "reading";
    region.classList.toggle("is-reading-mode", reading);
    region.classList.toggle("is-comparison-mode", !reading);
    if (userSelected) region.dataset.userTableMode = mode;
    region.querySelectorAll("[data-table-mode]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.tableMode === mode));
    });
    const status = region.querySelector(".table-view-status");
    if (status) {
      status.value = reading
        ? region.classList.contains("is-definition-table")
          ? "Definition rows · all fields shown"
          : "Row summaries · expand for detail"
        : "Column comparison view";
      status.textContent = status.value;
    }
    const wrapper = region.querySelector(".table-wrap");
    if (reading && wrapper) wrapper.scrollLeft = 0;
    requestAnimationFrame(() => updateTableRegion(region));
  }

  function activateArticleTable(region) {
    activateTableRegion(region);
    if (!region?.classList.contains("is-switchable")) return;
    let lastDefaultMode = "";
    const useResponsiveDefault = () => {
      if (region.dataset.userTableMode) return;
      const rootFontSize = Number.parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
      const comparisonWidth = (Number.parseFloat(region.dataset.tableMinRem) || 0) * rootFontSize;
      const availableWidth = region.getBoundingClientRect().width;
      const mode = availableWidth < 900 || comparisonWidth > availableWidth + 2 ? "reading" : "comparison";
      if (mode === lastDefaultMode) return;
      lastDefaultMode = mode;
      setArticleTableMode(region, mode);
    };
    region.addEventListener("click", (event) => {
      const mode = event.target.closest("[data-table-mode]")?.dataset.tableMode;
      if (mode) setArticleTableMode(region, mode, true);
      const rowToggle = event.target.closest("[data-row-toggle]");
      if (!rowToggle) return;
      const row = rowToggle.closest("tr");
      const expanded = row?.dataset.rowExpanded !== "true";
      if (!row) return;
      row.dataset.rowExpanded = String(expanded);
      rowToggle.setAttribute("aria-expanded", String(expanded));
      const rowLabel = row.querySelector(".is-row-key-cell .table-card-value")?.childNodes[0]?.textContent?.trim() || "this row";
      rowToggle.setAttribute("aria-label", `${expanded ? "Hide" : "Show"} all fields for ${rowLabel}`);
      rowToggle.textContent = expanded ? "Hide fields" : "Show all fields";
    });
    new ResizeObserver(useResponsiveDefault).observe(region);
    useResponsiveDefault();
  }

  let tableResizeFrame = null;
  window.addEventListener("resize", () => {
    cancelAnimationFrame(tableResizeFrame);
    tableResizeFrame = requestAnimationFrame(() => {
      document.querySelectorAll(".table-region").forEach((region) => updateTableRegion(region));
    });
  });

  function activateDataGrid(container) {
    const grid = container.querySelector(".data-grid");
    const tables = [...(grid?.querySelectorAll(".data-table") || [])];
    if (!grid || !tables.length) return;
    tables.forEach((table) => sizeTableColumns(table, [...table.querySelectorAll("thead th")].map((cell) => cell.dataset.field || "")));
    activateTableRegion(grid);

    grid.querySelectorAll("[data-grid-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        const mode = button.dataset.gridMode;
        grid.querySelectorAll("[data-grid-mode]").forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
        grid.querySelectorAll("[data-grid-view]").forEach((view) => {
          view.hidden = view.dataset.gridView !== mode;
        });
        requestAnimationFrame(() => updateTableRegion(grid));
      });
    });

    const filter = grid.querySelector("[data-grid-filter]");
    const output = grid.querySelector("[data-grid-count]");
    const empty = grid.querySelector("[data-grid-empty]");
    const sourceRows = [...(grid.querySelectorAll(".data-table--full tbody tr[data-record-index]").length
      ? grid.querySelectorAll(".data-table--full tbody tr[data-record-index]")
      : grid.querySelectorAll("tbody tr[data-record-row]"))];
    if (!filter || !output) return;
    const update = () => {
      const query = filter.value.trim().toLocaleLowerCase();
      let visible = 0;
      sourceRows.forEach((row) => {
        const matches = !query || row.textContent.toLocaleLowerCase().includes(query);
        grid.querySelectorAll(`[data-record-index="${row.dataset.recordIndex}"]`).forEach((candidate) => {
          candidate.hidden = !matches;
        });
        if (matches) visible += 1;
      });
      output.textContent = `Showing ${visible} of ${sourceRows.length} ${sourceRows.length === 1 ? "record" : "records"}`;
      if (empty) empty.hidden = visible !== 0;
      updateTableRegion(grid);
    };
    filter.addEventListener("input", update);
  }

  function findHeaderIndexes(headers, names) {
    const normalized = headers.map((header) => String(header).trim().toLowerCase());
    return names.map((name) => normalized.indexOf(name)).filter((index, position, indexes) => index >= 0 && indexes.indexOf(index) === position);
  }

  function datasetColumnViews(headers, item) {
    const path = item?.path || "";
    let primary = [];
    if (path === "decision-matrix/criteria.csv") {
      primary = findHeaderIndexes(headers, ["criterion_id", "criterion", "category", "requirement_type", "default_weight", "status"]);
    } else if (path === "reports/content-remediation-backlog.csv") {
      primary = findHeaderIndexes(headers, ["recommendation_id", "priority", "workstream", "status", "owner_role", "target_gate"]);
    } else if (path === "research/sources.csv") {
      primary = findHeaderIndexes(headers, ["source_id", "vendor", "product", "title", "access_date"]);
    } else if (path === "reports/source-coverage.csv") {
      primary = findHeaderIndexes(headers, ["document_path", "registry_state", "source_id", "host"]);
    } else if (headers.length > 8) {
      const preferred = [
        /(^|_)id$/,
        /(^|_)(name|title|criterion|recommendation|claim)($|_)/,
        /(^|_)priority($|_)/,
        /(^|_)(category|workstream|type)($|_)/,
        /(^|_)(status|state)($|_)/,
        /(^|_)(owner|owner_role|gate|score)($|_)/,
      ];
      primary.push(0);
      preferred.forEach((pattern) => {
        const index = headers.findIndex((header, candidate) => !primary.includes(candidate) && pattern.test(String(header).toLowerCase()));
        if (index >= 0 && primary.length < 6) primary.push(index);
      });
      for (let index = 0; index < headers.length && primary.length < 6; index += 1) {
        if (!primary.includes(index)) primary.push(index);
      }
    }
    const details = headers.map((_, index) => index).filter((index) => !primary.includes(index));
    return { primary, details, usesDisclosure: primary.length > 0 && details.length > 0 };
  }

  function csvHeaderMarkup(headers, indexes) {
    return indexes.map((index) => `<th scope="col" data-field="${escapeHtml(headers[index])}"><abbr title="Source field: ${escapeHtml(headers[index])}">${escapeHtml(humanizeFieldName(headers[index]))}</abbr></th>`).join("");
  }

  function csvRecordCells(row, indexes) {
    return indexes.map((index, position) => position === 0
      ? `<th scope="row" class="data-row-key">${escapeHtml(row[index])}</th>`
      : `<td>${escapeHtml(row[index])}</td>`).join("");
  }

  function csvTableMarkup(headers, records, indexes, title, modifier = "full") {
    return `<table class="data-table editorial-table data-table--${modifier}">
      <caption>${escapeHtml(title)}: ${records.length} ${records.length === 1 ? "record" : "records"} across ${indexes.length} visible ${indexes.length === 1 ? "field" : "fields"}.</caption>
      <thead><tr>${csvHeaderMarkup(headers, indexes)}</tr></thead>
      <tbody>${records.map((row, recordIndex) => `<tr data-record-row data-record-index="${recordIndex}">${csvRecordCells(row, indexes)}</tr>`).join("")}</tbody>
    </table>`;
  }

  function csvReadingTableMarkup(headers, records, primary, details, title) {
    return `<table class="data-table editorial-table data-table--reading">
      <caption>${escapeHtml(title)} reading view. Each record exposes ${primary.length} primary fields and ${details.length} additional fields in an expandable disclosure.</caption>
      <thead><tr>${csvHeaderMarkup(headers, primary)}</tr></thead>
      <tbody>${records.map((row, recordIndex) => `<tr data-record-row data-record-index="${recordIndex}">${csvRecordCells(row, primary)}</tr>
        <tr class="data-detail-row" data-record-index="${recordIndex}"><td colspan="${primary.length}">
          <details class="data-record-details"><summary><span>Supporting fields</span><small>${details.length} ${details.length === 1 ? "field" : "fields"}</small></summary>
            <dl>${details.map((index) => `<div><dt>${escapeHtml(humanizeFieldName(headers[index]))}</dt><dd>${row[index] ? escapeHtml(row[index]) : '<span class="data-empty-value">Not supplied</span>'}</dd></div>`).join("")}</dl>
          </details>
        </td></tr>`).join("")}</tbody>
    </table>`;
  }

  function csvSchemaMarkup(headers, gridId) {
    return `<section class="schema-dictionary" aria-labelledby="${gridId}-schema-title">
      <header><span class="data-grid-kicker">Reusable schema</span><h3 id="${gridId}-schema-title">Field dictionary</h3><p>This template has no sample records. The complete schema is shown below instead of as an empty wide grid.</p></header>
      <dl>${headers.map((header, index) => {
        const profile = tableColumnProfile(header, []);
        return `<div><dt><span>${String(index + 1).padStart(2, "0")}</span>${escapeHtml(humanizeFieldName(header))}</dt><dd><code>${escapeHtml(header)}</code><span>${escapeHtml(profile.kind === "narrative" ? "Narrative field" : profile.kind === "identifier" ? "Identifier" : profile.kind === "date" ? "Date" : profile.kind === "number" ? "Number" : "Structured field")}</span></dd></div>`;
      }).join("")}</dl>
    </section>`;
  }

  function csvMarkup(text, item) {
    const rows = parseCsv(text);
    if (!rows.length) return "<p>The dataset is empty.</p>";
    const width = Math.max(...rows.map((row) => row.length));
    const normalized = rows.map((row) => [...row, ...Array(Math.max(0, width - row.length)).fill("")]);
    const headers = normalized[0];
    const records = normalized.slice(1);
    const gridId = `dataset-${slug(item?.id || item?.title || "records")}`;
    const title = item?.title || "Dataset";
    const views = datasetColumnViews(headers, item);
    const guide = views.usesDisclosure
      ? "Start with the primary fields. Scroll the grid to compare them, expand a record for supporting fields, or open the full grid."
      : "Scroll rows and compare every field in the bounded grid.";
    return `
      <section class="table-region data-grid" aria-labelledby="${gridId}-title">
        <header class="data-grid-heading">
          <div>
            <span class="data-grid-kicker">Structured dataset</span>
            <h2 id="${gridId}-title">${escapeHtml(title)}</h2>
          </div>
          <p class="data-grid-summary"><strong>${records.length}</strong> ${records.length === 1 ? "record" : "records"}<span aria-hidden="true">/</span><strong>${headers.length}</strong> ${headers.length === 1 ? "field" : "fields"}</p>
          <p class="data-grid-guide" id="${gridId}-guide">${escapeHtml(guide)}</p>
        </header>
        ${records.length ? `<div class="data-grid-tools">
          <label class="data-grid-filter" for="${gridId}-filter"><span>Find in dataset</span><input id="${gridId}-filter" type="search" placeholder="Filter all records" autocomplete="off" data-grid-filter></label>
          <output class="data-grid-count" for="${gridId}-filter" aria-live="polite" data-grid-count>Showing ${records.length} of ${records.length} ${records.length === 1 ? "record" : "records"}</output>
          ${views.usesDisclosure ? `<div class="data-grid-modes" role="group" aria-label="Dataset view"><button type="button" aria-pressed="true" data-grid-mode="reading">Reading view</button><button type="button" aria-pressed="false" data-grid-mode="full">Full grid</button></div>` : ""}
        </div>` : ""}
        ${records.length ? `${views.usesDisclosure ? `<div class="table-viewport" data-grid-view="reading"><div class="table-wrap" role="region" aria-labelledby="${gridId}-title" aria-describedby="${gridId}-guide">${csvReadingTableMarkup(headers, records, views.primary, views.details, title)}</div></div>
          <div class="table-viewport" data-grid-view="full" hidden><div class="table-wrap" role="region" aria-labelledby="${gridId}-title" aria-describedby="${gridId}-guide">${csvTableMarkup(headers, records, headers.map((_, index) => index), title)}</div></div>`
          : `<div class="table-viewport" data-grid-view="full"><div class="table-wrap" role="region" aria-labelledby="${gridId}-title" aria-describedby="${gridId}-guide">${csvTableMarkup(headers, records, headers.map((_, index) => index), title)}</div></div>`}
        <p class="table-scroll-hint"><span aria-hidden="true">↔</span> Scroll inside the grid to reach every visible field</p>` : csvSchemaMarkup(headers, gridId)}
        <p class="data-grid-empty" data-grid-empty hidden>No records match this filter.</p>
      </section>`;
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

  function wrapSvgLabel(value, maximumCharacters) {
    const words = String(value || "").replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
    const lines = [];
    let line = "";
    words.forEach((word) => {
      const candidate = line ? `${line} ${word}` : word;
      if (line && candidate.length > maximumCharacters) {
        lines.push(line);
        line = word;
      } else {
        line = candidate;
      }
    });
    if (line) lines.push(line);
    return lines.length ? lines : ["Diagram node"];
  }

  function htmlSvgLabelText(root) {
    const chunks = [];
    const boundaries = new Set(["br", "div", "p", "li", "section"]);
    const visit = (node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        chunks.push(node.nodeValue || "");
        return;
      }
      const name = String(node.localName || node.nodeName || "").toLowerCase();
      const boundary = boundaries.has(name);
      if (boundary) chunks.push(" ");
      [...node.childNodes].forEach(visit);
      if (boundary) chunks.push(" ");
    };
    visit(root);
    return chunks.join("").replace(/\s+/g, " ").trim();
  }

  function replaceHtmlSvgLabels(svgMarkup) {
    const namespace = "http://www.w3.org/2000/svg";
    const template = document.createElement("template");
    template.innerHTML = String(svgMarkup || "").trim();
    const svg = template.content.querySelector("svg");
    if (!svg) return svgMarkup;
    // Mermaid currently emits HTML-backed labels even when flowchart
    // `htmlLabels` is disabled. XML tag lookup is case-sensitive, while the
    // emitted spelling has varied between Mermaid/browser combinations. Find
    // the element by local name so every variant is converted to SVG text
    // before DOMPurify removes foreign content.
    [...svg.querySelectorAll("*")]
      .filter((element) => String(element.localName || element.tagName || "").toLowerCase() === "foreignobject")
      .forEach((foreignObject) => {
        const width = Number.parseFloat(foreignObject.getAttribute("width")) || 200;
        const height = Number.parseFloat(foreignObject.getAttribute("height")) || 48;
        const lines = wrapSvgLabel(htmlSvgLabelText(foreignObject), Math.max(12, Math.floor(width / 7.2)));
        const text = document.createElementNS(namespace, "text");
        text.setAttribute("class", "mermaid-svg-label");
        text.setAttribute("x", String(width / 2));
        text.setAttribute("y", String(height / 2));
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("dominant-baseline", "central");
        lines.forEach((line, index) => {
          const tspan = document.createElementNS(namespace, "tspan");
          tspan.setAttribute("x", String(width / 2));
          tspan.setAttribute("dy", index === 0 ? `${-0.55 * (lines.length - 1)}em` : "1.1em");
          tspan.textContent = line;
          text.appendChild(tspan);
        });
        foreignObject.replaceWith(text);
      });
    return svg.outerHTML;
  }

  function padSvgViewBox(svg, padding = {}) {
    const values = (svg.getAttribute("viewBox") || "").trim().split(/\s+/).map(Number);
    if (values.length !== 4 || values.some((value) => !Number.isFinite(value))) return;
    const [x, y, width, height] = values;
    if (width <= 0 || height <= 0) return;
    const left = Math.max(0, Number(padding.left) || 0);
    const right = Math.max(0, Number(padding.right) || 0);
    const top = Math.max(0, Number(padding.top) || 0);
    const bottom = Math.max(0, Number(padding.bottom) || 0);
    svg.setAttribute("viewBox", `${x - left} ${y - top} ${width + left + right} ${height + top + bottom}`);
    svg.style.overflow = "visible";
    svg.dataset.viewBoxPadded = "true";
  }

  function measuredSvgPadding(svg, selector, margin = 12) {
    const values = (svg.getAttribute("viewBox") || "").trim().split(/\s+/).map(Number);
    const svgRect = svg.getBoundingClientRect();
    if (
      values.length !== 4
      || values.some((value) => !Number.isFinite(value))
      || svgRect.width <= 0
      || svgRect.height <= 0
    ) return null;
    const contentRects = [...svg.querySelectorAll(selector)]
      .map((node) => node.getBoundingClientRect())
      .filter((rect) => rect.width > 0 || rect.height > 0);
    if (!contentRects.length) return null;
    const [, , viewWidth, viewHeight] = values;
    const unitsPerPixelX = viewWidth / svgRect.width;
    const unitsPerPixelY = viewHeight / svgRect.height;
    const minLeft = Math.min(...contentRects.map((rect) => rect.left));
    const maxRight = Math.max(...contentRects.map((rect) => rect.right));
    const minTop = Math.min(...contentRects.map((rect) => rect.top));
    const maxBottom = Math.max(...contentRects.map((rect) => rect.bottom));
    return {
      left: Math.max(0, margin - ((minLeft - svgRect.left) * unitsPerPixelX)),
      right: Math.max(0, margin - ((svgRect.right - maxRight) * unitsPerPixelX)),
      top: Math.max(0, margin - ((minTop - svgRect.top) * unitsPerPixelY)),
      bottom: Math.max(0, margin - ((svgRect.bottom - maxBottom) * unitsPerPixelY)),
    };
  }

  function medianNumber(values, fallback) {
    if (!values.length) return fallback;
    const ordered = [...values].sort((left, right) => left - right);
    const middle = Math.floor(ordered.length / 2);
    return ordered.length % 2 ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
  }

  function diagramGeometry(svg) {
    const viewBox = svg.viewBox?.baseVal;
    const width = viewBox?.width || Number.parseFloat(svg.getAttribute("width")) || svg.getBoundingClientRect().width || 1;
    const height = viewBox?.height || Number.parseFloat(svg.getAttribute("height")) || svg.getBoundingClientRect().height || 1;
    const fontSizes = [...svg.querySelectorAll("text")]
      .map((node) => Number.parseFloat(getComputedStyle(node).fontSize))
      .filter((value) => Number.isFinite(value) && value > 0);
    return { width, height, labelSize: medianNumber(fontSizes, 18) };
  }

  function setDiagramWidth(svg, naturalWidth, scale) {
    const safeScale = Math.max(0.05, Math.min(3, scale));
    svg.style.width = `${Math.ceil(naturalWidth * safeScale)}px`;
    svg.style.maxWidth = "none";
    svg.style.height = "auto";
    return safeScale;
  }

  function diagramContentWidth(element) {
    const styles = getComputedStyle(element);
    const padding = Number.parseFloat(styles.paddingLeft) + Number.parseFloat(styles.paddingRight);
    return Math.max(1, element.clientWidth - padding);
  }

  function configureDiagram(target, svg, label, options = {}) {
    const geometry = diagramGeometry(svg);
    const isPreview = target.classList.contains("architecture-preview");
    const isPresentation = target.classList.contains("slide-diagram");
    const minimumLabel = isPresentation ? 18 : isPreview ? 14 : 16;
    const initialWidth = diagramContentWidth(target);
    const semanticSummary = String(target.dataset.diagramSummary || "").trim();
    const semanticFigureId = String(target.dataset.diagramId || label || "Canonical model").trim();
    const authoredOverview = String(options.authoredOverview || "").trim();
    const hasAuthoredOverview = Boolean(authoredOverview);
    const denseOverview = geometry.labelSize * Math.min(1, initialWidth / geometry.width) < minimumLabel;
    const hasSemanticSummary = Boolean(semanticSummary || hasAuthoredOverview);

    if (isPreview) {
      const previewStyles = getComputedStyle(target);
      const previewHeight = Math.max(1, target.clientHeight
        - Number.parseFloat(previewStyles.paddingTop)
        - Number.parseFloat(previewStyles.paddingBottom));
      setDiagramWidth(svg, geometry.width, Math.min(1, initialWidth / geometry.width, previewHeight / geometry.height));
      target.classList.add("is-overview-mode");
      target.setAttribute("aria-label", `${label}. Whole-diagram preview; open the companion note to inspect the source.`);
      return;
    }

    target.classList.add("diagram-frame");

    const toolbar = document.createElement("div");
    toolbar.className = "diagram-toolbar";
    toolbar.setAttribute("role", "toolbar");
    toolbar.setAttribute("aria-label", `${label} zoom controls`);
    const viewport = document.createElement("div");
    viewport.className = "diagram-scroll";
    viewport.tabIndex = 0;
    viewport.setAttribute("role", "region");
    viewport.setAttribute("aria-label", `${label}. Scroll horizontally and vertically to inspect the diagram.`);
    viewport.addEventListener("keydown", (event) => {
      const horizontalOverflow = viewport.scrollWidth > viewport.clientWidth + 2;
      const verticalOverflow = viewport.scrollHeight > viewport.clientHeight + 2;
      const horizontalStep = Math.max(48, Math.round(viewport.clientWidth * 0.22));
      const verticalStep = Math.max(64, Math.round(viewport.clientHeight * 0.7));
      if (horizontalOverflow && ["ArrowLeft", "ArrowRight"].includes(event.key)) {
        event.preventDefault();
        event.stopPropagation();
        viewport.scrollLeft += event.key === "ArrowRight" ? horizontalStep : -horizontalStep;
        return;
      }
      if (verticalOverflow && ["ArrowUp", "ArrowDown", "PageUp", "PageDown", " "].includes(event.key)) {
        event.preventDefault();
        event.stopPropagation();
        const backwards = event.key === "ArrowUp" || event.key === "PageUp" || event.shiftKey && event.key === " ";
        viewport.scrollTop += backwards ? -verticalStep : verticalStep;
      }
    });
    const status = document.createElement("output");
    status.className = "diagram-zoom-status";
    status.setAttribute("aria-live", "polite");

    const makeButton = (text, action, accessibleLabel) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = text;
      button.dataset.diagramAction = action;
      button.setAttribute("aria-label", accessibleLabel);
      return button;
    };
    const summaryButton = hasSemanticSummary
      ? makeButton(hasAuthoredOverview ? "Overview" : "Takeaway", "summary", hasAuthoredOverview ? "Show the source-derived architecture overview" : "Show the authored takeaway for this diagram")
      : null;
    const overview = makeButton(hasAuthoredOverview ? "Full model" : "Overview", "overview", "Show the whole canonical diagram at the available width");
    const readable = makeButton("Readable", "readable", "Open a readable, scrollable inspection view");
    const actual = makeButton("100%", "actual", "Show the diagram at its natural size");
    const out = makeButton("−", "out", "Zoom out");
    const zoomIn = makeButton("+", "in", "Zoom in");
    const expand = makeButton("Expand", "expand", "Open the diagram in an expanded canvas");
    const note = document.createElement("span");
    note.className = "diagram-mode-note";
    if (summaryButton) toolbar.append(summaryButton);
    toolbar.append(overview, readable);
    if (!isPresentation) toolbar.append(actual, out, zoomIn);
    toolbar.append(expand, note, status);
    const summaryPanel = document.createElement("div");
    summaryPanel.className = "diagram-summary";
    if (hasAuthoredOverview) {
      summaryPanel.classList.add("has-authored-overview");
      summaryPanel.innerHTML = window.DOMPurify ? window.DOMPurify.sanitize(authoredOverview) : authoredOverview;
      target.classList.add("has-authored-overview");
    } else if (hasSemanticSummary) {
      const kicker = document.createElement("span");
      kicker.textContent = `${semanticFigureId} · decision brief`;
      const heading = document.createElement("strong");
      heading.textContent = "What this model means";
      const copy = document.createElement("p");
      copy.textContent = semanticSummary;
      const instruction = document.createElement("small");
      instruction.textContent = "Choose Readable for the full model at presentation-safe type, or Expand for focused inspection.";
      summaryPanel.append(kicker, heading, copy, instruction);
    }
    target.replaceChildren(toolbar);
    if (hasSemanticSummary) target.append(summaryPanel);
    target.append(viewport);
    viewport.appendChild(svg);

    let lastAvailableSize = "";
    let scale = 1;
    const defaultMode = isPresentation && hasSemanticSummary ? "summary" : "overview";
    let mode = defaultMode;
    let expanded = false;
    let inertSiblings = [];
    let originPlaceholder = null;

    const availableWidth = () => diagramContentWidth(viewport);
    const availableHeight = () => {
      const styles = getComputedStyle(viewport);
      return Math.max(1, viewport.clientHeight
        - Number.parseFloat(styles.paddingTop)
        - Number.parseFloat(styles.paddingBottom));
    };
    const overviewScale = () => Math.min(
      1,
      availableWidth() / geometry.width,
      isPresentation ? availableHeight() / geometry.height : 1,
    );
    const readableScale = () => Math.max(Math.min(1, availableWidth() / geometry.width), minimumLabel / geometry.labelSize);

    const update = () => {
      scale = setDiagramWidth(svg, geometry.width, scale);
      const modeLabel = mode === "summary" ? "Summary" : mode === "overview" ? "Overview" : mode === "readable" ? "Readable" : mode === "actual" ? "Actual size" : "Custom";
      status.value = mode === "summary" ? `${hasAuthoredOverview ? "Overview" : "Summary"} · full model available` : `${modeLabel} · ${Math.round(scale * 100)}%`;
      status.textContent = status.value;
      if (summaryButton) summaryButton.setAttribute("aria-pressed", String(mode === "summary"));
      overview.setAttribute("aria-pressed", String(mode === "overview"));
      readable.setAttribute("aria-pressed", String(mode === "readable"));
      actual.setAttribute("aria-pressed", String(mode === "actual"));
      expand.setAttribute("aria-pressed", String(expanded));
      expand.textContent = expanded ? "Close" : "Expand";
      expand.setAttribute("aria-label", expanded ? "Close the expanded diagram canvas" : "Open the diagram in an expanded canvas");
      target.classList.toggle("is-summary-mode", mode === "summary");
      target.classList.toggle("is-overview-mode", mode === "overview");
      target.classList.toggle("is-inspection-mode", !["summary", "overview"].includes(mode));
      target.classList.toggle("is-expanded", expanded);
      document.body.classList.toggle("has-expanded-diagram", Boolean(document.querySelector(".diagram-frame.is-expanded")));
      if (hasSemanticSummary) summaryPanel.hidden = mode !== "summary";
      viewport.hidden = mode === "summary";
      viewport.tabIndex = ["summary", "overview"].includes(mode) ? -1 : 0;
      const renderedLabel = geometry.labelSize * scale;
      note.textContent = mode === "summary"
        ? hasAuthoredOverview ? "Source-derived overview" : "Decision brief"
        : mode === "overview" && renderedLabel < minimumLabel
        ? "Whole model · choose Readable to inspect labels"
        : mode === "overview" ? "Whole model" : "Scroll the canvas to inspect detail";
      viewport.setAttribute("aria-label", mode === "overview"
        ? `${label}. Whole-diagram overview.`
        : `${label}. Readable inspection canvas; scroll horizontally and vertically as needed.`);
    };

    const setExpanded = (nextExpanded, restoreFocus = true, deferLayout = true) => {
      expanded = nextExpanded;
      if (expanded) {
        originPlaceholder = document.createComment("expanded diagram origin");
        target.before(originPlaceholder);
        document.body.append(target);
        inertSiblings = [];
        [...document.body.children].forEach((sibling) => {
          if (sibling === target || sibling.inert) return;
          sibling.inert = true;
          inertSiblings.push(sibling);
        });
        target.setAttribute("role", "dialog");
        target.setAttribute("aria-modal", "true");
        target.setAttribute("aria-label", `${label} expanded diagram`);
        target.tabIndex = -1;
      } else {
        inertSiblings.forEach((element) => { element.inert = false; });
        inertSiblings = [];
        if (originPlaceholder?.parentNode) originPlaceholder.replaceWith(target);
        originPlaceholder = null;
        target.removeAttribute("role");
        target.removeAttribute("aria-modal");
        target.removeAttribute("aria-label");
        target.removeAttribute("tabindex");
      }
      update();
      if (!deferLayout) return;
      requestAnimationFrame(() => {
        if (mode === "overview") scale = overviewScale();
        else if (mode === "readable") scale = readableScale();
        update();
        if (expanded || restoreFocus) {
          setTimeout(() => expand.focus({ preventScroll: true }), 0);
        }
      });
    };

    target.addEventListener("diagram-close-request", (event) => {
      if (expanded) setExpanded(
        false,
        event.detail?.restoreFocus !== false,
        event.detail?.deferLayout !== false,
      );
    });

    toolbar.addEventListener("click", (event) => {
      const action = event.target.closest("button")?.dataset.diagramAction;
      if (!action) return;
      if (action === "summary") {
        mode = "summary";
        viewport.scrollTo({ left: 0, top: 0 });
      } else if (action === "overview") {
        mode = "overview";
        scale = overviewScale();
        viewport.scrollTo({ left: 0, top: 0 });
      } else if (action === "readable") {
        mode = "readable";
        update();
        requestAnimationFrame(() => {
          scale = readableScale();
          update();
        });
        return;
      } else if (action === "actual") {
        mode = "actual";
        scale = 1;
      } else if (action === "out") {
        mode = "custom";
        scale /= 1.2;
      } else if (action === "in") {
        mode = "custom";
        scale *= 1.2;
      } else if (action === "expand") {
        if (!expanded && mode === "summary") {
          mode = "readable";
          update();
          requestAnimationFrame(() => {
            scale = readableScale();
            setExpanded(true);
          });
        } else {
          setExpanded(!expanded);
        }
        return;
      }
      update();
    });
    target.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && expanded) {
        event.preventDefault();
        event.stopPropagation();
        setExpanded(false);
        return;
      }
      if (event.key !== "Tab" || !expanded) return;
      const focusable = [...target.querySelectorAll("button:not([disabled]), [tabindex='0']")];
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    const resizeObserver = new ResizeObserver(() => {
      const width = availableWidth();
      const height = availableHeight();
      const size = `${Math.round(width)}×${Math.round(height)}`;
      if (size === lastAvailableSize) return;
      lastAvailableSize = size;
      if (mode === "summary") return;
      if (mode === "overview") scale = overviewScale();
      else if (mode === "readable") scale = readableScale();
      update();
    });
    resizeObserver.observe(viewport);
    scale = defaultMode === "summary" ? 1 : defaultMode === "readable" ? readableScale() : overviewScale();
    update();
  }

  async function mermaidMarkup(text, target, label = "Mermaid diagram") {
    if (!window.mermaid) {
      target.innerHTML = `<pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
      return;
    }
    try {
      const authoredOverview = target.querySelector("template[data-diagram-overview]")?.innerHTML || "";
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        fontFamily: "Inter, Arial, sans-serif",
        flowchart: { htmlLabels: false, useMaxWidth: true },
        sequence: { useMaxWidth: true },
        themeVariables: {
          fontSize: "18px",
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
      const textLabelSvg = replaceHtmlSvgLabels(result.svg);
      target.innerHTML = window.DOMPurify ? window.DOMPurify.sanitize(textLabelSvg, { USE_PROFILES: { svg: true, svgFilters: true } }) : textLabelSvg;
      const svg = target.querySelector("svg");
      if (svg) {
        // Mermaid uses intentionally unlabelled structural nodes for state
        // starts/ends, forks, joins, and choices. Those shapes do not create a
        // label group; only fail when a node that is meant to carry a label
        // loses its text during SVG normalization or sanitization.
        const blankNodes = [...svg.querySelectorAll("g.node")].filter((node) => node.querySelector(".label") && !node.textContent.trim());
        if (blankNodes.length) {
          throw new Error(`Rendered diagram is missing ${blankNodes.length} node label${blankNodes.length === 1 ? "" : "s"}.`);
        }
        // Mermaid's xychart renderer positions the rotated y-axis title just
        // outside its own root viewBox. Give that chart family a real canvas
        // margin so the label remains visible in scroll containers, screenshots,
        // and print output instead of relying on overflow leaking from the SVG.
        if (/^\s*xychart-beta\b/m.test(text)) {
          padSvgViewBox(svg, { left: 44, right: 12, top: 12, bottom: 18 });
        }
        if (/^\s*pie\b/m.test(text)) {
          const padding = measuredSvgPadding(svg, ".pieTitleText, .pieCircle, .slice, .legend", 12);
          if (padding) padSvgViewBox(svg, padding);
        }
        const namespace = "http://www.w3.org/2000/svg";
        const titleId = `${id}-title`;
        const descriptionId = `${id}-description`;
        const title = document.createElementNS(namespace, "title");
        const description = document.createElementNS(namespace, "desc");
        title.id = titleId;
        title.textContent = label;
        description.id = descriptionId;
        description.textContent = "Rendered from the repository Mermaid source. The adjacent source disclosure contains the complete text model.";
        svg.prepend(description);
        svg.prepend(title);
        svg.removeAttribute("aria-hidden");
        svg.setAttribute("role", "img");
        svg.setAttribute("aria-labelledby", `${titleId} ${descriptionId}`);
        configureDiagram(target, svg, label, { authoredOverview });
      }
    } catch (error) {
      target.innerHTML = `<div class="error-state"><h1>Diagram source could not render.</h1><p>${escapeHtml(error.message)}</p><pre class="code-view"><code>${escapeHtml(text)}</code></pre></div>`;
    }
  }

  function documentScaffold(item) {
    const isMethodologyReview = item.path === "reports/methodology-review.md";
    return `
      <article class="document-shell${item.type === "csv" ? " is-dataset" : ""}${isMethodologyReview ? " is-methodology-review" : ""}">
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
            ${item.companionId ? `<a class="action-link" href="#/doc/${encodeURIComponent(item.companionId)}">Open companion note <span aria-hidden="true">↗</span></a>` : ""}
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

  function embedDocumentVisualContext(item, prose) {
    const markup = documentVisualContext(item);
    if (!markup) return;
    const template = document.createElement("template");
    template.innerHTML = markup.trim();
    const context = template.content.firstElementChild;
    if (!context) return;
    context.classList.add("is-inline", "artifact-shell");
    const firstHeading = prose.querySelector("h2");
    let anchor = firstHeading || prose.querySelector("p, ol, ul, .table-wrap, blockquote") || prose.firstElementChild;
    if (firstHeading) {
      while (anchor.nextElementSibling && anchor.nextElementSibling.tagName !== "H2") anchor = anchor.nextElementSibling;
    }
    if (anchor) anchor.after(context);
    else prose.prepend(context);
  }

  function embedDocumentVisualPlacements(item, prose) {
    const placements = window.ApiStudyCharts?.documentPlacements?.(item, state.manifest.visuals || {}) || [];
    let inserted = 0;
    placements.forEach((placement) => {
      const heading = prose.querySelector(`#${CSS.escape(placement.headingId || "")}`);
      if (!heading) return;
      const template = document.createElement("template");
      template.innerHTML = String(placement.markup || "").trim();
      const visual = template.content.firstElementChild;
      if (!visual) return;
      visual.classList.add("artifact-shell");
      let anchor = heading;
      let cursor = heading.nextElementSibling;
      while (cursor && cursor.tagName !== "H2") {
        anchor = cursor;
        if (cursor.classList.contains("table-region")) break;
        cursor = cursor.nextElementSibling;
      }
      anchor.after(visual);
      inserted += 1;
    });
    prose.dataset.visualPlacements = `${inserted}/${placements.length}`;
  }

  async function renderDocument(id, anchor = "") {
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
        target.innerHTML = `<div class="prose">${markdownToHtml(text)}</div>`;
        const prose = target.querySelector(".prose");
        enhanceMarkdown(prose, item);
        await renderInlineMermaid(prose, item.title);
        embedDocumentVisualContext(item, prose);
        embedDocumentVisualPlacements(item, prose);
        enhanceDocumentSections(prose, item);
      } else if (item.type === "csv") {
        target.innerHTML = `${csvMarkup(text, item)}${documentVisualContext(item)}`;
        activateDataGrid(target);
        document.querySelector("[data-document-rail]").innerHTML = "<span>Structured dataset</span>";
      } else if (item.type === "mermaid") {
        target.innerHTML = `<div class="diagram-frame" data-diagram-frame><p>Rendering diagram…</p></div><h2>Mermaid source</h2><pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
        document.querySelector("[data-document-rail]").innerHTML = "<span>Rendered model</span><a href=\"#diagram-source\">Source</a>";
        document.querySelector("[data-document-rail] a").addEventListener("click", (event) => {
          event.preventDefault();
          document.getElementById("diagram-source")?.scrollIntoView({ behavior: "smooth", block: "start" });
        });
        target.querySelector("h2").id = "diagram-source";
        await mermaidMarkup(text, target.querySelector("[data-diagram-frame]"), item.title);
      } else if (item.type === "openapi") {
        target.innerHTML = `<div class="prose">${openApiMarkup(text, item)}</div>`;
        enhanceMarkdown(target.querySelector(".prose"), item);
      } else if (item.type === "html") {
        target.innerHTML = `<div class="empty-state"><h2>HTML presentation or prototype</h2><p>Open this resource in a separate tab to use its native interactions.</p><a class="action-link is-primary" href="${escapeHtml(item.contentUrl)}" target="_blank" rel="noreferrer">Open HTML <span aria-hidden="true">↗</span></a></div>`;
      } else {
        target.innerHTML = `<pre class="code-view"><code>${escapeHtml(text)}</code></pre>`;
        document.querySelector("[data-document-rail]").innerHTML = `<span>${escapeHtml(formatType(item.type))} source</span>`;
      }
      if (token === state.renderToken) focusDocumentAnchor(anchor);
    } catch (error) {
      target.innerHTML = `<div class="error-state"><h1>Source unavailable.</h1><p>${escapeHtml(error.message)}</p></div>`;
    }
  }

  function presentationVisualMarkup(slide, source, isJourneyDeck = false) {
    const visuals = state.manifest.visuals || {};
    const options = { presentation: true, compact: true, title: isJourneyDeck ? slide.title : slide.metricLabel };
    const selected = (rows, idKey = "id") => {
      const ids = Array.isArray(slide.rowIds) ? new Set(slide.rowIds) : null;
      return Array.isArray(rows) ? rows.filter((row) => !ids || ids.has(row?.[idKey])) : [];
    };
    switch (slide.visual) {
      case "composition": return chartMarkup("composition", visuals.library || {}, options);
      case "methodologyFlow": return chartMarkup("methodologyFlow", visuals.methodology?.steps || [], options);
      case "stackedBars": return chartMarkup("stackedBars", visuals.criteria?.categories || [], { ...options, keys: ["mandatory", "weighted"] });
      case "statusMatrix": return chartMarkup("statusMatrix", visuals.variants || [], options);
      case "architectureDiagram": return presentationArchitectureMarkup(slide, source);
      case "donut": return chartMarkup("donut", visuals.criteria?.statuses || [], { ...options, total: visuals.criteria?.total, centerLabel: "criteria" });
      case "sourceBalance": return chartMarkup("sourceBalance", visuals.sources || {}, options);
      case "pocStatus": return chartMarkup("pocStatus", visuals.poc || {}, { ...options, title: `${Number(visuals.poc?.total) || 0} aggregate status-register items` });
      case "roadmap": return chartMarkup("roadmap", visuals.roadmap || {}, options);
      case "problemMatrix": return chartMarkup("problemMatrix", visuals.industryProblems || {}, { ...options, presentation: true });
      case "practiceFramework": return chartMarkup("practiceFramework", visuals.industryPractices || {}, { ...options, presentation: true });
      case "scenarioMatrix": return chartMarkup("scenarioMatrix", visuals.industryPractices || {}, { ...options, presentation: true });
      case "maturitySequence": return chartMarkup("maturitySequence", visuals.industryPractices || {}, { ...options, presentation: true });
      case "studyRoadmap": {
        const roadmap = visuals.kongMulticloud || {};
        const ids = Array.isArray(slide.workstreamIds) ? new Set(slide.workstreamIds) : null;
        const slicedRoadmap = {
          ...roadmap,
          workstreams: Array.isArray(roadmap.workstreams)
            ? roadmap.workstreams.filter((workstream) => !ids || ids.has(workstream.id))
            : [],
        };
        return chartMarkup("studyRoadmap", slicedRoadmap, { ...options, presentation: true });
      }
      case "guidedEvaluation": {
        const guidedOptions = {
          ...options,
          viewId: slide.viewId,
          phaseId: slide.phaseId,
          evidenceState: slide.evidenceState,
          sourceClass: slide.sourceClass,
          rowIds: slide.rowIds,
          optionIds: slide.optionIds,
        };
        const inlineFigure = (figure, kind = "KPS") => {
          const mermaid = figure?.mermaid || "";
          const figureId = figure?.figureId || slide.figureId || `${kind} figure`;
          return mermaid
            ? `<div class="slide-diagram is-guided-canonical" data-slide-inline-mermaid="${escapeHtml(mermaid)}" data-diagram-id="${escapeHtml(figureId)}" data-diagram-summary="${escapeHtml(figure?.title || slide.body || "")}"><p>Rendering canonical ${escapeHtml(figureId)}…</p></div>`
            : `<p class="visual-empty">The canonical ${escapeHtml(figureId)} model is unavailable.</p>`;
        };
        if (slide.viewId === "architecture") {
          const figure = visuals.kongPlatformStrategy?.architecture;
          const overview = visuals.kongPlatformStrategy?.guidedArchitectureOverview;
          const mermaid = figure?.mermaid || "";
          const overviewMarkup = chartMarkup("guidedArchitectureOverview", overview, { presentation: true, compact: true });
          return mermaid
            ? `<div class="slide-diagram is-guided-canonical" data-slide-inline-mermaid="${escapeHtml(mermaid)}" data-diagram-id="KPS-1" data-diagram-summary="${escapeHtml(figure?.title || slide.body || "")}"><template data-diagram-overview>${overviewMarkup}</template><p>Rendering the KGE-09 overview and canonical KPS-1 inspection model…</p></div>`
            : overviewMarkup;
        }
        if (["state-trust", "degraded", "operating-model", "assurance"].includes(slide.viewId)) {
          const figure = (visuals.kongPlatformStrategy?.figures || []).find((item) => item.figureId === slide.figureId);
          return inlineFigure(figure, "KPS");
        }
        if (slide.viewId === "coexistence") {
          const figure = (visuals.muleMigration?.figures || []).find((item) => item.figureId === slide.figureId);
          return inlineFigure(figure, "MULE");
        }
        if (slide.viewId === "adoption") {
          const roadmap = visuals.kongPlatformStrategy?.roadmap || {};
          return chartMarkup("kongPlatformRoadmap", { ...roadmap, phases: selected(roadmap.phases) }, guidedOptions);
        }
        if (slide.viewId === "migration-boundary") {
          const migration = visuals.muleMigration || {};
          return chartMarkup("muleMigrationBoundary", { ...migration, responsibilities: selected(migration.responsibilities) }, guidedOptions);
        }
        if (slide.viewId === "waves") {
          const migration = visuals.muleMigration || {};
          return chartMarkup("muleMigrationWaves", { ...migration, waves: selected(migration.waves) }, guidedOptions);
        }
        if (["outcomes-1", "outcomes-2"].includes(slide.viewId)) {
          const outcomes = visuals.kongPlatformStrategy?.outcomes || {};
          return chartMarkup("kongPlatformOutcomes", { ...outcomes, rows: selected(outcomes.rows) }, guidedOptions);
        }
        return chartMarkup("guidedEvaluation", {
          ...(visuals.guidedEvaluation || {}),
          platformOptions: visuals.kongMulticloud || {},
          platformFit: visuals.kongPlatformStrategy?.fit || {},
        }, guidedOptions);
      }
      case "kongPlatformFit": {
        const fit = visuals.kongPlatformStrategy?.fit || {};
        return chartMarkup("kongPlatformFit", { ...fit, rows: selected(fit.rows, "projectionId") }, options);
      }
      case "kongOptions": {
        const optionIds = Array.isArray(slide.optionIds) ? new Set(slide.optionIds) : null;
        const optionsData = visuals.kongMulticloud || {};
        return chartMarkup("kongOptions", {
          ...optionsData,
          options: Array.isArray(optionsData.options)
            ? optionsData.options.filter((option) => !optionIds || optionIds.has(option.id))
            : [],
        }, options);
      }
      case "kongJourneySpine": return chartMarkup("kongJourneySpine", { phases: slide.journeyPhases || [] }, options);
      case "kongSelectedOption": {
        const fit = visuals.kongPlatformStrategy?.fit || {};
        return chartMarkup("kongSelectedOption", { ...fit, rows: selected(fit.rows, "projectionId") }, options);
      }
      case "kongPlatformArchitecture": {
        const architecture = visuals.kongPlatformStrategy?.architecture || {};
        const mermaid = architecture.mermaid || "";
        return mermaid
          ? `<div class="slide-diagram is-kps-target" data-slide-inline-mermaid="${escapeHtml(mermaid)}" data-diagram-id="KPS-1" data-diagram-summary="${escapeHtml(architecture.title || "")}"><p>Rendering canonical KPS-1…</p></div>`
          : '<p class="visual-empty">The canonical KPS-1 model is unavailable.</p>';
      }
      case "kongTechnicalFigure": {
        const figure = (visuals.kongPlatformStrategy?.figures || []).find((item) => item.figureId === slide.figureId);
        const mermaid = figure?.mermaid || "";
        return mermaid
          ? `<div class="slide-diagram is-kps-target" data-slide-inline-mermaid="${escapeHtml(mermaid)}" data-diagram-id="${escapeHtml(slide.figureId)}" data-diagram-summary="${escapeHtml(figure?.title || "")}"><p>Rendering canonical ${escapeHtml(slide.figureId)}…</p></div>`
          : `<p class="visual-empty">The canonical ${escapeHtml(slide.figureId || "KPS figure")} model is unavailable.</p>`;
      }
      case "kongPlatformCases": {
        const cases = visuals.kongPlatformStrategy?.cases || {};
        return chartMarkup("kongPlatformCases", { ...cases, rows: selected(cases.rows) }, options);
      }
      case "kongPlatformRoadmap": return chartMarkup("kongPlatformRoadmap", visuals.kongPlatformStrategy?.roadmap || {}, options);
      case "kongPlatformOutcomes": {
        const outcomes = visuals.kongPlatformStrategy?.outcomes || {};
        return chartMarkup("kongPlatformOutcomes", { ...outcomes, rows: selected(outcomes.rows) }, options);
      }
      case "muleMigrationBoundary": return chartMarkup("muleMigrationBoundary", visuals.muleMigration || {}, options);
      case "muleMigrationWaves": return chartMarkup("muleMigrationWaves", visuals.muleMigration || {}, options);
      case "muleMigrationFigure": {
        const figure = (visuals.muleMigration?.figures || []).find((item) => item.figureId === slide.figureId);
        const mermaid = figure?.mermaid || "";
        return mermaid
          ? `<div class="slide-diagram is-migration-model" data-slide-inline-mermaid="${escapeHtml(mermaid)}" data-diagram-id="${escapeHtml(slide.figureId)}" data-diagram-summary="${escapeHtml(figure?.title || "")}"><p>Rendering canonical ${escapeHtml(slide.figureId)}…</p></div>`
          : `<p class="visual-empty">The canonical ${escapeHtml(slide.figureId || "migration figure")} model is unavailable.</p>`;
      }
      case "governance": return chartMarkup("governance", visuals.governance || {}, options);
      case "recommendation": return chartMarkup("recommendation", visuals.review || {}, options);
      default: return "";
    }
  }

  function presentationArchitectureMarkup(slide, source) {
    const node = (label, tone = "") => `<span class="slide-system-node ${tone}" role="presentation">${escapeHtml(label)}</span>`;
    const arrow = '<span class="slide-system-arrow" aria-hidden="true">→</span>';
    if (slide.key === "target-state") {
      return `<figure class="slide-system-map is-target" role="img" aria-label="Reviewed API operations configure a control plane, while consumer traffic passes through edge controls and workload-local gateway data planes to domain and integration capabilities with shared observability.">
        <div class="slide-system-lane"><b>Control</b><div class="slide-system-row is-control" aria-hidden="true">${node("Reviewed API operations")}${arrow}${node("API management control plane", "is-accent")}${arrow}${node("mTLS configuration")}</div></div>
        <div class="slide-system-lane"><b>Request</b><div class="slide-system-row" aria-hidden="true">${node("Consumers + edge")}${arrow}${node("External + private gateway data planes", "is-accent")}${arrow}${node("AKS domain + integration capabilities")}${arrow}${node("Observability + security")}</div></div>
      </figure>`;
    }
    if (slide.key === "system") {
      return `<figure class="slide-system-map is-transition" role="img" aria-label="Release control and health evidence govern per-route allocation between legacy Mule or PCF services and AKS targets behind a stable enterprise gateway.">
        <div class="slide-system-lane"><b>Control</b><div class="slide-system-row is-control" aria-hidden="true">${node("Release controls")}${arrow}${node("Health + reconciliation evidence", "is-accent")}${arrow}${node("Adjust weights or rollback")}</div></div>
        <div class="slide-system-lane"><b>Traffic</b><div class="slide-system-row" aria-hidden="true">${node("Consumers + edge")}${arrow}${node("Enterprise gateway")}${arrow}${node("Per-route allocation", "is-accent")}${arrow}${node("Mule / PCF coexistence or AKS target")}${arrow}${node("Integration capabilities")}</div></div>
      </figure>`;
    }
    if (slide.key === "lessons") {
      return `<figure class="slide-system-map is-lessons" role="img" aria-label="Public incident patterns connect policy, configuration, network, trust, and state changes to shared runtime failures, then to containment, reconciliation, and independent recovery controls.">
        <div class="slide-system-lane"><b>Triggers</b><div class="slide-system-row" aria-hidden="true">${node("Policy + code")}${node("Generated configuration")}${node("Network + state")}${node("Certificate trust")}</div></div>
        <div class="slide-system-lane"><b>Failures</b><div class="slide-system-row" aria-hidden="true">${node("Fleet resource exhaustion", "is-accent")}${node("Latent defect activated", "is-accent")}${node("Divergence + backlog", "is-accent")}${node("Client incompatibility", "is-accent")}</div></div>
        <div class="slide-system-lane"><b>Controls</b><div class="slide-system-row is-control" aria-hidden="true">${node("Bound + canary")}${node("Fail small")}${node("Reconcile state")}${node("Independent recovery access")}</div></div>
      </figure>`;
    }
    return source ? `<div class="slide-diagram" data-slide-diagram="${escapeHtml(source.contentUrl)}"><p>Rendering system model…</p></div>` : "";
  }

  async function renderPresentationDiagram() {
    const target = document.querySelector("[data-slide-diagram], [data-slide-inline-mermaid]");
    if (!target) return;
    try {
      const text = target.dataset.slideInlineMermaid || await fetchText(target.dataset.slideDiagram);
      await mermaidMarkup(text, target, document.querySelector(".slide-title")?.textContent || "Presentation architecture diagram");
    } catch (error) {
      target.innerHTML = `<p class="visual-empty">Open the supporting source to inspect this model.</p>`;
    }
  }

  function activatePresentationFrame() {
    const slideMain = document.querySelector(".presentation-stage .slide-main");
    if (!slideMain) return;
    const comparison = document.querySelector(".presentation-stage .viz-guided-comparison-wrap");
    const surfaces = [
      [slideMain, "Expanded slide detail. Scroll vertically to inspect the opened evidence.", "vertical"],
      [document.querySelector(".presentation-stage .slide-aside-content"), "Additional slide context. Scroll vertically to inspect the complete cue and source framing.", "vertical"],
      [comparison, `${comparison?.dataset.comparisonLabel || "Supplied product comparison"}. Scroll horizontally to compare every product.`, "horizontal"],
    ].filter(([surface]) => surface);
    const syncSurface = (surface, label, axis) => {
      const scrollable = axis === "horizontal"
        ? surface.scrollWidth > surface.clientWidth + 2
        : surface.scrollHeight > surface.clientHeight + 2;
      surface.tabIndex = scrollable ? 0 : -1;
      if (scrollable) {
        surface.setAttribute("role", "region");
        surface.setAttribute("aria-label", label);
      } else {
        surface.removeAttribute("role");
        surface.removeAttribute("aria-label");
        if (axis === "horizontal") surface.scrollLeft = 0;
        else surface.scrollTop = 0;
      }
      if (axis === "horizontal") {
        const cue = surface.parentElement?.querySelector(":scope > .viz-guided-scroll-cue");
        if (cue) cue.hidden = !scrollable;
      }
    };
    const sync = () => surfaces.forEach(([surface, label, axis]) => syncSurface(surface, label, axis));
    surfaces.forEach(([surface, , axis]) => {
      surface.addEventListener("toggle", () => requestAnimationFrame(sync), true);
      if (axis === "horizontal") {
        surface.addEventListener("keydown", (event) => {
          if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
          event.preventDefault();
          event.stopPropagation();
          if (event.key === "Home") surface.scrollLeft = 0;
          else if (event.key === "End") surface.scrollLeft = surface.scrollWidth;
          else surface.scrollLeft += (event.key === "ArrowRight" ? 1 : -1) * Math.max(48, surface.clientWidth * 0.18);
        });
      } else {
        surface.addEventListener("keydown", (event) => {
          if (!["ArrowUp", "ArrowDown", "PageUp", "PageDown", "Home", "End", " "].includes(event.key)) return;
          event.preventDefault();
          event.stopPropagation();
          if (event.key === "Home") {
            surface.scrollTop = 0;
            return;
          }
          if (event.key === "End") {
            surface.scrollTop = surface.scrollHeight;
            return;
          }
          const backwards = event.key === "ArrowUp" || event.key === "PageUp" || event.shiftKey && event.key === " ";
          const step = ["ArrowUp", "ArrowDown"].includes(event.key)
            ? Math.max(48, surface.clientHeight * 0.18)
            : Math.max(64, surface.clientHeight * 0.7);
          surface.scrollTop += backwards ? -step : step;
        });
      }
    });
    const observer = new ResizeObserver(sync);
    surfaces.forEach(([surface]) => observer.observe(surface));
    requestAnimationFrame(sync);
  }

  function presentationContext(contextId = "") {
    const allSlides = state.manifest.presentation || [];
    const audience = contextId
      ? window.ApiStudyAudiences?.getById?.(state.manifest.audiences || [], contextId)
      : null;
    const deck = contextId
      ? (state.manifest.presentationDecks || []).find((item) => item.id === contextId) || null
      : null;
    const context = audience || deck;
    if (contextId && !context) return { audience: null, deck: null, context: null, slides: [] };
    const slides = window.ApiStudyAudiences?.presentationSlides
      ? window.ApiStudyAudiences.presentationSlides(context, allSlides)
      : allSlides;
    return { audience, deck, context, slides };
  }

  function presentationExitHref(audience, deck) {
    if (audience) return `#/audiences/${encodeURIComponent(audience.id)}`;
    if (deck?.exitRoute) return deck.exitRoute;
    return "#/overview";
  }

  function presentationSlideHref(context, index) {
    return context
      ? `#/present/${encodeURIComponent(context.id)}/${index}`
      : `#/present/${index}`;
  }

  function renderPresentation(rawIndex, contextId = "") {
    const { audience, deck, context, slides } = presentationContext(contextId);
    if (!slides.length) {
      document.body.classList.remove("is-presenting");
      return renderNotFound("No presentation story is configured.");
    }
    const index = Number.parseInt(rawIndex, 10);
    if (!Number.isInteger(index) || index < 0 || index >= slides.length) {
      document.body.classList.remove("is-presenting");
      return renderNotFound("That presentation slide is outside the configured story.");
    }
    const slide = slides[index];
    const source = state.manifest.items.find((item) => item.id === slide.sourceId);
    const sourceLocatorFor = (sourceItem) => {
      if (!sourceItem) return "";
      const numberedStudy = sourceItem.path.match(/^docs\/(\d+)-/);
      return numberedStudy ? `docs/${numberedStudy[1]}` : sourceItem.path;
    };
    const sourceLocator = sourceLocatorFor(source);
    const isGuidedDeck = deck?.theme === "kong-guided";
    const isLegacyJourneyDeck = deck?.theme === "kong-journey";
    const isJourneyDeck = isLegacyJourneyDeck || isGuidedDeck;
    const visualSlide = isJourneyDeck && slide.visual === "kongJourneySpine"
      ? { ...slide, journeyPhases: deck.journeyPhases || [] }
      : slide;
    const stageClass = slide.key === "industry-practices"
      ? " is-industry-practices"
      : isGuidedDeck
        ? " is-kong-platform is-kong-journey is-kong-guided"
      : isJourneyDeck
        ? " is-kong-platform is-kong-journey"
      : deck?.theme === "kong-platform" || slide.key.startsWith("kong-platform-") || slide.key.startsWith("kong-technical-")
        ? " is-kong-platform"
        : "";
    const guidedDiagramViews = new Set(["architecture", "state-trust", "degraded", "operating-model", "coexistence", "assurance"]);
    const guidedRoadmapViews = new Set(["adoption", "migration-boundary", "waves", "outcomes-1", "outcomes-2"]);
    const narrativeClass = visualSlide.visual === "guidedEvaluation" && guidedDiagramViews.has(visualSlide.viewId)
      ? " is-diagram"
      : visualSlide.visual === "guidedEvaluation" && guidedRoadmapViews.has(visualSlide.viewId)
        ? " is-roadmap"
      : ["architectureDiagram", "kongPlatformArchitecture", "kongTechnicalFigure", "muleMigrationFigure"].includes(visualSlide.visual)
      ? " is-diagram"
      : ["roadmap", "kongPlatformRoadmap"].includes(visualSlide.visual)
        ? " is-roadmap"
        : visualSlide.visual === "studyRoadmap"
          ? " is-roadmap"
        : visualSlide.visual === "sourceBalance"
          ? " is-matrix is-source-balance"
        : ["statusMatrix", "recommendation", "governance", "problemMatrix", "practiceFramework", "scenarioMatrix", "maturitySequence", "kongPlatformFit", "kongSelectedOption", "kongOptions", "kongJourneySpine", "kongPlatformCases", "kongPlatformOutcomes", "muleMigrationBoundary", "muleMigrationWaves", "guidedEvaluation"].includes(visualSlide.visual)
          ? " is-matrix"
          : "";
    document.body.classList.add("is-presenting");
    const contextLabel = context?.shortLabel || "";
    setPageTitle(`${index + 1}. ${slide.title}${contextLabel ? ` — ${contextLabel}` : ""}`);
    setActiveNav("");
    const configuredPhases = Array.isArray(deck?.journeyPhases) ? deck.journeyPhases : [];
    const journeyPhases = configuredPhases.length
      ? configuredPhases
      : ["Options", "Architecture", "Adoption", "Migration", "Production"].map((label, phaseIndex) => ({ id: String(phaseIndex + 1).padStart(2, "0"), label }));
    const journeyPhaseStarts = journeyPhases.map((phase) => slides.findIndex((candidate) => candidate.key === phase.startKey));
    const explicitPhaseIndex = journeyPhases.findIndex((phase) => phase.id === slide.phaseId);
    const startKeyPhaseIndex = journeyPhases.reduce((matchedIndex, phase, phaseIndex) => {
      const startIndex = journeyPhaseStarts[phaseIndex];
      return startIndex >= 0 && startIndex <= index ? phaseIndex : matchedIndex;
    }, -1);
    const journeyPhaseIndex = explicitPhaseIndex >= 0
      ? explicitPhaseIndex
      : startKeyPhaseIndex >= 0
        ? startKeyPhaseIndex
        : 0;
    const journeySpine = isJourneyDeck
      ? `<nav class="journey-phase-nav" aria-label="${isGuidedDeck ? "Guided Kong evaluation phases" : "Kong platform journey phases"}"><ol class="journey-phase-spine" style="--journey-phase-count:${journeyPhases.length}">${journeyPhases.map((phase, phaseIndex) => {
          const phaseLabel = phase.phase || phase.label;
          const phaseStartIndex = journeyPhaseStarts[phaseIndex];
          const isCurrentPhase = phaseIndex === journeyPhaseIndex;
          const phaseId = phase.id || String(phaseIndex + 1).padStart(2, "0");
          const phaseIdMarkup = phaseId.startsWith("KGE-")
            ? `<span class="journey-phase-id-prefix">${escapeHtml(phaseId.slice(0, 4))}</span>${escapeHtml(phaseId.slice(4))}`
            : escapeHtml(phaseId);
          const phasePosition = `Phase ${phaseIndex + 1} of ${journeyPhases.length}: ${phaseLabel}`;
          const phaseAction = isCurrentPhase ? `Restart at slide ${phaseStartIndex + 1}` : `Go to slide ${phaseStartIndex + 1}`;
          return `<li class="${phaseIndex < journeyPhaseIndex ? "is-prior" : isCurrentPhase ? "is-current" : ""}"><a href="${presentationSlideHref(context, phaseStartIndex)}" aria-label="${escapeHtml(`${isCurrentPhase ? "Current " : ""}${phasePosition}. ${phaseAction}.`)}" title="${escapeHtml(`${phaseLabel} · slide ${phaseStartIndex + 1}`)}" ${isCurrentPhase ? 'aria-current="step"' : ""}><span aria-hidden="true">${phaseIdMarkup}</span><b>${escapeHtml(phaseLabel)}</b></a></li>`;
        }).join("")}</ol></nav>`
      : "";
    const guidedRepoReferences = isGuidedDeck
      ? [...new Set([slide.sourceId, ...(Array.isArray(slide.sourceIds) ? slide.sourceIds : [])].filter(Boolean))]
          .map((sourceId) => state.manifest.items.find((item) => item.id === sourceId))
          .filter(Boolean)
      : [];
    const guidedOfficialReferences = isGuidedDeck && Array.isArray(slide.officialReferences)
      ? slide.officialReferences.filter((reference) => reference?.label && /^https:\/\//.test(reference?.url || ""))
      : [];
    const guidedReferenceMarkup = isGuidedDeck
      ? `<div class="slide-reference-actions">
          ${source ? `<a class="slide-source" href="${itemHref(source)}" aria-label="Open repository source: ${escapeHtml(source.title)}">Source · ${escapeHtml(sourceLocator)} <span aria-hidden="true">↗</span></a>` : ""}
          <details class="slide-references">
            <summary aria-label="Open ${guidedRepoReferences.length + guidedOfficialReferences.length} references for this slide">References · ${guidedRepoReferences.length + guidedOfficialReferences.length}</summary>
            <div class="slide-reference-menu">
              <span>Repository studies</span>
              ${guidedRepoReferences.map((reference) => `<a href="${itemHref(reference)}">${escapeHtml(sourceLocatorFor(reference))} · ${escapeHtml(reference.title)}</a>`).join("")}
              <span>Official documentation</span>
              ${guidedOfficialReferences.map((reference) => `<a href="${escapeHtml(reference.url)}" target="_blank" rel="noreferrer">${escapeHtml(reference.label)} <span aria-hidden="true">↗</span></a>`).join("")}
            </div>
          </details>
        </div>`
      : source
        ? `<a class="slide-source" href="${itemHref(source)}" aria-label="Open canonical source: ${escapeHtml(source.title)}">Source · ${escapeHtml(sourceLocator)} <span aria-hidden="true">↗</span></a>`
        : "";
    const journeyProof = isJourneyDeck
      ? `<aside class="slide-aside journey-proof-strip">
          <div class="slide-aside-content">
            <div class="slide-metric"><strong>${escapeHtml(slide.metric)}</strong><span>${escapeHtml(slide.metricLabel)}</span></div>
            <div class="journey-proof-copy"><span>${isGuidedDeck ? "Decision cue" : "Why it matters"}</span><p class="slide-body">${escapeHtml(slide.body)}</p></div>
          </div>
          ${guidedReferenceMarkup}
        </aside>`
      : `<aside class="slide-aside">
          <div class="slide-aside-content">
            <div class="slide-metric"><strong>${escapeHtml(slide.metric)}</strong><span>${escapeHtml(slide.metricLabel)}</span></div>
            ${audience ? `<div class="slide-audience-cue"><span>Close this room with</span><p>${escapeHtml(audience.action)}</p></div>` : ""}
            <p class="slide-body">${escapeHtml(slide.body)}</p>
          </div>
          ${source ? `<a class="slide-source" href="${itemHref(source)}">Open supporting source <span aria-hidden="true">↗</span></a>` : ""}
        </aside>`;
    const guidedEvidence = isGuidedDeck
      ? `<div class="guided-evidence-ribbon" aria-label="Evidence and source classification">
          <span><b>Evidence</b>${escapeHtml(slide.evidenceState || "Not classified")}</span>
          <span><b>Source class</b>${escapeHtml(slide.sourceClass || "Not classified")}</span>
          ${slide.asOf ? `<span><b>As of</b>${escapeHtml(slide.asOf)}</span>` : ""}
          ${slide.evidenceInterpretation ? `<p>${escapeHtml(slide.evidenceInterpretation)}</p>` : ""}
        </div>`
      : "";
    main.innerHTML = `
      <section class="presentation-stage${stageClass}" aria-label="Presentation slide ${index + 1} of ${slides.length}">
        <article class="presentation-slide${isJourneyDeck ? " is-journey-slide" : ""}${isGuidedDeck ? " is-guided-slide" : ""}">
          ${journeySpine}
          <div class="slide-main">
            <span class="eyebrow">${escapeHtml(slide.eyebrow)}${audience ? ` / ${escapeHtml(audience.shortLabel)} lens` : deck ? ` / ${escapeHtml(deck.shortLabel)} deck` : ""}</span>
            ${guidedEvidence}
            <div class="slide-narrative${narrativeClass}">
              <h1 class="slide-title">${escapeHtml(slide.title)}</h1>
              <div class="slide-visual">${presentationVisualMarkup(visualSlide, source, isJourneyDeck)}</div>
            </div>
            <span class="slide-counter">${audience ? `${escapeHtml(audience.shortLabel)} briefing · ` : deck ? `${escapeHtml(deck.shortLabel)} deck · ` : ""}${String(index + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}</span>
          </div>
          ${journeyProof}
        </article>
        <div class="slide-controls" aria-label="Presentation controls">
          <button type="button" data-slide-prev aria-label="Previous slide" ${index === 0 ? "disabled" : ""}>←</button>
          <button type="button" data-slide-next aria-label="Next slide" ${index === slides.length - 1 ? "disabled" : ""}>→</button>
          <button type="button" data-fullscreen aria-label="Toggle fullscreen">⛶</button>
          <a href="${presentationExitHref(audience, deck)}" aria-label="Exit presentation">×</a>
        </div>
        <span class="slide-progress" style="width:${((index + 1) / slides.length) * 100}%"></span>
      </section>`;

    document.querySelector("[data-slide-prev]").addEventListener("click", () => moveSlide(-1));
    document.querySelector("[data-slide-next]").addEventListener("click", () => moveSlide(1));
    document.querySelector("[data-fullscreen]").addEventListener("click", toggleFullscreen);
    renderPresentationDiagram();
    activatePresentationFrame();
  }

  function moveSlide(delta) {
    const route = parseRoute();
    if (route.name !== "present") return;
    const hasContext = route.parts.length > 1;
    const contextId = hasContext ? route.parts[0] : "";
    const current = Number.parseInt(route.parts[hasContext ? 1 : 0] || "0", 10) || 0;
    const { context, slides } = presentationContext(contextId);
    if (!slides.length) return;
    const next = Math.min(Math.max(current + delta, 0), slides.length - 1);
    if (next !== current) location.hash = presentationSlideHref(context, next);
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
    document.querySelector(".diagram-frame.is-expanded [data-diagram-action='expand']")?.click();
    document.body.classList.remove("has-expanded-diagram");
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
      case "doc": renderDocument(current.parts[0], current.params.get("anchor") || ""); break;
      case "present": {
        const genericRoute = current.parts.length === 1 && /^\d+$/.test(current.parts[0]);
        const contextualRoute = current.parts.length === 2 && /^\d+$/.test(current.parts[1]);
        if (contextualRoute) renderPresentation(current.parts[1], current.parts[0]);
        else if (genericRoute) renderPresentation(current.parts[0]);
        else {
          document.body.classList.remove("is-presenting");
          renderNotFound("No presentation story is configured.");
        }
        break;
      }
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
    document.querySelector(".diagram-frame.is-expanded")?.dispatchEvent(new CustomEvent("diagram-close-request", {
      detail: { restoreFocus: false },
    }));
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

  function preparePrintArtifacts() {
    if (state.printSnapshot) return;
    const expandedDiagram = document.querySelector(".diagram-frame.is-expanded");
    expandedDiagram?.dispatchEvent(new CustomEvent("diagram-close-request", {
      detail: { restoreFocus: false, deferLayout: false },
    }));
    const closedDetails = [...document.querySelectorAll(".atlas-panel:not([open]), .visual-disclosure:not([open]), .document-evidence-panel:not([open]), .viz-presentation-detail:not([open]), .viz-kps-fit-contract:not([open]), .data-record-details:not([open])")]
      .filter((detail) => !detail.closest(".presentation-stage.is-kong-journey"));
    const namedDetails = [...document.querySelectorAll(".viz-kps-fit-contract[name]")]
      .map((detail) => ({ detail, name: detail.getAttribute("name") }));
    const hiddenEvidence = [...document.querySelectorAll(".document-section-body[hidden], .diagram-scroll[hidden]")]
      .filter((element) => !element.closest(".presentation-stage.is-kong-journey"));
    const journeyVisibility = [...document.querySelectorAll(".presentation-stage.is-kong-journey .diagram-summary, .presentation-stage.is-kong-journey .diagram-scroll")]
      .map((element) => ({ element, hidden: element.hidden }));
    state.printSnapshot = { closedDetails, hiddenEvidence, namedDetails, journeyVisibility, expandedDiagram };
    namedDetails.forEach(({ detail }) => detail.removeAttribute("name"));
    closedDetails.forEach((detail) => { detail.open = true; });
    hiddenEvidence.forEach((element) => { element.hidden = false; });
    journeyVisibility.forEach(({ element }) => {
      element.hidden = element.classList.contains("diagram-scroll");
    });
  }

  function restorePrintArtifacts() {
    if (!state.printSnapshot) return;
    const { expandedDiagram } = state.printSnapshot;
    state.printSnapshot.closedDetails.forEach((detail) => {
      if (document.contains(detail)) detail.open = false;
    });
    state.printSnapshot.hiddenEvidence.forEach((element) => {
      if (document.contains(element)) element.hidden = true;
    });
    state.printSnapshot.namedDetails.forEach(({ detail, name }) => {
      if (document.contains(detail) && name) detail.setAttribute("name", name);
    });
    state.printSnapshot.journeyVisibility.forEach(({ element, hidden }) => {
      if (document.contains(element)) element.hidden = hidden;
    });
    state.printSnapshot = null;
    if (expandedDiagram && document.contains(expandedDiagram) && !expandedDiagram.classList.contains("is-expanded")) {
      expandedDiagram.querySelector("[data-diagram-action='expand']")?.click();
    }
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
  window.addEventListener("beforeprint", preparePrintArtifacts);
  window.addEventListener("afterprint", restorePrintArtifacts);
  document.addEventListener("keydown", (event) => {
    if (event.defaultPrevented) return;
    if (trapSearchFocus(event)) return;
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openSearch();
      return;
    }
    if (event.key === "Escape") {
      const openReferences = document.querySelector(".slide-references[open]");
      const expandedDiagram = document.querySelector(".diagram-frame.is-expanded");
      if (openReferences) {
        event.preventDefault();
        openReferences.open = false;
        openReferences.querySelector("summary")?.focus();
      } else if (expandedDiagram) {
        event.preventDefault();
        expandedDiagram.dispatchEvent(new CustomEvent("diagram-close-request", {
          detail: { restoreFocus: true },
        }));
      } else if (!searchDialog.hidden) closeSearch();
      else if (document.body.classList.contains("is-presenting")) {
        const current = parseRoute();
        const { audience, deck } = presentationContext(current.parts.length > 1 ? current.parts[0] : "");
        location.hash = presentationExitHref(audience, deck);
      }
      return;
    }
    if (document.body.classList.contains("is-presenting")) {
      const interactive = event.target instanceof Element && event.target.closest("a, button, input, select, textarea, summary, [contenteditable='true']");
      if (interactive) return;
      const scrollSurface = event.target instanceof Element && event.target.closest(".slide-main[tabindex='0'], .slide-aside-content[tabindex='0'], .diagram-scroll[tabindex='0'], .table-wrap[tabindex='0'], .viz-guided-comparison-wrap[tabindex='0']");
      const verticalScrollKey = ["ArrowDown", "ArrowUp", "PageDown", "PageUp", " "].includes(event.key);
      const horizontalScrollKey = ["ArrowRight", "ArrowLeft"].includes(event.key);
      if (scrollSurface && verticalScrollKey && scrollSurface.scrollHeight > scrollSurface.clientHeight + 2) return;
      if (scrollSurface && horizontalScrollKey && scrollSurface.scrollWidth > scrollSurface.clientWidth + 2) return;
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
