(() => {
  "use strict";

  const SCHEMA_VERSION = 2;
  const EVIDENCE_LEVELS = Object.freeze(["E0", "E1", "E2", "E3", "E4"]);
  const OUTCOMES = new Set(["pass", "amend", "hold", "unknown", "not-applicable", "inform"]);
  const HOLD_RULE_STATUSES = Object.freeze(["open", "closed"]);
  const MEETING_DECISIONS = Object.freeze(["approve", "amend", "hold"]);
  const PUBLIC_ROLES = Object.freeze([
    "Decision owner",
    "Enterprise architecture",
    "Platform product",
    "Security architecture",
    "IAM",
    "SRE/performance",
    "FinOps",
    "Migration lead",
    "Independent assurance",
    "Legal/procurement",
    "Service owner",
    "Unassigned role",
  ]);
  const memoryStores = new Map();
  const limits = Object.freeze({
    id: 120,
    label: 160,
    decision: 2000,
    reference: 500,
    rationale: 2000,
    role: 160,
    gate: 160,
    scope: 3000,
    record: 3000,
    request: 2000,
  });

  const restrictedPatterns = Object.freeze([
    { label: "email address", pattern: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i },
    { label: "IP address", pattern: /\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[A-F0-9]{1,4}:){2,}[A-F0-9:]{1,4}\b/i },
    { label: "private URL", pattern: /https?:\/\/(?:localhost|127\.0\.0\.1|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|[^/\s]+\.(?:internal|local|corp|lan))(?:[/:?#]|\b)/i },
    { label: "credential-like value", pattern: /(?:password|passwd|secret|api[_ -]?key|access[_ -]?token|authorization|bearer)\s*[:=]\s*\S+|-----BEGIN [A-Z ]*PRIVATE KEY-----/i },
    { label: "phone number", pattern: /(?:\+?\d[\s().-]*){9,}\d/ },
    { label: "commercial quote", pattern: /(?:\$|CAD\s|USD\s|EUR\s)\d[\d,.]*(?:\s*(?:per|\/)(?:month|year|request|unit))?/i },
  ]);

  function boundedText(value, limit) {
    return String(value ?? "")
      .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "")
      .slice(0, limit);
  }

  function publicSafeText(value, limit, options = {}) {
    const text = boundedText(value, limit);
    const safe = restrictedPatterns.some(({ pattern }) => pattern.test(text)) ? "" : text;
    return options.trim === false ? safe : safe.trim();
  }

  function privacyFinding(value) {
    const text = boundedText(value, limits.record);
    return restrictedPatterns.find(({ pattern }) => pattern.test(text))?.label || "";
  }

  function cleanId(value) {
    return boundedText(value, limits.id).trim();
  }

  function cleanRecordId(value) {
    const text = publicSafeText(value, limits.id);
    return /^[A-Za-z0-9][A-Za-z0-9._:/-]*$/.test(text) ? text : "";
  }

  function cleanRevision(value) {
    const text = boundedText(value, limits.id).trim();
    return /^[0-9a-f]{40,64}$/i.test(text) ? text : "";
  }

  function cleanPublicRole(value) {
    const role = publicSafeText(value, limits.role);
    return PUBLIC_ROLES.includes(role) ? role : "";
  }

  function cleanDate(value) {
    const text = boundedText(value, 40).trim();
    return text && !Number.isNaN(Date.parse(text)) ? text : "";
  }

  function questionsFor(contract) {
    return contract?.schemaVersion === SCHEMA_VERSION && Array.isArray(contract.questions)
      ? contract.questions.filter((question) => cleanId(question?.id))
      : [];
  }

  function choiceSetsFor(contract) {
    const sets = Array.isArray(contract?.choiceSets) ? contract.choiceSets : [];
    return new Map(sets.map((set) => [cleanId(set?.id), set]));
  }

  function choicesFor(question, choiceSets) {
    const choices = choiceSets.get(cleanId(question?.choiceSetId))?.choices;
    return Array.isArray(choices)
      ? choices.filter((choice) => cleanId(choice?.value) && OUTCOMES.has(choice?.outcome))
      : [];
  }

  function emptyResponse() {
    return {
      choice: "",
      holdRuleStatus: "open",
      evidenceLevel: "E0",
      evidenceReference: "",
      rationale: "",
      ownerRole: "",
      dueGate: "",
      criterionId: "",
      optionId: "",
      evidenceRequest: "",
      restrictedReferenceId: "",
      dissent: "",
      nextForum: "",
    };
  }

  function normalizeResponse(question, rawResponse, choiceSets, options = {}) {
    const source = rawResponse && typeof rawResponse === "object" ? rawResponse : {};
    const validChoices = new Set(choicesFor(question, choiceSets).map((choice) => cleanId(choice.value)));
    const choice = cleanId(source.choice);
    const evidenceLevel = cleanId(source.evidenceLevel).toUpperCase();
    const holdRuleStatus = cleanId(source.holdRuleStatus);
    const textOptions = { trim: options.trimFreeText !== false };
    return {
      choice: validChoices.has(choice) ? choice : "",
      holdRuleStatus: HOLD_RULE_STATUSES.includes(holdRuleStatus) ? holdRuleStatus : "open",
      evidenceLevel: EVIDENCE_LEVELS.includes(evidenceLevel) ? evidenceLevel : "E0",
      evidenceReference: publicSafeText(source.evidenceReference, limits.reference, textOptions),
      rationale: publicSafeText(source.rationale ?? source.notes, limits.rationale, textOptions),
      ownerRole: cleanPublicRole(source.ownerRole),
      dueGate: publicSafeText(source.dueGate, limits.gate, textOptions),
      criterionId: cleanRecordId(source.criterionId),
      optionId: cleanRecordId(source.optionId),
      evidenceRequest: publicSafeText(source.evidenceRequest, limits.request, textOptions),
      restrictedReferenceId: cleanRecordId(source.restrictedReferenceId),
      dissent: publicSafeText(source.dissent, limits.record, textOptions),
      nextForum: publicSafeText(source.nextForum, limits.gate, textOptions),
    };
  }

  function normalizeAssessment(contract, raw = {}, options = {}) {
    const source = raw && typeof raw === "object" ? raw : {};
    const choiceSets = choiceSetsFor(contract);
    const textOptions = { trim: options.trimFreeText !== false };
    const responses = {};
    questionsFor(contract).forEach((question) => {
      const questionId = cleanId(question.id);
      responses[questionId] = normalizeResponse(question, source.responses?.[questionId], choiceSets, options);
    });
    return {
      schemaVersion: SCHEMA_VERSION,
      deckId: cleanId(source.deckId || contract?.deckId || "kong-platform-journey-guided"),
      deckRevision: cleanRevision(contract?.deckRevision),
      label: publicSafeText(source.label, limits.label, textOptions),
      meetingDecision: MEETING_DECISIONS.includes(cleanId(source.meetingDecision).toLowerCase())
        ? cleanId(source.meetingDecision).toLowerCase()
        : "",
      decisionOwnerRole: cleanPublicRole(source.decisionOwnerRole),
      authorizedScope: publicSafeText(source.authorizedScope, limits.scope, textOptions),
      unauthorizedScope: publicSafeText(source.unauthorizedScope, limits.scope, textOptions),
      assumptions: publicSafeText(source.assumptions, limits.record, textOptions),
      actions: publicSafeText(source.actions, limits.record, textOptions),
      dissent: publicSafeText(source.dissent, limits.record, textOptions),
      nextForum: publicSafeText(source.nextForum, limits.gate, textOptions),
      holdReason: publicSafeText(source.holdReason, limits.record, textOptions),
      createdAt: cleanDate(source.createdAt),
      updatedAt: cleanDate(source.updatedAt),
      expiresAt: cleanDate(source.expiresAt),
      responses,
    };
  }

  function evidenceRank(level) {
    const rank = EVIDENCE_LEVELS.indexOf(level);
    return rank < 0 ? 0 : rank;
  }

  function fieldResolved(record, field) {
    if (!record?.[field] || (typeof record[field] === "string" && !record[field].trim())) return false;
    if (["ownerRole", "decisionOwnerRole"].includes(field)) return record[field] !== "Unassigned role";
    if (field === "holdRuleStatus") return record[field] === "closed";
    return true;
  }

  function summarizeQuestion(question, response, choiceSets, reviewRequirements) {
    const choices = choicesFor(question, choiceSets);
    const selected = choices.find((choice) => cleanId(choice.value) === response.choice);
    const outcome = selected?.outcome || "";
    const minimumEvidence = EVIDENCE_LEVELS.includes(question?.minimumEvidence)
      ? question.minimumEvidence
      : "E0";
    const gaps = [];
    if (selected && outcome !== "not-applicable" && evidenceRank(response.evidenceLevel) < evidenceRank(minimumEvidence)) {
      gaps.push("evidence");
    }
    if (selected && outcome === "not-applicable" && !response.rationale) gaps.push("rationale");
    const evidenceClaimRequired = Array.isArray(reviewRequirements?.evidenceClaimRequired)
      ? reviewRequirements.evidenceClaimRequired.map(cleanId)
      : ["evidenceReference"];
    if (selected && outcome !== "not-applicable" && evidenceRank(response.evidenceLevel) >= evidenceRank(minimumEvidence)) {
      evidenceClaimRequired.forEach((field) => {
        if (!response[field]) gaps.push(field);
      });
    }
    if (selected && outcome !== "not-applicable" && response.holdRuleStatus !== "closed") {
      gaps.push("holdRuleStatus");
    }
    if (selected && question.mandatory === true) {
      const mandatoryRequired = Array.isArray(reviewRequirements?.mandatoryResponseRequired)
        ? reviewRequirements.mandatoryResponseRequired.map(cleanId)
        : ["rationale", "ownerRole", "dueGate", "holdRuleStatus"];
      mandatoryRequired.forEach((field) => {
        const missing = !fieldResolved(response, field);
        if (missing && !gaps.includes(field)) gaps.push(field);
      });
    }
    const status = selected ? outcome : "unanswered";
    return {
      id: cleanId(question.id),
      phaseId: cleanId(question.phaseId),
      slideIds: Array.isArray(question.slideIds) ? question.slideIds.map(cleanId).filter(Boolean) : [],
      targetIds: Array.isArray(question.targetIds) ? question.targetIds.map(cleanId).filter(Boolean) : [],
      prompt: boundedText(question.prompt, 1200).trim(),
      decisionUse: boundedText(question.decisionUse, 800).trim(),
      evidenceBoundary: boundedText(question.evidenceBoundary, 800).trim(),
      holdRule: boundedText(question.holdRule, 1200).trim(),
      minimumEvidence,
      mandatory: question.mandatory === true,
      choiceSetId: cleanId(question.choiceSetId),
      choiceLabel: boundedText(selected?.label, 240).trim(),
      outcome,
      status,
      gaps,
      response: { ...response },
    };
  }

  function summarizeAssessment(contract, normalized, options = {}) {
    const session = normalizeAssessment(contract, normalized);
    const choiceSets = choiceSetsFor(contract);
    const reviewRequirements = contract?.reviewRequirements && typeof contract.reviewRequirements === "object"
      ? contract.reviewRequirements
      : {};
    const questions = questionsFor(contract).map((question) => (
      summarizeQuestion(question, session.responses[cleanId(question.id)] || emptyResponse(), choiceSets, reviewRequirements)
    ));
    const mandatoryQuestions = questions.filter((question) => question.mandatory);
    const questionHold = questions.some((question) => (
      question.outcome === "hold"
      || question.outcome === "unknown"
      || question.gaps.includes("holdRuleStatus")
      || (question.mandatory && (question.status === "unanswered" || question.gaps.length > 0))
    ));
    const requiredSessionFields = Array.isArray(reviewRequirements.sessionRequired)
      ? reviewRequirements.sessionRequired.map(cleanId)
      : ["meetingDecision", "decisionOwnerRole", "authorizedScope", "unauthorizedScope", "nextForum"];
    const sessionGaps = requiredSessionFields.filter((field) => !fieldResolved(session, field));
    const mandatoryResolved = mandatoryQuestions.length > 0 && mandatoryQuestions.every((question) => (
      ["pass", "inform", "not-applicable"].includes(question.outcome) && question.gaps.length === 0
    ));
    const requiresAmendment = session.meetingDecision === "amend"
      || questions.some((question) => question.outcome === "amend" || question.gaps.length > 0);
    let decisionState = session.meetingDecision === "hold" || questionHold || sessionGaps.length > 0
      ? "hold"
      : session.meetingDecision === "approve" && mandatoryResolved && !requiresAmendment
        ? "reviewable"
        : "amend";
    if (decisionState === "hold") {
      const holdStateRequired = Array.isArray(reviewRequirements.holdStateRequired)
        ? reviewRequirements.holdStateRequired.map(cleanId)
        : ["holdReason"];
      holdStateRequired.forEach((field) => {
        if (!fieldResolved(session, field) && !sessionGaps.includes(field)) sessionGaps.push(field);
      });
    }
    if (sessionGaps.length > 0) decisionState = "hold";
    const evidenceSupported = questions.filter((question) => (
      question.status !== "unanswered"
      && question.outcome !== "not-applicable"
      && evidenceRank(question.response.evidenceLevel) >= evidenceRank(question.minimumEvidence)
      && !question.gaps.includes("evidenceReference")
    ));
    const holds = questions
      .filter((question) => ["hold", "unknown"].includes(question.outcome) || question.gaps.includes("holdRuleStatus") || (question.mandatory && (question.status === "unanswered" || question.gaps.length > 0)))
      .map((question) => question.id)
      .concat(sessionGaps.map((field) => `session:${field}`));
    const gaps = questions
      .filter((question) => question.gaps.length > 0)
      .map((question) => ({ questionId: question.id, types: [...question.gaps] }));
    const counts = {
      total: questions.length,
      answered: questions.filter((question) => question.status !== "unanswered").length,
      unanswered: questions.filter((question) => question.status === "unanswered").length,
      mandatory: mandatoryQuestions.length,
      pass: questions.filter((question) => question.outcome === "pass").length,
      amend: questions.filter((question) => question.outcome === "amend").length,
      hold: questions.filter((question) => question.outcome === "hold").length,
      unknown: questions.filter((question) => question.outcome === "unknown").length,
      notApplicable: questions.filter((question) => question.outcome === "not-applicable").length,
      questionGaps: questions.filter((question) => question.gaps.length > 0).length,
      sessionGaps: sessionGaps.length,
      gaps: questions.filter((question) => question.gaps.length > 0).length + sessionGaps.length,
      evidenceSupported: evidenceSupported.length,
    };
    const phaseQuestionIds = contract?.phaseQuestionIds && typeof contract.phaseQuestionIds === "object"
      ? contract.phaseQuestionIds
      : {};
    const phaseIds = [...new Set([
      ...Object.keys(phaseQuestionIds),
      ...questions.map((question) => question.phaseId).filter(Boolean),
    ])];
    const phases = phaseIds.map((phaseId) => {
      const configuredIds = Array.isArray(phaseQuestionIds[phaseId]) ? phaseQuestionIds[phaseId].map(cleanId) : [];
      const questionIds = configuredIds.length
        ? configuredIds.filter((id) => questions.some((question) => question.id === id))
        : questions.filter((question) => question.phaseId === phaseId).map((question) => question.id);
      const phaseQuestions = questions.filter((question) => questionIds.includes(question.id));
      return {
        phaseId: cleanId(phaseId),
        questionIds,
        answered: phaseQuestions.filter((question) => question.status !== "unanswered").length,
        unanswered: phaseQuestions.filter((question) => question.status === "unanswered").length,
        gaps: phaseQuestions.filter((question) => question.gaps.length > 0).length,
      };
    });
    return {
      schemaVersion: SCHEMA_VERSION,
      deckId: session.deckId,
      deckRevision: session.deckRevision,
      label: session.label,
      meetingDecision: session.meetingDecision,
      decisionOwnerRole: session.decisionOwnerRole,
      authorizedScope: session.authorizedScope,
      unauthorizedScope: session.unauthorizedScope,
      assumptions: session.assumptions,
      actions: session.actions,
      dissent: session.dissent,
      nextForum: session.nextForum,
      holdReason: session.holdReason,
      createdAt: session.createdAt,
      updatedAt: session.updatedAt,
      expiresAt: session.expiresAt,
      generatedAt: cleanDate(options.generatedAt),
      decisionState,
      reviewable: decisionState === "reviewable",
      counts,
      holds,
      gaps,
      sessionGaps,
      phases,
      questions,
      safeguards: {
        storage: "local-browser-only",
        evidenceAuthority: "Meeting input does not upgrade evidence.",
        productionAuthorization: "Production remains unauthorized until the defined evidence and approval gates close.",
        privacy: "Controlled role values and automatic removal of obvious restricted patterns reduce risk but do not make browser storage private.",
      },
    };
  }

  function buildReport(contract, normalized, options = {}) {
    return summarizeAssessment(contract, normalized, options);
  }

  function exportSafeValue(value, key = "") {
    if (typeof value === "string") {
      if (key === "deckRevision") return cleanRevision(value);
      return ["ownerRole", "decisionOwnerRole"].includes(key)
        ? cleanPublicRole(value)
        : publicSafeText(value, limits.record);
    }
    if (Array.isArray(value)) return value.map((nested) => exportSafeValue(nested));
    if (value && typeof value === "object") {
      return Object.fromEntries(Object.entries(value).map(([nestedKey, nested]) => [nestedKey, exportSafeValue(nested, nestedKey)]));
    }
    return value;
  }

  function exportAssessmentJson(summary) {
    const report = exportSafeValue(summary && typeof summary === "object" ? summary : {});
    return `${JSON.stringify(report, null, 2)
      .replace(/</g, "\\u003c")
      .replace(/>/g, "\\u003e")
      .replace(/&/g, "\\u0026")}\n`;
  }

  function markdownText(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\\/g, "\\\\")
      .replace(/([`*_[\]{}#+.!|])/g, "\\$1")
      .replace(/\r?\n/g, "  \n");
  }

  function exportAssessmentMarkdown(summary) {
    const report = exportSafeValue(summary && typeof summary === "object" ? summary : {});
    const lines = [
      "# Guided evaluation meeting summary",
      "",
      `- Schema version (schemaVersion): ${Number(report.schemaVersion || SCHEMA_VERSION)}`,
      `- Deck ID (deckId): ${markdownText(report.deckId || "Not recorded")}`,
      `- Meeting: ${markdownText(report.label || "Not labelled")}`,
      `- Deck revision (deckRevision): ${markdownText(report.deckRevision || "Not recorded")}`,
      `- Meeting decision: ${markdownText(report.meetingDecision || "Not captured")}`,
      `- Decision owner role: ${markdownText(report.decisionOwnerRole || "Not assigned")}`,
      `- Decision state: ${markdownText(String(report.decisionState || "amend").toUpperCase())}`,
      `- Created (createdAt): ${markdownText(report.createdAt || "Not recorded")}`,
      `- Updated (updatedAt): ${markdownText(report.updatedAt || "Not recorded")}`,
      `- Expires (expiresAt): ${markdownText(report.expiresAt || "Not recorded")}`,
      `- Generated (generatedAt): ${markdownText(report.generatedAt || "Not recorded")}`,
      `- Responses: ${Number(report.counts?.answered || 0)} of ${Number(report.counts?.total || 0)}`,
      "",
      "## Decision record",
      "",
      `- Authorized scope: ${markdownText(report.authorizedScope || "Not captured")}`,
      `- Unauthorized scope: ${markdownText(report.unauthorizedScope || "Not captured")}`,
      `- Assumptions: ${markdownText(report.assumptions || "None recorded")}`,
      `- Actions: ${markdownText(report.actions || "None recorded")}`,
      `- Dissent: ${markdownText(report.dissent || "None recorded")}`,
      `- Next forum: ${markdownText(report.nextForum || "Not captured")}`,
      `- Hold reason: ${markdownText(report.holdReason || "Not applicable")}`,
      `- Session gaps: ${report.sessionGaps?.length ? report.sessionGaps.map(markdownText).join(", ") : "None recorded"}`,
      "",
      "> Local meeting input does not upgrade evidence. Production remains unauthorized until the defined evidence and approval gates close.",
      "",
    ];
    (Array.isArray(report.phases) ? report.phases : []).forEach((phase) => {
      lines.push(
        `## ${markdownText(phase.phaseId || "Unassigned phase")}`,
        "",
        `- Phase ID (phaseId): ${markdownText(phase.phaseId || "Not recorded")}`,
        `- Question IDs (questionIds): ${phase.questionIds?.length ? phase.questionIds.map(markdownText).join(", ") : "None recorded"}`,
        "",
      );
      const phaseQuestions = (Array.isArray(report.questions) ? report.questions : [])
        .filter((question) => (phase.questionIds || []).includes(question.id));
      phaseQuestions.forEach((question) => {
        lines.push(
          `### ${markdownText(question.id)} — ${markdownText(question.status || "unanswered")}`,
          "",
          markdownText(question.prompt || "Question"),
          "",
          `- Question ID (questionId): ${markdownText(question.id || "Not recorded")}`,
          `- Phase ID (phaseId): ${markdownText(question.phaseId || phase.phaseId || "Not recorded")}`,
          `- Slide IDs (slideIds): ${question.slideIds?.length ? question.slideIds.map(markdownText).join(", ") : "None recorded"}`,
          `- Target IDs (targetIds): ${question.targetIds?.length ? question.targetIds.map(markdownText).join(", ") : "None recorded"}`,
          `- Choice value (choice): ${markdownText(question.response?.choice || "Unanswered")}`,
          `- Choice label: ${markdownText(question.choiceLabel || "Unanswered")}`,
          `- Hold rule: ${markdownText(question.holdRule || "Not recorded")}`,
          `- Hold-rule disposition: ${markdownText(question.response?.holdRuleStatus || "open")}`,
          `- Evidence: ${markdownText(question.response?.evidenceLevel || "E0")} (minimum ${markdownText(question.minimumEvidence || "E0")})`,
          `- Evidence reference: ${markdownText(question.response?.evidenceReference || "Not captured")}`,
          `- Criterion ID: ${markdownText(question.response?.criterionId || "Not captured")}`,
          `- Option ID: ${markdownText(question.response?.optionId || "Not captured")}`,
          `- Evidence request: ${markdownText(question.response?.evidenceRequest || "Not captured")}`,
          `- Restricted-reference ID: ${markdownText(question.response?.restrictedReferenceId || "Not captured")}`,
          `- Rationale / notes: ${markdownText(question.response?.rationale || "Not captured")}`,
          `- Owner role: ${markdownText(question.response?.ownerRole || "Not assigned")}`,
          `- Due gate: ${markdownText(question.response?.dueGate || "Not assigned")}`,
          `- Dissent: ${markdownText(question.response?.dissent || "None recorded")}`,
          `- Next forum: ${markdownText(question.response?.nextForum || "Not assigned")}`,
          `- Open gaps: ${question.gaps?.length ? question.gaps.map(markdownText).join(", ") : "None recorded"}`,
          "",
        );
      });
    });
    return `${lines.join("\n").trim()}\n`;
  }

  function defaultStorageKey(deckId = "kong-platform-journey-guided") {
    let path = "/";
    try {
      path = window.location.pathname || "/";
    } catch (error) {
      path = "/";
    }
    return `api-study:${path}:${cleanId(deckId)}:assessment:v${SCHEMA_VERSION}`;
  }

  function createStore(options = {}) {
    const key = boundedText(options.key || defaultStorageKey(options.deckId), 500);
    let persistentStorage = options.storage;
    let persistence = "localStorage";
    let issue = "";
    let writeProtected = false;
    if (!persistentStorage) {
      try {
        persistentStorage = window.localStorage;
      } catch (error) {
        persistentStorage = null;
      }
    }
    if (!persistentStorage) {
      persistence = "memory";
      issue = "Browser storage is unavailable. Changes last only for this page session.";
    }

    function fail(message) {
      persistence = "memory";
      issue = message;
    }

    function load() {
      let serialized = null;
      if (persistentStorage && persistence === "localStorage") {
        try {
          serialized = persistentStorage.getItem(key);
        } catch (error) {
          fail("Browser storage could not be read. Changes now last only for this page session.");
        }
      }
      if (serialized == null) serialized = memoryStores.get(key) || null;
      if (!serialized) return null;
      try {
        const value = JSON.parse(serialized);
        if (!value || value.schemaVersion !== SCHEMA_VERSION) {
          issue = "Saved assessment data uses an unsupported version and was left untouched.";
          writeProtected = true;
          return null;
        }
        if (value.expiresAt && !Number.isNaN(Date.parse(value.expiresAt)) && Date.parse(value.expiresAt) <= Date.now()) {
          issue = "Saved assessment data has expired and was left untouched. Clear it before saving a new persistent assessment.";
          writeProtected = true;
          return null;
        }
        return value;
      } catch (error) {
        issue = "Saved assessment data could not be read and was left untouched.";
        writeProtected = true;
        return null;
      }
    }

    function save(value) {
      const serialized = JSON.stringify(exportSafeValue(value));
      memoryStores.set(key, serialized);
      if (writeProtected) {
        persistence = "memory";
      } else if (persistentStorage && persistence === "localStorage") {
        try {
          persistentStorage.setItem(key, serialized);
        } catch (error) {
          fail("Browser storage could not save this assessment. Changes now last only for this page session.");
        }
      }
      return { ...status() };
    }

    function clear() {
      memoryStores.delete(key);
      if (persistentStorage) {
        try {
          persistentStorage.removeItem(key);
        } catch (error) {
          fail("Browser storage could not clear the saved assessment.");
          return false;
        }
      }
      writeProtected = false;
      persistence = persistentStorage ? "localStorage" : "memory";
      issue = persistence === "memory"
        ? "Browser storage is unavailable. Changes last only for this page session."
        : "";
      return true;
    }

    function status() {
      return { key, persistence, issue, writeProtected };
    }

    return Object.freeze({ key, load, save, clear, status });
  }

  window.ApiStudyAssessment = Object.freeze({
    SCHEMA_VERSION,
    EVIDENCE_LEVELS,
    PUBLIC_ROLES,
    privacyFinding,
    publicSafeText,
    normalizeAssessment,
    summarizeAssessment,
    exportAssessmentJson,
    exportAssessmentMarkdown,
    createStore,
    createLocalStore: createStore,
    normalize: normalizeAssessment,
    summarize: summarizeAssessment,
    buildReport,
    toJson: exportAssessmentJson,
    toMarkdown: exportAssessmentMarkdown,
  });
})();
