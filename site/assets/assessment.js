(() => {
  "use strict";

  const SCHEMA_VERSION = 1;
  const EVIDENCE_LEVELS = Object.freeze(["E0", "E1", "E2", "E3", "E4"]);
  const OUTCOMES = new Set(["pass", "amend", "hold", "unknown", "not-applicable", "inform"]);
  const memoryStores = new Map();
  const limits = Object.freeze({
    id: 120,
    label: 160,
    decision: 2000,
    reference: 500,
    rationale: 2000,
    role: 160,
    gate: 160,
  });

  function boundedText(value, limit) {
    return String(value ?? "")
      .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "")
      .slice(0, limit);
  }

  function cleanId(value) {
    return boundedText(value, limits.id).trim();
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
      evidenceLevel: "E0",
      evidenceReference: "",
      rationale: "",
      ownerRole: "",
      dueGate: "",
    };
  }

  function normalizeResponse(question, rawResponse, choiceSets) {
    const source = rawResponse && typeof rawResponse === "object" ? rawResponse : {};
    const validChoices = new Set(choicesFor(question, choiceSets).map((choice) => cleanId(choice.value)));
    const choice = cleanId(source.choice);
    const evidenceLevel = cleanId(source.evidenceLevel).toUpperCase();
    return {
      choice: validChoices.has(choice) ? choice : "",
      evidenceLevel: EVIDENCE_LEVELS.includes(evidenceLevel) ? evidenceLevel : "E0",
      evidenceReference: boundedText(source.evidenceReference, limits.reference).trim(),
      rationale: boundedText(source.rationale ?? source.notes, limits.rationale).trim(),
      ownerRole: boundedText(source.ownerRole, limits.role).trim(),
      dueGate: boundedText(source.dueGate, limits.gate).trim(),
    };
  }

  function normalizeAssessment(contract, raw = {}) {
    const source = raw && typeof raw === "object" ? raw : {};
    const choiceSets = choiceSetsFor(contract);
    const responses = {};
    questionsFor(contract).forEach((question) => {
      const questionId = cleanId(question.id);
      responses[questionId] = normalizeResponse(question, source.responses?.[questionId], choiceSets);
    });
    return {
      schemaVersion: SCHEMA_VERSION,
      deckId: cleanId(source.deckId || contract?.deckId || "kong-platform-journey-guided"),
      label: boundedText(source.label, limits.label).trim(),
      meetingDecision: boundedText(source.meetingDecision, limits.decision).trim(),
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

  function summarizeQuestion(question, response, choiceSets) {
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
    const status = selected ? outcome : "unanswered";
    return {
      id: cleanId(question.id),
      phaseId: cleanId(question.phaseId),
      slideIds: Array.isArray(question.slideIds) ? question.slideIds.map(cleanId).filter(Boolean) : [],
      targetIds: Array.isArray(question.targetIds) ? question.targetIds.map(cleanId).filter(Boolean) : [],
      prompt: boundedText(question.prompt, 1200).trim(),
      decisionUse: boundedText(question.decisionUse, 800).trim(),
      evidenceBoundary: boundedText(question.evidenceBoundary, 800).trim(),
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
    const questions = questionsFor(contract).map((question) => (
      summarizeQuestion(question, session.responses[cleanId(question.id)] || emptyResponse(), choiceSets)
    ));
    const mandatoryQuestions = questions.filter((question) => question.mandatory);
    const mandatoryHold = mandatoryQuestions.some((question) => (
      question.status === "unanswered" || question.outcome === "hold" || question.outcome === "unknown" || question.gaps.length > 0
    ));
    const mandatoryResolved = mandatoryQuestions.length > 0 && mandatoryQuestions.every((question) => (
      ["pass", "inform", "not-applicable"].includes(question.outcome) && question.gaps.length === 0
    ));
    const requiresAmendment = questions.some((question) => question.outcome === "amend" || question.gaps.length > 0);
    const decisionState = mandatoryHold ? "hold" : mandatoryResolved && !requiresAmendment ? "reviewable" : "amend";
    const evidenceSupported = questions.filter((question) => (
      question.status !== "unanswered"
      && question.outcome !== "not-applicable"
      && evidenceRank(question.response.evidenceLevel) >= evidenceRank(question.minimumEvidence)
    ));
    const holds = mandatoryQuestions
      .filter((question) => question.status === "unanswered" || ["hold", "unknown"].includes(question.outcome) || question.gaps.length > 0)
      .map((question) => question.id);
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
      gaps: questions.filter((question) => question.gaps.length > 0).length,
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
      label: session.label,
      meetingDecision: session.meetingDecision,
      createdAt: session.createdAt,
      updatedAt: session.updatedAt,
      expiresAt: session.expiresAt,
      generatedAt: cleanDate(options.generatedAt),
      decisionState,
      reviewable: decisionState === "reviewable",
      counts,
      holds,
      gaps,
      phases,
      questions,
      safeguards: {
        storage: "local-browser-only",
        evidenceAuthority: "Meeting input does not upgrade evidence.",
        productionAuthorization: "Production remains unauthorized until the defined evidence and approval gates close.",
      },
    };
  }

  function buildReport(contract, normalized, options = {}) {
    return summarizeAssessment(contract, normalized, options);
  }

  function exportAssessmentJson(summary) {
    return `${JSON.stringify(summary && typeof summary === "object" ? summary : {}, null, 2)
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
    const report = summary && typeof summary === "object" ? summary : {};
    const lines = [
      "# Guided evaluation meeting summary",
      "",
      `- Meeting: ${markdownText(report.label || "Not labelled")}`,
      `- Meeting decision: ${markdownText(report.meetingDecision || "Not captured")}`,
      `- Decision state: ${markdownText(String(report.decisionState || "amend").toUpperCase())}`,
      `- Generated: ${markdownText(report.generatedAt || "Not recorded")}`,
      `- Responses: ${Number(report.counts?.answered || 0)} of ${Number(report.counts?.total || 0)}`,
      "",
      "> Local meeting input does not upgrade evidence. Production remains unauthorized until the defined evidence and approval gates close.",
      "",
    ];
    (Array.isArray(report.phases) ? report.phases : []).forEach((phase) => {
      lines.push(`## ${markdownText(phase.phaseId || "Unassigned phase")}`, "");
      const phaseQuestions = (Array.isArray(report.questions) ? report.questions : [])
        .filter((question) => (phase.questionIds || []).includes(question.id));
      phaseQuestions.forEach((question) => {
        lines.push(
          `### ${markdownText(question.id)} — ${markdownText(question.status || "unanswered")}`,
          "",
          markdownText(question.prompt || "Question"),
          "",
          `- Choice: ${markdownText(question.choiceLabel || question.response?.choice || "Unanswered")}`,
          `- Evidence: ${markdownText(question.response?.evidenceLevel || "E0")} (minimum ${markdownText(question.minimumEvidence || "E0")})`,
          `- Evidence reference: ${markdownText(question.response?.evidenceReference || "Not captured")}`,
          `- Rationale / notes: ${markdownText(question.response?.rationale || "Not captured")}`,
          `- Owner role: ${markdownText(question.response?.ownerRole || "Not assigned")}`,
          `- Due gate: ${markdownText(question.response?.dueGate || "Not assigned")}`,
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
      const serialized = JSON.stringify(value);
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
