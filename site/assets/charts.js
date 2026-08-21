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

  function number(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function label(value, fallback = "Unlabelled") {
    const text = String(value ?? "").trim();
    return text || fallback;
  }

  function series(data) {
    if (Array.isArray(data)) {
      return data.map((item, index) => {
        if (typeof item === "number") return { label: `Item ${index + 1}`, value: item };
        if (typeof item === "string") return { label: item, value: 1 };
        return {
          ...item,
          label: label(item?.label ?? item?.name ?? item?.id, `Item ${index + 1}`),
          value: number(item?.value ?? item?.count ?? item?.total),
        };
      });
    }
    if (data && typeof data === "object") {
      return Object.entries(data).map(([key, value]) => ({ label: key, value: number(value) }));
    }
    return [];
  }

  function total(items) {
    return items.reduce((sum, item) => sum + number(item.value), 0);
  }

  function slug(value = "") {
    return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "unknown";
  }

  function heading(options = {}) {
    if (!options.title && !options.note) return "";
    return `<figcaption class="viz-heading">
      ${options.title ? `<strong>${escapeHtml(options.title)}</strong>` : ""}
      ${options.note ? `<span>${escapeHtml(options.note)}</span>` : ""}
    </figcaption>`;
  }

  function empty(message = "No visualization data is available yet.") {
    return `<div class="viz-empty">${escapeHtml(message)}</div>`;
  }

  function sourceLink(meta, labelText = "Open canonical source") {
    if (!meta?.sourceId && !meta?.sourceHref) return "";
    const paths = Array.isArray(meta.sourcePaths) && meta.sourcePaths.length ? meta.sourcePaths : [meta.sourcePath].filter(Boolean);
    const detail = paths.length > 1 ? `${paths.length} sources · ${paths[0]}` : paths[0] || "";
    const href = meta.sourceId ? `#/doc/${encodeURIComponent(meta.sourceId)}` : meta.sourceHref;
    return `<a class="visual-source" href="${escapeHtml(href)}" title="${escapeHtml(paths.join(" · "))}">${escapeHtml(labelText)}<span>${escapeHtml(detail)}</span></a>`;
  }

  function seriesValue(data, wanted) {
    const match = series(data).find((item) => item.label.toLowerCase() === String(wanted).toLowerCase());
    return match ? number(match.value) : 0;
  }

  function legend(data, options = {}) {
    const items = series(data);
    if (!items.length) return "";
    return `<div class="viz-legend" aria-label="Legend">
      ${items.map((item, index) => `<span class="viz-legend-item"><i class="viz-swatch" style="--viz-swatch:var(--viz-color-${index % 6})"></i><span>${escapeHtml(item.label)}</span>${options.values === false ? "" : `<strong>${escapeHtml(item.value)}</strong>`}</span>`).join("")}
    </div>`;
  }

  function bars(data, options = {}) {
    const items = series(data);
    if (!items.length) return empty();
    const maximum = Math.max(...items.map((item) => item.value), 1);
    const rows = items.map((item, index) => {
      const percentage = Math.max(0, Math.min(100, (item.value / maximum) * 100));
      return `<div class="viz-bar-row">
        <span class="viz-bar-label">${escapeHtml(item.label)}</span>
        <span class="viz-bar-track" aria-hidden="true"><i class="viz-bar-fill" style="width:${percentage}%;--viz-fill:var(--viz-color-${index % 6})"></i></span>
        <strong class="viz-bar-value">${escapeHtml(item.value)}</strong>
      </div>`;
    }).join("");
    return `<figure class="viz viz-bars ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Bar chart")}">${heading(options)}<div class="viz-bar-list">${rows}</div></figure>`;
  }

  function stackedBars(data, options = {}) {
    const rows = Array.isArray(data) ? data : [];
    if (!rows.length) return empty();
    const keys = Array.isArray(options.keys) && options.keys.length ? options.keys : ["mandatory", "weighted"];
    const maxTotal = Math.max(...rows.map((row) => keys.reduce((sum, key) => sum + number(row[key]), 0)), 1);
    const content = rows.map((row) => {
      const rowTotal = keys.reduce((sum, key) => sum + number(row[key]), 0);
      const detail = keys.map((key) => `${key}: ${number(row[key])}`).join(", ");
      return `<div class="viz-stacked-row">
        <span class="viz-bar-label">${escapeHtml(row.label || row.id)}</span>
        <span class="viz-stacked-track" role="img" aria-label="${escapeHtml(row.label || row.id)} — ${escapeHtml(detail)}; total: ${rowTotal}">
          ${keys.map((key, index) => {
            const value = number(row[key]);
            const width = (value / maxTotal) * 100;
            return `<i class="viz-segment is-${escapeHtml(slug(key))}" style="width:${width}%;--viz-fill:var(--viz-color-${index % 6})" title="${escapeHtml(key)}: ${value}"></i>`;
          }).join("")}
        </span>
        <strong class="viz-bar-value">${rowTotal}</strong>
      </div>`;
    }).join("");
    return `<figure class="viz viz-stacked ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Stacked bar chart")}">${heading(options)}<div class="viz-bar-list">${content}</div>${legend(keys.map((key, index) => ({ label: key, value: rows.reduce((sum, row) => sum + number(row[key]), 0), colorIndex: index })))}</figure>`;
  }

  function donut(data, options = {}) {
    const items = series(data);
    if (!items.length) return empty();
    const sum = number(options.total) || total(items);
    let cursor = 0;
    const segments = items.map((item, index) => {
      const start = cursor;
      cursor += sum ? (item.value / sum) * 100 : 0;
      return `var(--viz-color-${index % 6}) ${start}% ${cursor}%`;
    });
    if (cursor < 100) segments.push(`var(--viz-empty) ${cursor}% 100%`);
    return `<figure class="viz viz-donut ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Donut chart")}">${heading(options)}
      <div class="viz-donut-layout">
        <div class="viz-donut-ring" style="background:conic-gradient(${segments.join(",")})" aria-hidden="true"><span class="viz-donut-core"><strong>${escapeHtml(sum)}</strong><small>${escapeHtml(options.centerLabel || "total")}</small></span></div>
        ${legend(items)}
      </div>
    </figure>`;
  }

  function evidenceLadder(data, options = {}) {
    const levels = Array.isArray(data) ? data : data?.evidenceLevels || [];
    if (!levels.length) return empty();
    return `<figure class="viz viz-ladder ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Evidence ladder")}">${heading(options)}
      <ol class="viz-ladder-list">${levels.map((item, index) => `<li class="viz-ladder-step">
        <strong class="viz-level">${escapeHtml(item.level || `E${index}`)}</strong>
        <span><b>${escapeHtml(item.label || item.evidence)}</b><small>${escapeHtml(item.confidence || "")}</small></span>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function statusMatrix(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    const nameHeader = options.nameHeader || "Item";
    const statusHeader = options.statusHeader || "Status";
    const noteHeader = options.noteHeader || "Evidence / condition";
    return `<figure class="viz viz-matrix ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Status table")}">${heading(options)}
      <div class="viz-matrix-table" role="table">
        <div class="viz-matrix-header" role="row">
          <span role="columnheader">#</span>
          <strong role="columnheader">${escapeHtml(nameHeader)}</strong>
          <span role="columnheader">${escapeHtml(statusHeader)}</span>
          ${options.compact ? "" : `<small role="columnheader">${escapeHtml(noteHeader)}</small>`}
        </div>
        ${rows.map((item, index) => `<div class="viz-matrix-row" role="row">
          <span class="viz-matrix-index" role="cell">${String(index + 1).padStart(2, "0")}</span>
          <strong role="cell">${escapeHtml(item.name || item.label)}</strong>
          <span class="viz-status is-${escapeHtml(slug(item.status))}" role="cell">${escapeHtml(item.status || "Unknown")}</span>
          ${options.compact ? "" : `<small role="cell">${escapeHtml(item.evidenceStatus || item.note || "")}</small>`}
        </div>`).join("")}
      </div>
    </figure>`;
  }

  function methodologyFlow(data, options = {}) {
    const steps = Array.isArray(data) ? data : data?.steps || [];
    if (!steps.length) return empty();
    return `<figure class="viz viz-flow ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Methodology flow")}">${heading(options)}
      <ol class="viz-flow-list">${steps.map((step, index) => `<li><span>${String(index + 1).padStart(2, "0")}</span><strong>${escapeHtml(step.label)}</strong>${options.compact ? "" : `<p>${escapeHtml(step.description || "")}</p>`}</li>`).join("")}</ol>
    </figure>`;
  }

  function roadmap(data, options = {}) {
    const phases = Array.isArray(data) ? data : data?.phases || [];
    if (!phases.length) return empty();
    return `<figure class="viz viz-roadmap ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Roadmap")}">${heading(options)}
      <ol class="viz-roadmap-list" style="--phase-count:${phases.length}">${phases.map((phase, index) => `<li>
        <span class="viz-roadmap-marker">${String(index).padStart(2, "0")}</span>
        <div><strong>${escapeHtml(phase.label)}</strong><b>${escapeHtml(phase.duration)}</b>${options.compact ? "" : `<p>${escapeHtml(phase.exitCriteria || "")}</p>`}</div>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function problemMatrix(data, options = {}) {
    const problems = Array.isArray(data) ? data : data?.problems || [];
    if (!problems.length) return empty();
    const mechanismLabel = options.mechanismLabel || "Mechanism vendors productize";
    const proofLabel = options.proofLabel || "Decision implication";
    return `<figure class="viz viz-problem-matrix ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Enduring API-management problems")}">${heading(options)}
      <div class="viz-problem-key" aria-hidden="true"><span></span><span>Problem</span><span>${escapeHtml(mechanismLabel)}</span>${options.compact ? "" : `<span>${escapeHtml(proofLabel)}</span>`}</div>
      <ol class="viz-problem-list">${problems.map((problem, index) => {
        const rawId = label(problem.id, String(index + 1));
        const displayId = /^\d+$/.test(rawId) ? rawId.padStart(2, "0") : rawId;
        return `<li>
          <span class="viz-problem-index">${escapeHtml(displayId)}</span>
          <div class="viz-problem-copy"><strong>${escapeHtml(problem.label || problem.name)}</strong><p>${escapeHtml(problem.mechanism || "")}</p><small data-label="${escapeHtml(proofLabel)}">${escapeHtml(problem.proof || problem.implication || "")}</small></div>
        </li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function practiceFramework(data, options = {}) {
    const practices = Array.isArray(data) ? data : data?.practices || [];
    if (!practices.length) return empty();
    const displayPractice = (practice) => label(practice.label).replace(/^BP-\d+\s*(?:[—–:\-]\s*)?/i, "");
    return `<figure class="viz viz-practice-framework ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "API-management best-practice framework")}">${heading(options)}
      <div class="viz-practice-key" aria-hidden="true"><span>Practice</span><span>Required practice</span><span>Minimum mechanism</span>${options.compact ? "" : "<span>Acceptance evidence</span><span>Reject or hold</span>"}</div>
      <ol class="viz-practice-list">${practices.map((practice, index) => `<li>
        <span class="viz-practice-index"><b>${escapeHtml(practice.id || `BP-${index + 1}`)}</b><small>${escapeHtml(practice.problemId || "")}</small></span>
        <div class="viz-practice-copy"><strong>${escapeHtml(displayPractice(practice))}</strong><p>${escapeHtml(practice.mechanism || "")}</p>${options.compact ? "" : `<small>${escapeHtml(practice.evidence || "")}</small><em>${escapeHtml(practice.hold || "")}</em>`}</div>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function scenarioMatrix(data, options = {}) {
    const scenarios = Array.isArray(data) ? data : data?.scenarios || [];
    if (!scenarios.length) return empty();
    const presentation = Boolean(options.presentation);
    const displayControl = (scenario) => {
      const control = label(scenario.control);
      return presentation
        ? control.replace(/^(?:BP-\d+\s*,\s*)*BP-\d+\s*[—–-]\s*/i, "")
        : control;
    };
    return `<figure class="viz viz-scenario-matrix ${options.compact ? "is-compact" : ""} ${presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Realistic API-management scenarios")}">${heading(options)}
      <div class="viz-scenario-key" aria-hidden="true"><span></span><span>Scenario</span><span>Failure mechanism</span><span>Best-practice control</span>${options.compact ? "" : "<span>Measurable acceptance</span><span>Owner</span>"}</div>
      <ol class="viz-scenario-list">${scenarios.map((scenario, index) => `<li>
        <span class="viz-scenario-index">${escapeHtml(scenario.id || `S${index + 1}`)}</span>
        <div class="viz-scenario-copy"><strong>${escapeHtml(scenario.label)}</strong>${presentation ? '<span class="viz-scenario-control-label" aria-hidden="true">Control</span>' : `<p class="viz-scenario-failure">${escapeHtml(scenario.failure || "")}</p>`}<p class="viz-scenario-control">${escapeHtml(displayControl(scenario))}</p>${options.compact || presentation ? "" : `<small>${escapeHtml(scenario.acceptance || "")}</small><em>${escapeHtml(scenario.owner || "")}</em>`}</div>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function maturitySequence(data, options = {}) {
    const stages = Array.isArray(data) ? data : data?.stages || [];
    if (!stages.length) return empty();
    return `<figure class="viz viz-maturity-sequence ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Capability maturity and adoption sequence")}">${heading(options)}
      <ol class="viz-maturity-list">${stages.map((stage, index) => `<li>
        <span class="viz-maturity-index">${escapeHtml(stage.id || String(index + 1).padStart(2, "0"))}</span>
        <div><strong>${escapeHtml(stage.label || stage.outcome)}</strong><p>${escapeHtml(stage.outcome || "")}</p>${options.compact ? "" : `<small>${escapeHtml(stage.evidence || "")}</small>`}<em>${escapeHtml(stage.exitGate || "")}</em></div>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function studyRoadmap(data, options = {}) {
    const workstreams = Array.isArray(data) ? data : data?.workstreams || [];
    if (!workstreams.length) return empty();
    const problemHref = data?.problemSourceId ? `#/doc/${encodeURIComponent(data.problemSourceId)}` : "";
    return `<figure class="viz viz-study-roadmap ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Gated study roadmap")}">${heading(options)}
      <ol class="viz-study-roadmap-list" style="--study-columns:${workstreams.length <= 6 ? 3 : 4}">${workstreams.map((workstream, index) => {
        const id = label(workstream.id, `WS-${String(index + 1).padStart(2, "0")}`);
        const fullLabel = label(workstream.label);
        const workstreamLabel = fullLabel.toLowerCase().startsWith(id.toLowerCase()) ? fullLabel.slice(id.length).trim() : fullLabel;
        const problemIds = Array.isArray(workstream.problemIds) ? workstream.problemIds : [];
        const problemLabel = label(workstream.problemLabel, problemIds.join(", ")).replace(/\s+,/g, ",");
        return `<li>
          <div class="viz-study-roadmap-meta"><span>${escapeHtml(id)}</span><b title="${escapeHtml(workstream.duration || "Scenario pending")}">${escapeHtml(workstream.duration || "Scenario pending")}</b></div>
          <strong title="${escapeHtml(workstreamLabel)}">${escapeHtml(workstreamLabel)}</strong>
          ${options.compact ? "" : `<p>${escapeHtml(workstream.question || "")}</p>`}
          <div class="viz-study-roadmap-gates"><span title="${escapeHtml(`${workstream.entryGate || "Entry pending"} to ${workstream.exitGate || "Exit pending"}`)}">${escapeHtml(workstream.entryGate || "Entry pending")} <i aria-hidden="true">→</i> ${escapeHtml(workstream.exitGate || "Exit pending")}</span>${problemHref ? `<a href="${escapeHtml(problemHref)}" title="${escapeHtml(problemIds.join(", "))}" aria-label="Open canonical industry problems ${escapeHtml(problemIds.join(", "))}">${escapeHtml(problemLabel)} <span aria-hidden="true">↗</span></a>` : ""}</div>
        </li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function presentationEvidence(id, title, body, meta = "") {
    return `<details class="viz-presentation-detail">
      <summary>
        <span class="viz-kps-index">${escapeHtml(id)}</span>
        <span class="viz-presentation-summary-copy"><strong>${escapeHtml(title)}</strong>${meta ? `<small>${escapeHtml(meta)}</small>` : ""}</span>
        <span class="viz-presentation-action" aria-hidden="true"><span class="when-closed">Details</span><span class="when-open">Close</span></span>
      </summary>
      <div class="viz-kps-copy viz-presentation-detail-body">${body}</div>
    </details>`;
  }

  function kongPlatformFit(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    const mode = options.mode || (options.presentation ? "presentation" : "evidence");
    return `<figure class="viz viz-kps-fit ${options.compact ? "is-compact" : ""} ${options.presentation ? "is-presentation" : ""} is-${escapeHtml(mode)}" aria-label="${escapeHtml(options.title || "Kong platform outcome-fit conditions")}">${heading(options)}
      <ol class="viz-kps-fit-list">${rows.map((row, index) => {
        const id = row.projectionId || `KPS-FIT-${String(index + 1).padStart(2, "0")}`;
        const body = `
          <p class="viz-kps-mechanism" data-label="Kong mechanism">${escapeHtml(row.mechanism)}</p>
          <p class="viz-kps-reason" data-label="Scenario-relative advantage">${escapeHtml(row.reason)}</p>
          <p class="viz-kps-counter" data-label="Answer changes when">${escapeHtml(row.counterfactual)}</p>
          <p class="viz-kps-proof" data-label="Proof before commitment">${escapeHtml(row.proof)}</p>`;
        if (mode === "synopsis") {
          return `<li class="has-fit-synopsis"><details class="viz-kps-fit-contract" name="kong-fit-contract">
            <summary>
              <span class="viz-kps-index">${escapeHtml(id)}</span>
              <span class="viz-kps-fit-summary"><strong>${escapeHtml(row.outcome)}</strong><small data-label="Kong mechanism">${escapeHtml(row.mechanism)}</small></span>
              <span class="viz-kps-fit-action" aria-hidden="true"><span class="when-closed">Inspect condition</span><span class="when-open">Close condition</span></span>
            </summary>
            <div class="viz-kps-copy viz-kps-fit-contract-body">
              <p class="viz-kps-reason" data-label="Scenario-relative advantage">${escapeHtml(row.reason)}</p>
              <p class="viz-kps-counter" data-label="Answer changes when">${escapeHtml(row.counterfactual)}</p>
              <p class="viz-kps-proof" data-label="Proof before commitment">${escapeHtml(row.proof)}</p>
            </div>
          </details></li>`;
        }
        return `<li class="${mode === "presentation" ? "is-fit-contract" : ""}"><span class="viz-kps-index">${escapeHtml(id)}</span><div class="viz-kps-copy"><strong>${escapeHtml(row.outcome)}</strong>${body}</div></li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function kongPlatformProblems(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    return `<figure class="viz viz-kps-problems ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Kong platform response to P1 through P10")}">${heading(options)}
      <ol class="viz-kps-problem-list">${rows.map((row, index) => `<li>
        <span class="viz-kps-index">${escapeHtml(row.id || `P${index + 1}`)}</span>
        <div class="viz-kps-copy">
          <strong>${escapeHtml(row.problem)}</strong>
          <p class="viz-kps-response" data-label="Platform response">${escapeHtml(row.response)}</p>
          <p class="viz-kps-measure" data-label="Outcome measure">${escapeHtml(row.measure)}</p>
          <p class="viz-kps-hold" data-label="Hold condition">${escapeHtml(row.hold)}</p>
        </div>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function kongPlatformCases(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    return `<figure class="viz viz-kps-cases ${options.compact ? "is-compact" : ""} ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Synthetic Kong platform cases")}">${heading(options)}
      <ol class="viz-kps-case-list">${rows.map((row, index) => {
        const id = row.id || `KPS-C${index + 1}`;
        const body = `
          <p class="viz-kps-situation" data-label="Situation and trigger">${escapeHtml(row.situation)}</p>
          <p class="viz-kps-response" data-label="Platform response">${escapeHtml(row.response)}</p>
          <p class="viz-kps-measure" data-label="Business outcome measure">${escapeHtml(row.measure)}</p>
          <p class="viz-kps-hold" data-label="Hold / failure signal">${escapeHtml(row.hold)}</p>
          <p class="viz-kps-owner" data-label="Owner">${escapeHtml(row.owner)}</p>`;
        return options.presentation
          ? `<li class="has-presentation-detail">${presentationEvidence(id, row.label, body)}</li>`
          : `<li><span class="viz-kps-index">${escapeHtml(id)}</span><div class="viz-kps-copy"><strong>${escapeHtml(row.label)}</strong>${body}</div></li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function kongPlatformRoadmap(data, options = {}) {
    const phases = Array.isArray(data) ? data : data?.phases || [];
    if (!phases.length) return empty();
    return `<figure class="viz viz-kps-roadmap ${options.compact ? "is-compact" : ""} ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Kong platform roadmap")}">${heading(options)}
      <ol class="viz-kps-roadmap-list">${phases.map((phase, index) => {
        const id = phase.id || `KP${index}`;
        const body = `
          <p class="viz-kps-outcome" data-label="Outcome unlocked">${escapeHtml(phase.outcome)}</p>
          <p class="viz-kps-work" data-label="Platform work">${escapeHtml(phase.work)}</p>
          <p class="viz-kps-exit" data-label="Exit evidence">${escapeHtml(phase.exitEvidence)}</p>
          <p class="viz-kps-stop" data-label="Stop / replan">${escapeHtml(phase.stopCondition)}</p>`;
        return options.presentation
          ? `<li class="has-presentation-detail">${presentationEvidence(id, phase.label, body, phase.window)}</li>`
          : `<li><div class="viz-kps-roadmap-meta"><span>${escapeHtml(id)}</span><b>${escapeHtml(phase.window)}</b></div><strong>${escapeHtml(phase.label)}</strong>${body}</li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function kongPlatformOutcomes(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    return `<figure class="viz viz-kps-outcomes ${options.compact ? "is-compact" : ""} ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Kong platform outcome measures")}">${heading(options)}
      <ol class="viz-kps-outcome-list">${rows.map((row, index) => {
        const id = row.id || `KO-${index + 1}`;
        const body = `
          <p class="viz-kps-measure" data-label="Measure">${escapeHtml(row.measure)}</p>
          <p class="viz-kps-target" data-label="Scenario target form">${escapeHtml(row.target)}</p>
          <p class="viz-kps-artifact" data-label="Evidence artifact">${escapeHtml(row.artifact)}</p>
          <p class="viz-kps-cadence" data-label="Review cadence">${escapeHtml(row.cadence)}</p>
          <p class="viz-kps-owner" data-label="Accountable owner">${escapeHtml(row.owner)}</p>`;
        return options.presentation
          ? `<li class="has-presentation-detail">${presentationEvidence(id, row.label, body)}</li>`
          : `<li><span class="viz-kps-index">${escapeHtml(id)}</span><div class="viz-kps-copy"><strong>${escapeHtml(row.label)}</strong>${body}</div></li>`;
      }).join("")}</ol>
    </figure>`;
  }

  function kongOptions(data, options = {}) {
    const optionsList = Array.isArray(data) ? data : data?.options || [];
    if (!optionsList.length) return empty();
    const primaryIds = new Set(["KMC-1", "KMC-2", "KMC-3"]);
    const primary = optionsList.filter((option) => primaryIds.has(option.id));
    const attached = optionsList.filter((option) => !primaryIds.has(option.id));
    return `<figure class="viz viz-kong-options ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Kong operating-boundary options")}">${heading(options)}
      <div class="viz-kong-options-primary">${primary.map((option) => `<article aria-label="${escapeHtml(`${option.id}. ${option.journeyLabel || option.label}. ${option.journeyBoundary || option.placement}. Evidence track: ${option.journeyRole || option.role}.`)}">
        <span>${escapeHtml(option.id)}</span>
        <strong>${escapeHtml(option.journeyLabel || option.label)}</strong>
        <p data-label="Operating boundary">${escapeHtml(option.journeyBoundary || option.placement)}</p>
      </article>`).join("")}</div>
      <div class="viz-kong-options-attached" aria-label="Attached authority and hosting experiments">
        <b>Attach only after the primary operating boundary is fixed</b>
        <ol>${attached.map((option) => `<li><span>${escapeHtml(option.id)}</span><strong>${escapeHtml(option.journeyLabel || option.label)}</strong></li>`).join("")}</ol>
      </div>
    </figure>`;
  }

  function kongSelectedOption(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.rows || [];
    if (!rows.length) return empty();
    return `<figure class="viz viz-kong-selected ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Why the self-managed Kong option leads conditionally")}">${heading(options)}
      <div class="viz-kong-selected-grid">${rows.map((row) => `<article>
        <span>${escapeHtml(row.projectionId || "")}</span>
        <strong>${escapeHtml(row.outcome || "")}</strong>
        <p data-label="Why this fits here">${escapeHtml(row.reason || "")}</p>
        <p data-label="Platform response">${escapeHtml(row.mechanism || "")}</p>
        <p data-label="Reconsider when">${escapeHtml(row.counterfactual || "")}</p>
      </article>`).join("")}</div>
    </figure>`;
  }

  function kongJourneySpine(data, options = {}) {
    const phases = Array.isArray(data) ? data : data?.phases || [];
    if (!phases.length) return empty();
    return `<figure class="viz viz-kong-journey-spine" aria-label="${escapeHtml(options.title || "Kong platform journey from option to production")}">${heading(options)}
      <ol>${phases.map((phase, index) => `<li>
        <span>${escapeHtml(phase.id || String(index + 1).padStart(2, "0"))}</span>
        <strong>${escapeHtml(phase.label)}</strong>
        <p>${escapeHtml(phase.outcome)}</p>
      </li>`).join("")}</ol>
      <div class="viz-kong-journey-hold"><b>Evidence gate</b><span>Advance</span><span>Hold</span><span>Narrow</span><span>Switch custody</span><span>Exit</span></div>
    </figure>`;
  }

  function muleMigrationBoundary(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.responsibilities || [];
    if (!rows.length) return empty();
    const groups = [
      { label: "Gateway policy", ids: new Set(["G"]) },
      { label: "Owned services + platforms", ids: new Set(["F", "T", "O", "M", "B", "C"]) },
      { label: "Retire after proof", ids: new Set(["R"]) },
    ];
    return `<figure class="viz viz-mule-boundary ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Migration responsibility boundary")}">${heading(options)}
      <div class="viz-mule-boundary-groups">${groups.map((group) => `<section>
        <h3>${escapeHtml(group.label)}</h3>
        <ol>${rows.filter((row) => group.ids.has(row.id)).map((row) => `<li>
          <span>${escapeHtml(row.id)}</span>
          <div><strong>${escapeHtml(row.responsibility)}</strong><p>${escapeHtml(row.target)}</p></div>
        </li>`).join("")}</ol>
      </section>`).join("")}</div>
    </figure>`;
  }

  function muleMigrationWaves(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.waves || [];
    if (!rows.length) return empty();
    return `<figure class="viz viz-mule-waves ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Evidence-gated migration waves")}">${heading(options)}
      <ol class="viz-mule-wave-list">${rows.map((row) => `<li aria-label="${escapeHtml(`${row.id} ${row.label}. Scope: ${row.scope}. Enter when: ${row.entryGate}. Exit when: ${row.exitGate}.`)}">
        <span>${escapeHtml(row.id)}</span>
        <strong>${escapeHtml(row.label)}</strong>
        <p data-label="Exit evidence">${escapeHtml(row.exitGate)}</p>
      </li>`).join("")}</ol>
    </figure>`;
  }

  function dualMigrationRails(data, options = {}) {
    const mule = data?.mule || data?.muleMigration || {};
    const apigee = data?.apigee || data?.apigeeMigration || {};
    const muleRows = Array.isArray(mule) ? mule : (Array.isArray(mule?.waves) ? mule.waves : []);
    const apigeeRows = Array.isArray(apigee) ? apigee : (Array.isArray(apigee?.phases) ? apigee.phases : []);
    if (!muleRows.length && !apigeeRows.length) return empty();

    const rail = (sourceLabel, rows, kind) => {
      if (!rows.length) return "";
      const firstId = rows[0]?.id || "";
      const lastId = rows[rows.length - 1]?.id || "";
      const range = firstId && lastId ? `${firstId}–${lastId}` : `${rows.length} phases`;
      const rowMarkup = rows.map((row) => {
        const exitEvidence = kind === "mule" ? row.exitGate : row.exitEvidence;
        const purpose = kind === "mule" ? row.scope : row.purpose;
        const work = kind === "mule" ? row.pattern : row.work;
        const hold = kind === "mule" ? row.entryGate : row.hold;
        const accessible = [
          `${row.id || "Phase"} ${row.label || ""}`,
          purpose ? `Purpose or scope: ${purpose}` : "",
          work ? `Required work: ${work}` : "",
          exitEvidence ? `Exit evidence: ${exitEvidence}` : "",
          hold ? `${kind === "mule" ? "Entry gate" : "Hold or route-back signal"}: ${hold}` : "",
        ].filter(Boolean).join(". ");
        return `<li aria-label="${escapeHtml(accessible)}">
          <span>${escapeHtml(row.id || "")}</span>
          <strong>${escapeHtml(row.label || purpose || "Proposed phase")}</strong>
          <p data-label="Exit evidence" title="${escapeHtml(exitEvidence || "Evidence gate pending")}">${escapeHtml(exitEvidence || "Evidence gate pending")}</p>
        </li>`;
      }).join("");
      return `<section class="viz-dual-migration-rail is-${escapeHtml(kind)}">
        <header><span>Source-specific path</span><strong>${escapeHtml(sourceLabel)} ${escapeHtml(range)}</strong><small>${rows.length} evidence-gated phases</small></header>
        <ol style="--migration-step-count:${rows.length}">${rowMarkup}</ol>
      </section>`;
    };

    const body = `${rail("Mule", muleRows, "mule")}${rail("Apigee", apigeeRows, "apigee")}`;
    return `<figure class="viz viz-dual-migration ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "Mule and Apigee evidence-gated migration paths")}">${heading(options)}
      <div class="viz-dual-migration-rails">${body}</div>
    </figure>`;
  }

  function guidedRows(section, fallbackKeys = []) {
    if (Array.isArray(section)) return section;
    if (!section || typeof section !== "object") return [];
    if (Array.isArray(section.rows)) return section.rows;
    for (const key of fallbackKeys) {
      if (Array.isArray(section[key])) return section[key];
    }
    return [];
  }

  function guidedMeta(data, section, options = {}) {
    const provenance = section?.provenance || data?.provenance || {
      sourceId: data?.sourceId,
      sourcePath: data?.sourcePath,
    };
    const evidence = options.evidenceState || section?.evidenceState || "";
    const sourceClass = options.sourceClass || section?.sourceClass || "";
    if (!evidence && !sourceClass && !provenance?.sourceId && !provenance?.sourceHref) return "";
    return `<figcaption class="viz-guided-meta" aria-label="Evidence and source">
      <span>${evidence ? `<b>Evidence</b>${escapeHtml(evidence)}` : ""}</span>
      <span>${sourceClass ? `<b>Source class</b>${escapeHtml(sourceClass)}` : ""}</span>
      ${sourceLink(provenance, "Open canonical source")}
    </figcaption>`;
  }

  function guidedFrame(view, data, section, options, body, labelText) {
    return `<figure class="viz viz-guided is-${escapeHtml(slug(view))}" aria-label="${escapeHtml(labelText || options.title || "Guided evaluation visual")}">
      <div class="viz-guided-frame">${body}</div>
      ${guidedMeta(data, section, options)}
    </figure>`;
  }

  function guidedCover(data, options) {
    const section = data?.phases || {};
    const phases = guidedRows(section, ["phases"]);
    if (!phases.length) return empty();
    const body = `<ol class="viz-guided-phases">${phases.map((phase, index) => `<li>
      <span>${escapeHtml(phase.id || String(index + 1).padStart(2, "0"))}</span>
      <strong>${escapeHtml(phase.phase || phase.label)}</strong>
      <p>${escapeHtml(phase.audienceDecision || phase.outcome || "")}</p>
    </li>`).join("")}</ol>`;
    return guidedFrame("cover", data, section, options, body, options.title || "Guided decision phases");
  }

  function guidedTargetModel(data, options) {
    const section = data?.targetModel || {};
    const rows = guidedRows(section, ["lanes"]);
    if (!rows.length) return empty();
    const lanes = rows.reduce((groups, row) => {
      const lane = row.lane || row.label || "Target input";
      const current = groups.find((group) => group.lane === lane);
      if (current) current.rows.push(row);
      else groups.push({ lane, rows: [row] });
      return groups;
    }, []);
    const body = `<div class="viz-guided-target">${lanes.map((lane) => {
      const laneRows = guidedRows(lane, ["inputs", "items"]);
      return `<section>
        <h3>${escapeHtml(lane.lane || lane.label)}</h3>
        <ol>${laneRows.map((row) => `<li><strong>${escapeHtml(row.input || row.label)}</strong></li>`).join("")}</ol>
      </section>`;
    }).join("")}</div>`;
    return guidedFrame("target-model", data, section, options, body, options.title || "Stated target operating model");
  }

  function guidedRescoreContext(data, variant = "summary") {
    const section = data?.governedRescore || {};
    const rows = guidedRows(section);
    if (!rows.length) return "";
    const pendingRows = rows.filter((row) => /\b(tbd|pending|not run|unknown)\b/i.test(String(row.status || "")));
    const pendingTotal = pendingRows.length || rows.length;
    const statusLabel = pendingTotal === rows.length
      ? `${rows.length} dimensions pending`
      : `${pendingTotal} of ${rows.length} dimensions pending`;
    const details = variant === "detail"
      ? `<ul aria-label="Pending governed re-score dimensions">${rows.map((row) => `<li>
          <span>${escapeHtml(row.id || "")}</span>
          <strong>${escapeHtml(row.dimension || row.label || "Pending dimension")}</strong>
          <small>${escapeHtml(row.status || "Pending")}</small>
        </li>`).join("")}</ul>`
      : "";
    return `<aside class="viz-guided-rescore-context is-${escapeHtml(variant)}" aria-label="Governed re-score status">
      <div><span>Governed re-score</span><strong>${escapeHtml(statusLabel)}</strong></div>
      <p>Historical supplied weights and totals remain unchanged while evidence, rubric, weights, ratings, scorers, and approval stay unresolved.</p>
      ${details}
    </aside>`;
  }

  function guidedWeights(data, options) {
    const section = data?.weights || {};
    const rows = guidedRows(section);
    if (!rows.length) return empty();
    const weightValue = (row) => Math.max(0, number(String(row.weight ?? 0).replace("%", "")));
    const maxWeight = Math.max(...rows.map(weightValue), 1);
    const body = `${guidedRescoreContext(data, "detail")}<ol class="viz-guided-weights">${rows.map((row) => {
      const weight = weightValue(row);
      return `<li>
        <span>${escapeHtml(row.id || "")}</span>
        <strong>${escapeHtml(row.category || row.label)}</strong>
        <div class="viz-guided-weight-track" role="img" aria-label="${escapeHtml(`${row.category || row.label}: ${weight}%`)}"><i style="--guided-weight:${(weight / maxWeight) * 100}%"></i></div>
        <b>${escapeHtml(`${weight}%`)}</b>
      </li>`;
    }).join("")}</ol>`;
    return guidedFrame("weights", data, section, options, body, options.title || "Supplied weighting model");
  }

  function guidedOptions(data, options) {
    const section = data?.options || {};
    const requested = Array.isArray(options.rowIds) ? new Set(options.rowIds) : null;
    const rows = guidedRows(section).filter((row) => !requested || requested.has(row.id));
    if (!rows.length) return empty();
    const body = `<div class="viz-guided-options">${rows.map((row) => `<article>
      <span>${escapeHtml(row.id || "")}</span>
      <strong>${escapeHtml(row.archetype || row.label)}</strong>
      <p data-label="Strongest when">${escapeHtml(row.presentationStrongestWhen || row.strongestWhen || row.strength || "")}</p>
      <p data-label="Concern to test">${escapeHtml(row.presentationConcern || row.concern || row.test || "")}</p>
      <small>${escapeHtml(row.role || row.decisionRole || "")}</small>
    </article>`).join("")}</div>`;
    return guidedFrame("options", data, section, options, body, options.title || "Conditional operating-model archetypes");
  }

  function guidedScores(data, options, audit = false) {
    const section = data?.scoring || {};
    const rows = guidedRows(section);
    if (!rows.length) return empty();
    const names = [
      { key: "kong", inputKey: "kongInput", weightedKey: "kongWeighted", label: "Kong" },
      { key: "apigee", inputKey: "apigeeInput", weightedKey: "apigeeWeighted", label: "Apigee" },
      { key: "muleSoft", inputKey: "muleSoftInput", weightedKey: "muleSoftWeighted", label: "MuleSoft" },
    ];
    if (!audit) {
      const totals = section.totals || {};
      const maximum = Math.max(number(data?.weights?.weightTotal), ...names.map((item) => number(totals[item.key])), 1);
      const body = `${guidedRescoreContext(data)}<ol class="viz-guided-score-rank">${names
        .map((item) => ({ ...item, value: number(totals[item.key]) }))
        .sort((a, b) => b.value - a.value)
        .map((item, index) => `<li>
          <span>${String(index + 1).padStart(2, "0")}</span>
          <strong>${escapeHtml(item.label)}</strong>
          <div role="img" aria-label="${escapeHtml(`${item.label}: ${item.value}`)}"><i style="--guided-score:${(item.value / maximum) * 100}%"></i></div>
          <b>${escapeHtml(item.value)}</b>
        </li>`).join("")}</ol>`;
      return guidedFrame("score", data, section, options, body, options.title || "Supplied weighted totals");
    }
    const displayedTotals = section.displayedTotals || {};
    const body = `${guidedRescoreContext(data)}<div class="viz-guided-audit" role="table" aria-label="${escapeHtml(options.title || "Raw scoring audit")}">
      <div class="viz-guided-audit-head" role="row"><span role="columnheader">Category</span><span role="columnheader">Weight</span>${names.map((item) => `<span role="columnheader">${escapeHtml(item.label)}</span>`).join("")}</div>
      ${rows.map((row) => `<div class="viz-guided-audit-row" role="row">
        <strong role="cell">${escapeHtml(row.category || row.label)}</strong>
        <span role="cell">${escapeHtml(row.weight)}</span>
        ${names.map((item) => `<span role="cell"><b>${escapeHtml(row[item.inputKey])}</b></span>`).join("")}
      </div>`).join("")}
      <div class="viz-guided-audit-total is-supplied" role="row"><strong role="cell">Supplied displayed total</strong><span role="cell">—</span>${names.map((item) => `<b role="cell">${escapeHtml(displayedTotals[item.key] ?? "")}</b>`).join("")}</div>
      <div class="viz-guided-audit-total" role="row"><strong role="cell">Recalculated total</strong><span role="cell">${escapeHtml(data?.weights?.weightTotal || "")}</span>${names.map((item) => `<b role="cell">${escapeHtml(section.totals?.[item.key] ?? "")}</b>`).join("")}</div>
    </div>`;
    return guidedFrame("score-audit", data, section, options, body, options.title || "Raw scoring audit");
  }

  function guidedAuthorization(data, options) {
    const section = data?.authorization || data?.boundedAuthorization || data?.decision || {};
    const rows = guidedRows(section);
    if (!rows.length) return empty();
    const body = `<div class="viz-guided-authorization">
      <section class="is-authorize"><span>Authorize now</span><ul>${rows.map((row) => `<li><strong>${escapeHtml(row.decision || row.label)}</strong><p>${escapeHtml(row.authorizeNow || row.authorize || "")}</p></li>`).join("")}</ul></section>
      <section class="is-hold"><span>Not authorized</span><ul>${rows.map((row) => `<li><strong>${escapeHtml(row.decision || row.label)}</strong><p>${escapeHtml(row.doNotAuthorize || row.hold || "")}</p></li>`).join("")}</ul></section>
    </div>`;
    return guidedFrame("decision", data, section, options, body, options.title || "Bounded authorization");
  }

  function guidedBoundary(data, options) {
    const explicit = data?.boundaries || data?.boundary || {};
    const section = guidedRows(explicit).length ? explicit : data?.platformOptions || {};
    const requested = new Set(Array.isArray(options.optionIds) ? options.optionIds : []);
    const rows = guidedRows(section, ["options"])
      .filter((row) => !requested.size || requested.has(row.id))
      .slice(0, 3);
    if (!rows.length) return empty();
    const body = `<div class="viz-guided-boundaries">${rows.map((row, index) => `<article>
      <span>${escapeHtml(row.id || String(index + 1).padStart(2, "0"))}</span>
      <strong>${escapeHtml(row.boundary || row.journeyLabel || row.label)}</strong>
      <p>${escapeHtml(row.description || row.journeyBoundary || row.placement || "")}</p>
      <small>${escapeHtml(row.role || row.journeyRole || "")}</small>
    </article>`).join("")}</div>`;
    return guidedFrame("boundary", data, section, options, body, options.title || "Operating-boundary choices");
  }

  function guidedDuty(data, options) {
    const explicit = data?.duties || data?.duty || {};
    const section = guidedRows(explicit).length ? explicit : data?.platformFit || {};
    const requested = new Set(Array.isArray(options.rowIds) ? options.rowIds : []);
    const rows = guidedRows(section)
      .filter((row) => !requested.size || requested.has(row.id) || requested.has(row.projectionId))
      .slice(0, 2);
    if (!rows.length) return empty();
    const body = `<div class="viz-guided-duty">${rows.map((row) => `<article>
      <span>${escapeHtml(row.id || row.projectionId || "")}</span>
      <strong>${escapeHtml(row.duty || row.outcome || row.label)}</strong>
      <p data-label="Fit">${escapeHtml(row.fit || row.reason || row.mechanism || "")}</p>
      <p data-label="Permanent duty">${escapeHtml(row.permanentDuty || row.concern || row.counterfactual || "")}</p>
    </article>`).join("")}</div>`;
    return guidedFrame("duty", data, section, options, body, options.title || "Fit and permanent operating duty");
  }

  function guidedProofBoundary(data, options) {
    const section = data?.proofBoundary || {};
    const rows = guidedRows(section, ["systems"]);
    if (!rows.length) return empty();
    const body = `<div class="viz-guided-proof-boundary">${rows.map((row) => `<article>
      <strong>${escapeHtml(row.evidenceSystem || row.system || row.label)}</strong>
      <b>${escapeHtml(row.currentState || row.state || "")}</b>
      <p data-label="Can support">${escapeHtml(row.canSupport || row.supports || "")}</p>
      <p data-label="Cannot support">${escapeHtml(row.cannotSupport || row.doesNotSupport || row.cannot || "")}</p>
    </article>`).join("")}</div>`;
    return guidedFrame("proof-boundary", data, section, options, body, options.title || "Current proof boundary");
  }

  function guidedProofProgramme(data, options) {
    const section = data?.proofProgramme || {};
    const requested = new Set(Array.isArray(options.rowIds) ? options.rowIds : []);
    const rows = guidedRows(section).filter((row) => !requested.size || requested.has(row.id));
    if (!rows.length) return empty();
    const programmeClass = rows.length === 7 ? " is-seven" : "";
    const body = `<ol class="viz-guided-programme${programmeClass}" style="--guided-programme-count:${rows.length}">${rows.map((row) => `<li>
      <span>${escapeHtml(row.id || "")}</span>
      <strong>${escapeHtml(row.workstream || row.label)}</strong>
      <p>${escapeHtml(row.presentationSummary || row.scope || row.requiredScope || "")}</p>
    </li>`).join("")}</ol>`;
    return guidedFrame("proof-programme", data, section, options, body, options.title || "Target-aligned proof programme");
  }

  function guidedComparison(data, options, comparisonKey) {
    const section = data?.comparisons?.[comparisonKey] || {};
    const requested = new Set(Array.isArray(options.rowIds) ? options.rowIds : []);
    const rows = guidedRows(section).filter((row) => !requested.size || requested.has(row.id));
    if (!rows.length) return empty();
    const tableLabel = options.title || "Supplied comparison input";
    const body = `<div class="viz-guided-comparison-wrap" tabindex="-1" data-comparison-label="${escapeHtml(tableLabel)}">
      <table class="viz-guided-comparison">
        <caption>${escapeHtml(tableLabel)}</caption>
        <thead><tr><th scope="col">Dimension</th><th scope="col">Kong</th><th scope="col">Apigee</th><th scope="col">MuleSoft</th></tr></thead>
        <tbody>${rows.map((row) => `<tr>
          <th scope="row"><span>${escapeHtml(row.id || "")}</span>${escapeHtml(row.criterion || row.label)}</th>
          <td>${escapeHtml(row.kong || row.kongInput || "")}</td>
          <td>${escapeHtml(row.apigee || row.apigeeInput || "")}</td>
          <td>${escapeHtml(row.mulesoft || row.muleSoft || row.mulesoftInput || "")}</td>
        </tr>`).join("")}</tbody>
      </table>
    </div><p class="viz-guided-scroll-cue" aria-hidden="true" hidden>↔ Scroll to compare supplied inputs; evidence obligations remain in the canonical source</p>`;
    return guidedFrame(`comparison-${comparisonKey}`, data, section, options, body, options.title || "Supplied comparison input");
  }

  function guidedArchitectureOverview(data) {
    const control = data?.controlZone || {};
    const controlNodes = Array.isArray(control.nodes) ? control.nodes : [];
    const lanes = Array.isArray(data?.lanes) ? data.lanes : [];
    if (controlNodes.length !== 3 || lanes.length !== 3) return empty("The KGE-09 architecture overview is unavailable.");
    const node = (item, extraClass = "") => `<article class="viz-guided-architecture-node ${escapeHtml(extraClass)}">
      <strong>${escapeHtml(item?.label || "")}</strong>
      <span>${escapeHtml(item?.detail || "")}</span>
    </article>`;
    const controlFlow = (labelText) => `<span class="viz-guided-architecture-control-flow" aria-hidden="true"><b>${escapeHtml(labelText)}</b></span>`;
    const laneSummary = lanes.map((lane) => `${lane.dataPlane?.label || "Data plane"} serves ${lane.target?.label || "its local target"}`).join("; ");
    return `<figure class="viz-guided-architecture-overview" role="img" aria-label="${escapeHtml(`One enterprise control zone distributes configuration to three data-plane cells. ${laneSummary}. Evidence remains local to each lane.`)}">
      <div class="viz-guided-architecture-head" aria-hidden="true">
        <span>${escapeHtml(control.label || "Enterprise control zone")}</span>
        <div><span>${escapeHtml(data.dataPlaneLabel || "Distributed data-plane cells")}</span><span>${escapeHtml(data.targetLabel || "Local services and evidence")}</span></div>
      </div>
      <div class="viz-guided-architecture-map" aria-hidden="true">
        <section class="viz-guided-architecture-control">
          ${node(controlNodes[0], "is-authority")}
          ${controlFlow("approved intent")}
          ${node(controlNodes[1], "is-control-plane")}
          ${controlFlow("management state")}
          ${node(controlNodes[2], "is-state")}
        </section>
        <div class="viz-guided-architecture-fanout">${lanes.map((_, index) => `<span>${index === 0 ? "<b>configuration</b>" : ""}</span>`).join("")}</div>
        <ol class="viz-guided-architecture-lanes">${lanes.map((lane) => `<li>
          ${node(lane.dataPlane, "is-data-plane")}
          <span class="viz-guided-architecture-request"><b>proxy</b></span>
          ${node(lane.target, "is-local-target")}
        </li>`).join("")}</ol>
      </div>
    </figure>`;
  }

  function guidedEvaluation(data, options = {}) {
    const rawView = String(options.viewId || options.view || "cover");
    const view = rawView.replace(/^kong-guided-/, "").replace(/^guided-/, "").replace(/^compare-/, "comparison-");
    switch (view) {
      case "cover": return guidedCover(data, options);
      case "target-model": return guidedTargetModel(data, options);
      case "weights": return guidedWeights(data, options);
      case "options": return guidedOptions(data, options);
      case "score": return guidedScores(data, options);
      case "decision": return guidedAuthorization(data, options);
      case "boundary": return guidedBoundary(data, options);
      case "duty": return guidedDuty(data, options);
      case "proof-boundary": return guidedProofBoundary(data, options);
      case "proof-programme": return guidedProofProgramme(data, options);
      case "comparison-architecture": return guidedComparison(data, options, "architecture");
      case "comparison-management": return guidedComparison(data, options, "management");
      case "comparison-economics": return guidedComparison(data, options, "economics");
      case "score-audit": return guidedScores(data, options, true);
      default: return empty(`Unknown guided-evaluation view: ${rawView}`);
    }
  }

  function composition(data, options = {}) {
    const sections = data?.bySection || (Array.isArray(data) ? data : []);
    const types = data?.byType || [];
    if (!sections.length) return empty();
    return `<figure class="viz viz-composition ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Composition")}">${heading(options)}
      <div class="viz-composition-grid ${options.compact ? "is-single" : ""}">
        <div>${bars(sections, { compact: true, title: options.compact ? "" : "Study streams" })}</div>
        ${types.length && !options.compact ? `<div class="viz-type-list"><span class="viz-subhead">Formats</span>${types.slice(0, 8).map((item) => `<span><b>${escapeHtml(item.label)}</b><strong>${escapeHtml(item.value)}</strong></span>`).join("")}</div>` : ""}
      </div>
    </figure>`;
  }

  function sourceBalance(data, options = {}) {
    const vendors = data?.byVendor || (Array.isArray(data) ? data : []);
    if (!vendors.length) return empty();
    const used = number(data?.usedInFindings);
    const unused = number(data?.unusedInFindings);
    return `<figure class="viz viz-sources ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Source balance")}">${heading(options)}
      ${bars(vendors, { compact: true })}
      ${(used || unused) ? `<div class="viz-source-usage"><span><strong>${used}</strong> used in findings</span><span><strong>${unused}</strong> not yet used</span></div>` : ""}
    </figure>`;
  }

  function pocStatus(data, options = {}) {
    const statuses = data?.byStatus || (Array.isArray(data) ? data : []);
    if (!statuses.length) return empty();
    const tests = Array.isArray(data?.tests) ? data.tests : [];
    const registerTotal = number(data?.total) || total(series(statuses));
    const automatedStatus = statuses.find((item) => slug(item?.label) === "automated");
    const notRunStatus = statuses.find((item) => slug(item?.label) === "not-run");
    const automated = automatedStatus || { label: "Automated", value: 0 };
    const notRun = notRunStatus || { label: "Not run", value: 0 };
    const orderedStatuses = [
      automatedStatus,
      notRunStatus,
      ...statuses.filter((item) => !["automated", "not-run"].includes(slug(item?.label))),
    ].filter(Boolean);
    const showCohorts = tests.length && !options.compact;
    const cohorts = orderedStatuses.map((status) => {
      const label = String(status?.label || "Unknown");
      const ids = tests.filter((test) => slug(test?.status) === slug(label)).map((test) => String(test?.id || "")).filter(Boolean);
      return `<li class="is-${escapeHtml(slug(label))}">
        <div><strong>${escapeHtml(label)}</strong><b>${number(status?.value)}</b></div>
        <p>${ids.map((id) => `<code>${escapeHtml(id)}</code>`).join("")}</p>
      </li>`;
    }).join("");
    const statusLabel = orderedStatuses.map((item) => `${number(item?.value)} ${String(item?.label || "unknown")}`).join(", ");
    return `<figure class="viz viz-poc ${options.compact ? "is-compact" : ""} ${options.presentation ? "is-presentation" : ""}" aria-label="${escapeHtml(options.title || "PoC status")}">${heading(options)}
      <div class="viz-poc-score">
        <p><strong>${number(automated.value)}</strong><span>of ${registerTotal}<br/>automated baseline</span></p>
        <p class="is-hold"><strong>${number(notRun.value)}</strong><span>not run</span></p>
      </div>
      <div class="viz-poc-rail" role="img" aria-label="${escapeHtml(statusLabel)}">
        ${orderedStatuses.map((item, index) => {
          const tone = slug(item?.label) === "not-run" ? "var(--signal)" : slug(item?.label) === "automated" ? "var(--ink)" : `var(--viz-color-${index % 6})`;
          return `<span class="is-${escapeHtml(slug(item?.label))}" aria-hidden="true" style="--poc-share:${registerTotal ? (number(item?.value) / registerTotal) * 100 : 0}%;--poc-color:${tone}"></span>`;
        }).join("")}
      </div>
      ${showCohorts ? `<ol class="viz-poc-cohorts" aria-label="Scenario IDs grouped by baseline status">${cohorts}</ol>` : ""}
    </figure>`;
  }

  function governance(data, options = {}) {
    if (!data || typeof data !== "object") return empty();
    const assumptionTotal = number(data.assumptionTotal ?? total(series(data.assumptions)));
    const adrTotal = number(data.adrTotal ?? total(series(data.adrs)));
    const assumption = series(data.assumptions).length ? seriesValue(data.assumptions, "Open") : assumptionTotal;
    const adrs = series(data.adrs).length ? seriesValue(data.adrs, "Proposed") : adrTotal;
    const risks = number(data.riskTotal ?? total(series(data.risksByOwner)));
    const questions = number(data.openQuestions);
    return `<figure class="viz viz-governance ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Governance state")}">${heading(options)}
      <div class="viz-governance-metrics">
        <span><strong>${assumption}</strong><small>open assumptions · ${assumptionTotal} total</small></span>
        <span><strong>${adrs}</strong><small>proposed ADRs · ${adrTotal} total</small></span>
        <span><strong>${risks}</strong><small>registered risks</small></span>
        <span><strong>${questions}</strong><small>open questions</small></span>
      </div>
      ${options.compact ? "" : bars(data.risksByOwner || [], { compact: true, title: "Risk ownership" })}
    </figure>`;
  }

  function criteriaOverview(data, options = {}) {
    if (!data || typeof data !== "object") return empty();
    const statuses = series(data.statuses || []);
    const categories = Array.isArray(data.categories) ? data.categories : [];
    const criteriaTotal = number(data.total) || total(statuses) || categories.reduce((sum, row) => sum + number(row.total), 0);
    const unknownTotal = seriesValue(statuses, "Unknown");
    const mandatoryTotal = number(data.mandatory) || categories.reduce((sum, row) => sum + number(row.mandatory), 0);
    const weightedTotal = number(data.weighted) || categories.reduce((sum, row) => sum + number(row.weighted), 0);
    const allUnknown = criteriaTotal > 0 && unknownTotal === criteriaTotal;
    const statusCopy = allUnknown
      ? `All ${criteriaTotal} criteria retain Unknown status. No criterion-level result is presented as progress.`
      : `${unknownTotal} of ${criteriaTotal} criteria retain Unknown status.`;
    const domainRows = categories.map((row) => {
      const mandatory = number(row.mandatory);
      const weighted = number(row.weighted);
      const rowTotal = number(row.total) || mandatory + weighted;
      const rowLabel = row.label || row.id;
      return `<li aria-label="${escapeHtml(rowLabel)}: ${mandatory} mandatory, ${weighted} weighted, ${rowTotal} total">
        <strong>${escapeHtml(rowLabel)}</strong>
        <span class="is-mandatory"><small>M</small><b>${mandatory}</b></span>
        <span class="is-weighted"><small>W</small><b>${weighted}</b></span>
        <span class="is-total"><small>&Sigma;</small><b>${rowTotal}</b></span>
      </li>`;
    }).join("");
    return `<figure class="viz viz-criteria-overview ${options.compact ? "is-compact" : ""}" aria-label="${escapeHtml(options.title || "Criteria evidence state and composition")}">
      <section class="viz-criteria-state" aria-label="Evidence status">
        <span class="viz-subhead">Evidence status</span>
        <div class="viz-criteria-status"><strong>${unknownTotal}</strong><span><b>Unknown</b><small>of ${criteriaTotal} criteria</small></span></div>
        <p>${escapeHtml(statusCopy)}</p>
      </section>
      <section class="viz-criteria-composition" aria-label="Criterion composition">
        <header>
          <span class="viz-subhead">Criterion composition</span>
          <p><span><strong>${mandatoryTotal}</strong> mandatory</span><span><strong>${weightedTotal}</strong> weighted</span></p>
        </header>
        <div class="viz-criteria-key" aria-label="Allocation key"><span><b>M</b> mandatory</span><span><b>W</b> weighted</span><span><b>&Sigma;</b> total</span></div>
        <ul class="viz-criteria-domains" aria-label="Criterion allocation by domain">${domainRows}</ul>
      </section>
    </figure>`;
  }

  function recommendation(data, options = {}) {
    const rows = Array.isArray(data) ? data : data?.decisions || [];
    return statusMatrix(rows, {
      ...options,
      nameHeader: options.nameHeader || "Decision",
      statusHeader: options.statusHeader || "Status",
      noteHeader: options.noteHeader || "Recommendation and exit evidence",
    });
  }

  function documentContext(item, visuals = {}) {
    const path = item?.path || "";
    const provenance = visuals.provenance || {};
    const charts = [];
    const add = (caption, name, data, options = {}, sourceKey = "", extraClass = "") => {
      const open = charts.length === 0 ? " open" : "";
      const title = options.title || caption;
      charts.push(`<details class="document-visual document-evidence-panel ${escapeHtml(extraClass)}"${open}>
        <summary><span class="section-index">${escapeHtml(caption)}</span><strong>${escapeHtml(title)}</strong><span class="document-evidence-action" aria-hidden="true"><span class="when-closed">Open evidence</span><span class="when-open">Close evidence</span></span></summary>
        <div class="document-evidence-body">${render(name, data, { compact: true, ...options })}${sourceLink(provenance[sourceKey], "Source")}</div>
      </details>`);
    };
    if (path === "reports/methodology-review.md") {
      add("Steering recommendation", "statusMatrix", visuals.review?.decisions || [], { title: "Decision state", nameHeader: "Decision", noteHeader: "Exit evidence" }, "review");
      add("Decision readiness", "donut", visuals.criteria?.statuses || [], { title: "Criteria state", total: visuals.criteria?.total, centerLabel: "criteria" }, "criteria");
      add("Execution proof", "pocStatus", visuals.poc || {}, { title: "PoC state" }, "poc");
      add("Evidence-system roadmap", "roadmap", visuals.repositoryRoadmap || {}, { title: "Study maturity" }, "repositoryRoadmap", "is-roadmap is-wide");
    } else if (["docs/00-executive-summary.md", "decision-matrix/findings.md"].includes(path)) {
      add("Steering recommendation", "statusMatrix", visuals.review?.decisions || [], { title: "Decision state", nameHeader: "Decision" }, "review");
      add("Decision readiness", "donut", visuals.criteria?.statuses || [], { title: "Criteria state", total: visuals.criteria?.total, centerLabel: "criteria" }, "criteria");
      add("Execution proof", "pocStatus", visuals.poc || {}, { title: "PoC state" }, "poc");
    }
    if (["docs/03-assessment-methodology.md", "adr/0001-assessment-methodology.md"].includes(path)) {
      add("Assessment sequence", "methodologyFlow", visuals.methodology?.steps || [], { title: "From frame to pilot" }, "methodology");
      add("Evidence confidence", "evidenceLadder", visuals.methodology?.evidenceLevels || [], { title: "Evidence levels" }, "methodology");
    }
    if (path.startsWith("decision-matrix/") || path === "docs/09-product-shortlist.md") {
      add("Gate distribution", "stackedBars", visuals.criteria?.categories || [], { title: "Mandatory and weighted", keys: ["mandatory", "weighted"] }, "criteria");
      add("Option state", "statusMatrix", visuals.variants || [], { title: "Bounded archetypes", nameHeader: "Option" }, "variants");
    }
    if (path.startsWith("research/") || path === "docs/04-kong-first-hypothesis.md") {
      add("Research balance", "sourceBalance", visuals.sources || {}, { title: "Sources by vendor" }, "sources");
      add("Claim state", "bars", visuals.findings?.byState || [], { title: "Findings by state", horizontal: true }, "findings");
    }
    if (path.startsWith("poc/") && item?.type === "markdown") add("Scenario state", "pocStatus", visuals.poc || {}, { title: "PoC progress" }, "poc");
    if (["docs/02-current-state-assumptions.md", "docs/37-risks.md", "docs/38-open-questions.md", "adr/README.md"].includes(path)) add("Governance state", "governance", visuals.governance || {}, { title: "Open decision work" }, "governance");
    if (path === "docs/36-implementation-roadmap.md") add("Delivery sequence", "roadmap", visuals.roadmap || {}, { title: "Controlled delivery phases" }, "roadmap");
    if (path === "docs/39-repository-roadmap.md") add("Study maturity", "roadmap", visuals.repositoryRoadmap || {}, { title: "Evidence-system phases" }, "repositoryRoadmap");
    if (path === "docs/43-api-management-industry-problems.md") {
      add("Canonical problem taxonomy", "problemMatrix", visuals.industryProblems || {}, { title: "Problem → vendor mechanism → decision test", compact: false }, "industryProblems", "is-wide");
    }
    if (path === "docs/44-kong-multicloud-study-roadmap.md") {
      add("Canonical problem frame", "problemMatrix", visuals.industryProblems || {}, { title: "The cross-vendor problems this roadmap must answer" }, "industryProblems", "is-wide");
      add("Kong study sequence", "studyRoadmap", visuals.kongMulticloud || {}, { title: "Workstreams, gates, and scenario ranges", compact: false }, "kongMulticloud", "is-wide");
    }
    if (!charts.length) return "";
    return `<section class="document-visual-context" aria-label="Related decision evidence"><header><p class="eyebrow">Decision context</p><h2>How this source relates to the current evidence.</h2></header><div class="document-visual-grid">${charts.join("")}</div></section>`;
  }

  function documentPlacements(item, visuals = {}) {
    const placement = (headingId, index, title, chart, source) => ({
      headingId,
      markup: `<section class="document-visual-context is-inline is-placed" aria-label="${escapeHtml(title)}">
        <header><p class="eyebrow">Article figure / ${escapeHtml(index)}</p><h2>${escapeHtml(title)}</h2>${sourceLink(source, "Canonical source")}</header>
        <div class="document-visual-grid"><div class="document-visual is-wide">${chart}</div></div>
      </section>`,
    });
    if (item?.path === "docs/45-api-management-industry-practices.md") {
      const source = visuals.provenance?.industryPractices;
      return [
        placement("best-practice-framework-mapped-to-p1-p10", "A", "The ten-practice operating contract", practiceFramework(visuals.industryPractices || {}, { title: "Problem → practice → evidence → hold condition" }), source),
        placement("realistic-enterprise-scenarios", "B", "Eight realistic scenarios connect failure to proof", scenarioMatrix(visuals.industryPractices || {}, { title: "Scenario → failure → control → measurable acceptance" }), source),
        placement("capability-maturity-and-adoption-sequence", "C", "Adoption advances only through evidence gates", maturitySequence(visuals.industryPractices || {}, { title: "Operating outcome → required evidence → exit gate" }), source),
      ];
    }
    if (item?.path === "docs/47-kong-enterprise-platform-strategy.md") {
      const strategy = visuals.kongPlatformStrategy || {};
      return [
        placement("why-kong-is-the-better-fit-here", "KPS / A", "Seven conditions make Kong a scenario-relative fit", kongPlatformFit(strategy.fit || {}, { title: "Outcome → mechanism → counterfactual → proof" }), strategy.fit?.provenance),
        placement("industry-problem-traceability-p1-p10", "KPS / B", "P1–P10 remain outcome and hold gates", kongPlatformProblems(strategy.problems || {}, { title: "Problem → platform response → outcome → hold" }), strategy.problems?.provenance),
        placement("realistic-synthetic-enterprise-cases", "KPS / C", "Eight synthetic cases connect response to business outcome", kongPlatformCases(strategy.cases || {}, { title: "Trigger → response → business measure → hold" }), strategy.cases?.provenance),
        placement("0-18-month-platform-roadmap", "KPS / D", "Scale advances only through six evidence gates", kongPlatformRoadmap(strategy.roadmap || {}, { title: "Platform phase → outcome → exit evidence → stop" }), strategy.roadmap?.provenance),
        placement("outcome-measures-and-acceptance-artifacts", "KPS / E", "Eleven measures make platform outcomes reviewable", kongPlatformOutcomes(strategy.outcomes || {}, { title: "Outcome → target → artifact → cadence → owner" }), strategy.outcomes?.provenance),
      ];
    }
    return [];
  }

  function atlas(visuals = {}) {
    const criteria = visuals.criteria || {};
    const sources = visuals.sources || {};
    const provenance = visuals.provenance || {};
    const criteriaTotal = number(criteria.total);
    const unknownCriteria = series(criteria.statuses).length ? seriesValue(criteria.statuses, "Unknown") : criteriaTotal;
    const evidencedCriteria = Math.max(criteriaTotal - unknownCriteria, 0);
    const variantCount = Array.isArray(visuals.variants) ? visuals.variants.length : 0;
    const pocTotal = number(visuals.poc?.total);
    const pocNotRun = seriesValue(visuals.poc?.byStatus || [], "Not run");
    const repositoryPhases = visuals.repositoryRoadmap?.phases || [];
    const deliveryPhases = visuals.roadmap?.phases || [];
    const problemTotal = number(visuals.industryProblems?.total);
    const practiceTotal = number(visuals.industryPractices?.practiceTotal);
    const scenarioTotal = number(visuals.industryPractices?.scenarioTotal);
    const maturityStageTotal = number(visuals.industryPractices?.stageTotal);
    const kongWorkstreamTotal = number(visuals.kongMulticloud?.workstreamTotal);
    const kongPlatform = visuals.kongPlatformStrategy || {};
    const kongFitTotal = number(kongPlatform.fit?.rowTotal);
    const kongCaseTotal = number(kongPlatform.cases?.rowTotal);
    const kongPhaseTotal = number(kongPlatform.roadmap?.rowTotal);
    const kongOutcomeTotal = number(kongPlatform.outcomes?.rowTotal);
    const panel = (index, eyebrow, title, note, body, extraClass = "", source = null) => `<details class="visual-panel atlas-panel ${escapeHtml(extraClass)}"${index === "01" ? " open" : ""}><summary class="visual-panel-heading"><span class="section-index">${escapeHtml(index)} / ${escapeHtml(eyebrow)}</span><h2>${escapeHtml(title)}</h2><p>${escapeHtml(note)}</p><span class="atlas-panel-action"><span class="when-closed">Open visual</span><span class="when-open">Close visual</span></span></summary><div class="visual-panel-body">${sourceLink(source)}${body}</div></details>`;
    return `<div class="page-shell visual-atlas">
      <header class="page-intro"><div><p class="eyebrow">Decision evidence, drawn</p><h1>Visual Atlas</h1><p class="lede">Charts, matrices, timelines, and system models generated from the repository’s real assessment data.</p></div><p class="intro-note">These views expose evidence state and study structure. They do not manufacture platform scores where the underlying scorecards remain unknown.</p></header>
      <section class="visual-grid" aria-label="Decision readiness visualizations">
        ${panel("01", "Recommendation", "Proceed with bounded, reversible Kong foundation work", "The stakeholder direction focuses investment while the evidence contract keeps production fit, critical scale, Konnect custody-switch, and true-exit decisions explicit.", statusMatrix(visuals.review?.decisions || [], { title: "Steering decision state", nameHeader: "Decision", noteHeader: "Exit evidence" }), "is-wide", provenance.review)}
        ${panel("02", "Readiness", `${evidencedCriteria} of ${criteriaTotal} criteria have a recorded evidence state`, "Evidence coverage must be earned before products can be ranked.", donut(criteria.statuses || [], { title: "Criteria evidence state", total: criteria.total, centerLabel: "criteria", tone: "signal" }), "is-compact", provenance.criteria)}
        ${panel("03", "Gate structure", `${number(criteria.mandatory)} mandatory gates stay explicit`, "Mandatory and weighted requirements are visible by decision category.", stackedBars(criteria.categories || [], { title: "Mandatory and weighted criteria", keys: ["mandatory", "weighted"] }), "is-wide", provenance.criteria)}
        ${panel("04", "Option state", `${variantCount} bounded deployment archetypes`, "Each archetype needs a resolved Gate-1 bill of materials before it can receive evidence or a scorecard.", statusMatrix(visuals.variants || [], { title: "Option-resolution state", nameHeader: "Option" }), "is-wide", provenance.variants)}
        ${panel("05", "Research balance", `${number(sources.total)} registered official sources`, "Official-source volume is not the same as criterion coverage, but imbalance is an important review signal.", sourceBalance(sources, { title: "Official sources by vendor" }), "", provenance.sources)}
        ${panel("06", "Finding state", `${number(visuals.findings?.total)} tracked claims and interpretations`, "The claim register distinguishes confirmed findings, interpretations, and risks.", bars(visuals.findings?.byState || [], { title: "Findings by state" }), "", provenance.findings)}
        ${panel("07", "Source use", `${number(sources.usedInFindings)} source IDs are used in findings`, "A registered source is not decision evidence until it is tied to a claim or criterion.", donut([{ label: "Used in findings", value: sources.usedInFindings || 0 }, { label: "Not yet used", value: sources.unusedInFindings || 0 }], { title: "Source use in findings", centerLabel: "sources" }), "", provenance.sources)}
        ${panel("08", "Proof", `${pocNotRun} of ${pocTotal} scenarios are not run`, "Automated baseline checks are separated from unexecuted enterprise scenarios.", pocStatus(visuals.poc || {}, { title: "PoC scenario state" }), "is-wide", provenance.poc)}
        ${panel("09", "Governance", "Open work remains explicit", "Assumptions, decisions, risks, and open questions remain visible until accountable roles close them.", governance(visuals.governance || {}, { title: "Decision governance" }), "is-wide", provenance.governance)}
        ${panel("10", "Method", `${(visuals.methodology?.steps || []).length} gated assessment steps`, "Evidence confidence increases as claims move from documentation to repeatable labs and representative pilots.", methodologyFlow(visuals.methodology?.steps || [], { title: "Assessment sequence" }), "is-wide", provenance.methodology)}
        ${panel("11", "Evidence", `${(visuals.methodology?.evidenceLevels || []).length} confidence levels`, "Marketing assertion, official documentation, vendor confirmation, labs, and pilots are not interchangeable.", evidenceLadder(visuals.methodology?.evidenceLevels || [], { title: "Evidence ladder" }), "", provenance.methodology)}
        ${panel("12", "Delivery roadmap", `${deliveryPhases.length} controlled delivery phases`, "The organization plan uses exit evidence and decision rights rather than dates masquerading as commitments.", roadmap(visuals.roadmap || {}, { title: "Assessment-to-decommission sequence" }), "is-wide", provenance.roadmap)}
        ${panel("13", "Study roadmap", `${repositoryPhases.length} evidence-system phases`, "The repository moves through explicit decision-assurance gates before becoming a continuous study platform.", roadmap(visuals.repositoryRoadmap || {}, { title: "Repository maturity sequence" }), "is-wide", provenance.repositoryRoadmap)}
        ${panel("14", "Library", "The evidence base has shape", "Repository composition shows where the study is deep and where additional evidence will accumulate.", composition(visuals.library || {}, { title: "Resources by study stream" }), "is-wide", provenance.library)}
        ${panel("15", "Industry agenda", `${problemTotal} enduring problem families`, "The canonical taxonomy keeps vendor packaging subordinate to enterprise outcomes and equivalent proof.", problemMatrix(visuals.industryProblems || {}, { title: "Problem and mechanism map", compact: true }), "is-wide", provenance.industryProblems)}
        ${panel("16", "Kong roadmap", `${kongWorkstreamTotal} gated study workstreams`, "The stakeholder-selected Kong direction advances from reversible foundation to production scale only through exact options, explicit owners, prerequisite gates, and decision evidence.", studyRoadmap(visuals.kongMulticloud || {}, { title: "Kong study sequence", compact: true }), "is-wide", provenance.kongMulticloud)}
        ${panel("17", "Industry practices", `${practiceTotal} problem-bound operating practices`, "Each practice connects the required control to its minimum mechanism, acceptance evidence, and an explicit hold condition.", practiceFramework(visuals.industryPractices || {}, { title: "Practice contract", compact: true }), "is-wide", provenance.industryPractices)}
        ${panel("18", "Realistic cases", `${scenarioTotal} synthetic practice scenarios`, "RE-1 and case-local assumptions expose failure mechanisms, accountable controls, measurable acceptance, and named owner roles without pretending to be benchmark results.", scenarioMatrix(visuals.industryPractices || {}, { title: "Scenario-to-proof matrix", compact: true }), "is-wide", provenance.industryPractices)}
        ${panel("19", "Adoption gates", `${maturityStageTotal} evidence-gated maturity stages`, "Capability advances through operating outcomes and exit evidence; ownership and runtime-custody choices remain orthogonal design decisions.", maturitySequence(visuals.industryPractices || {}, { title: "Capability maturity sequence", compact: true }), "is-wide", provenance.industryPractices)}
        ${panel("20", "Kong platform fit", `${kongFitTotal} scenario-relative fit conditions`, "Scan the outcome and mechanism pairs, then inspect the counterfactual and proof for the condition under review; this is not a universal product ranking.", kongPlatformFit(kongPlatform.fit || {}, { title: "Outcome-fit contract", compact: true, mode: "synopsis" }), "is-wide", kongPlatform.fit?.provenance)}
        ${panel("21", "Kong problem response", "P1–P10 stay tied to measurable hold gates", "The selected-platform posture does not mark an industry problem solved; each response remains conditional on outcome evidence.", kongPlatformProblems(kongPlatform.problems || {}, { title: "Problem-to-proof traceability", compact: true }), "is-wide", kongPlatform.problems?.provenance)}
        ${panel("22", "Kong realistic cases", `${kongCaseTotal} synthetic enterprise cases`, "Management loss, clean-node scale, trust rollover, burst faults, change defects, regional loss, coexistence, and restore remain labelled test scenarios.", kongPlatformCases(kongPlatform.cases || {}, { title: "Case-to-outcome contract", compact: true }), "is-wide", kongPlatform.cases?.provenance)}
        ${panel("23", "Kong platform roadmap", `${kongPhaseTotal} evidence-gated phases across a 0–18 month scenario`, "Elapsed windows are assumptions; each phase advances through exit evidence and preserves a stop or replan condition.", kongPlatformRoadmap(kongPlatform.roadmap || {}, { title: "Foundation-to-scale sequence", compact: true }), "is-wide", kongPlatform.roadmap?.provenance)}
        ${panel("24", "Kong outcome system", `${kongOutcomeTotal} outcome and acceptance contracts`, "Active state, business reliability, trust, recovery, change, capacity, evidence, adoption, sustainability, exit, and estate truth each have an artifact, cadence, and owner.", kongPlatformOutcomes(kongPlatform.outcomes || {}, { title: "Outcome review contract", compact: true }), "is-wide", kongPlatform.outcomes?.provenance)}
      </section>
    </div>`;
  }

  const renderers = {
    bars,
    bar: bars,
    stackedBars,
    stacked: stackedBars,
    donut,
    ring: donut,
    evidenceLadder,
    ladder: evidenceLadder,
    statusMatrix,
    matrix: statusMatrix,
    methodologyFlow,
    flow: methodologyFlow,
    roadmap,
    timeline: roadmap,
    problemMatrix,
    problems: problemMatrix,
    practiceFramework,
    practices: practiceFramework,
    scenarioMatrix,
    scenarios: scenarioMatrix,
    maturitySequence,
    maturity: maturitySequence,
    studyRoadmap,
    kongPlatformFit,
    kongPlatformProblems,
    kongPlatformCases,
    kongPlatformRoadmap,
    kongPlatformOutcomes,
    kongOptions,
    kongSelectedOption,
    kongJourneySpine,
    muleMigrationBoundary,
    muleMigrationWaves,
    dualMigrationRails,
    guidedEvaluation,
    guidedArchitectureOverview,
    composition,
    sourceBalance,
    sources: sourceBalance,
    pocStatus,
    poc: pocStatus,
    governance,
    criteriaOverview,
    criteria: criteriaOverview,
    recommendation,
  };

  function render(name, data, options = {}) {
    const renderer = renderers[name];
    return renderer ? renderer(data, options) : empty(`Unknown visualization: ${name}`);
  }

  function mount(target, name, data, options = {}) {
    const element = typeof target === "string" ? document.querySelector(target) : target;
    if (!element) return null;
    element.innerHTML = render(name, data, options);
    return element;
  }

  function dataFor(name, visuals) {
    const map = {
      criteria: visuals?.criteria,
      variants: visuals?.variants,
      sources: visuals?.sources,
      findings: visuals?.findings?.byState,
      poc: visuals?.poc,
      governance: visuals?.governance,
      library: visuals?.library,
      roadmap: visuals?.roadmap,
      methodology: visuals?.methodology?.steps,
      evidence: visuals?.methodology?.evidenceLevels,
      review: visuals?.review,
      recommendation: visuals?.review,
      problemMatrix: visuals?.industryProblems,
      problems: visuals?.industryProblems,
      practiceFramework: visuals?.industryPractices,
      practices: visuals?.industryPractices,
      scenarioMatrix: visuals?.industryPractices,
      scenarios: visuals?.industryPractices,
      maturitySequence: visuals?.industryPractices,
      maturity: visuals?.industryPractices,
      studyRoadmap: visuals?.kongMulticloud,
      kongPlatformFit: visuals?.kongPlatformStrategy?.fit,
      kongPlatformProblems: visuals?.kongPlatformStrategy?.problems,
      kongPlatformCases: visuals?.kongPlatformStrategy?.cases,
      kongPlatformRoadmap: visuals?.kongPlatformStrategy?.roadmap,
      kongPlatformOutcomes: visuals?.kongPlatformStrategy?.outcomes,
      kongOptions: visuals?.kongMulticloud,
      kongSelectedOption: visuals?.kongPlatformStrategy?.fit,
      kongJourneySpine: visuals?.kongPlatformJourney,
      muleMigrationBoundary: visuals?.muleMigration,
      muleMigrationWaves: visuals?.muleMigration,
      dualMigrationRails: { mule: visuals?.muleMigration, apigee: visuals?.apigeeMigration },
      guidedEvaluation: visuals?.guidedEvaluation,
      guidedArchitectureOverview: visuals?.kongPlatformStrategy?.guidedArchitectureOverview,
    };
    return map[name] ?? visuals?.[name];
  }

  function mountAll(root = document, visuals = {}) {
    root.querySelectorAll("[data-viz]").forEach((target) => {
      const name = target.dataset.viz;
      const key = target.dataset.vizData || name;
      mount(target, name, dataFor(key, visuals), { title: target.dataset.vizTitle || "", compact: target.dataset.vizCompact === "true" });
    });
  }

  window.ApiStudyCharts = {
    render,
    mount,
    mountAll,
    legend,
    bars,
    stackedBars,
    donut,
    evidenceLadder,
    statusMatrix,
    methodologyFlow,
    roadmap,
    problemMatrix,
    practiceFramework,
    scenarioMatrix,
    maturitySequence,
    studyRoadmap,
    kongPlatformFit,
    kongPlatformProblems,
    kongPlatformCases,
    kongPlatformRoadmap,
    kongPlatformOutcomes,
    kongOptions,
    kongSelectedOption,
    kongJourneySpine,
    muleMigrationBoundary,
    muleMigrationWaves,
    dualMigrationRails,
    guidedEvaluation,
    guidedArchitectureOverview,
    composition,
    sourceBalance,
    pocStatus,
    governance,
    criteriaOverview,
    recommendation,
    documentContext,
    documentPlacements,
    atlas,
    escapeHtml,
  };
})();
