(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const siteDemo = location.hostname.endsWith("chatgpt.site") || location.protocol === "file:";

  const tones = {
    acid: "#caff3f", coral: "#ff7a5c", violet: "#9c7cff",
    cyan: "#47d7ff", amber: "#ffbd4a", pink: "#ff69c8"
  };

  const projects = [
    {
      title: "BillFlow AI", category: "AI FINANCE · FULL STACK", status: "Working vertical slice",
      tagline: "An explainable finance operating system that plans bills, protects a safety reserve and keeps payment authorization human-controlled.",
      problem: "Traditional trackers describe past spending but do not safely coordinate upcoming bills and competing cash-flow deadlines.",
      proof: "FastAPI + React vertical slice, authentication, PostgreSQL, deterministic provider connectors, audit events and automated tests.",
      stack: ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker"],
      link: "https://github.com/Yashovardhan47/AI_finance_manage_system_AI", domain: "safepay://decision-engine", metricLabel: "Liquidity confidence", metric: "94%", visual: "finance"
    },
    {
      title: "OmniCalc", category: "VERIFIED AI · RESEARCH", status: "Production-oriented prototype",
      tagline: "A natural-language calculation workspace that compiles requests into verified, deterministic calculation graphs.",
      problem: "LLM-generated calculations can be persuasive but unverifiable, unsafe and difficult to reproduce.",
      proof: "Typed intermediate representation, static verification, secure sign-in, PostgreSQL history, evidence receipts and a benchmark harness.",
      stack: ["Python", "FastAPI", "React", "PostgreSQL", "JWT", "Docker"],
      link: "https://github.com/Yashovardhan47/AI_calculator", domain: "calcgraph://verified-run", metricLabel: "Checks passed", metric: "12/12", visual: "verified"
    },
    {
      title: "Quick Hire", category: "RECRUITMENT · FULL STACK", status: "Full-stack application",
      tagline: "A role-based recruitment platform connecting job seekers and recruiters through focused workflows.",
      problem: "Disconnected hiring workflows make it harder to track applications, manage opportunities and surface relevant candidates.",
      proof: "Database-backed application with authentication, separate role dashboards, listings, applications and personalized recommendations.",
      stack: ["PHP", "MySQL", "JavaScript", "HTML", "CSS"],
      link: "https://github.com/Yashovardhan47/Quick-Hire", domain: "quickhire://role-workflow", metricLabel: "Workflow states", metric: "08", visual: "roles"
    },
    {
      title: "BloomSense", category: "COMPUTER VISION · AI", status: "AI application",
      tagline: "A multimodal flower identification experience using detection, botanical context, translation and voice output.",
      problem: "Species identification tools often return only a label and remain difficult to use across input modes or languages.",
      proof: "FastAPI backend, responsive interface, multi-mode detection, YOLOv8, 18-language translation and accessible text-to-speech.",
      stack: ["Python", "FastAPI", "YOLOv8", "OpenCV", "JavaScript", "REST APIs"],
      link: "https://github.com/Yashovardhan47/BloomSense_AI", domain: "bloomsense://vision-pipeline", metricLabel: "Input modes", metric: "03", visual: "vision"
    },
    {
      title: "Mental Health", category: "MACHINE LEARNING · ANALYTICS", status: "Data science project",
      tagline: "A model-comparison and exploratory-analysis project for understanding patterns in mental-health data.",
      problem: "Health datasets require careful preparation, interpretable exploration and responsible comparison before conclusions.",
      proof: "Reproducible cleaning, visualization and model-comparison workflow across SVM, Random Forest and XGBoost.",
      stack: ["Python", "pandas", "XGBoost", "SVM", "Seaborn"],
      link: "https://github.com/Yashovardhan47/Mental-Disorder-Data-Analysis", domain: "analysis://model-compare", metricLabel: "Models compared", metric: "03", visual: "analysis"
    },
    {
      title: "Flower Vision", category: "COMPUTER VISION · ML", status: "Computer vision project",
      tagline: "A real-time flower detection and classification workflow built around a YOLOv8 vision pipeline.",
      problem: "Image classification alone does not localize multiple visual objects or provide an interactive inference experience.",
      proof: "Complete pipeline spanning dataset configuration, YOLOv8 inference, annotated results, Flask integration and browser delivery.",
      stack: ["Python", "YOLOv8", "OpenCV", "Flask"],
      link: "https://github.com/Yashovardhan47/Flower-Detection-and-classification-System", domain: "vision://realtime-detect", metricLabel: "Pipeline stages", metric: "04", visual: "detect"
    }
  ];

  const modes = {
    language: { code: "MODE / 01", title: "Languages", score: 92, description: "The expressive layer: Python for systems and analysis, SQL for evidence, JavaScript for interaction, and Java for foundations.", tools: ["Python", "SQL", "JavaScript", "Java"], values: [80, 65, 84, 88, 72], log: "Syntax → logic → tested output. Language layer stable." },
    ai: { code: "MODE / 02", title: "AI + Data", score: 89, description: "The intelligence layer: explore responsibly, compare models, explain outputs and build computer-vision workflows that users can inspect.", tools: ["Machine Learning", "pandas", "NumPy", "XGBoost", "YOLOv8", "Tableau", "Power BI"], values: [96, 66, 58, 92, 74], log: "Dataset profiled → model compared → evidence visualized." },
    stack: { code: "MODE / 03", title: "Full Stack", score: 87, description: "The product layer: APIs, interfaces, auth and state stitched into coherent workflows instead of isolated technical demos.", tools: ["FastAPI", "Flask", "React", "REST APIs", "HTML", "CSS", "PHP"], values: [64, 95, 91, 68, 83], log: "Client ↔ API ↔ persistence. End-to-end path verified." },
    delivery: { code: "MODE / 04", title: "Data + Delivery", score: 84, description: "The reliability layer: durable stores, containers, version control and automated checks that make the result repeatable.", tools: ["PostgreSQL", "MySQL", "SQLite", "Docker", "Git", "GitHub Actions"], values: [58, 80, 72, 86, 94], log: "Schema checked → container built → CI green. Ready to ship." }
  };

  const state = { scene: 0, principle: 0, project: 0, commandIndex: 0, motion: !prefersReduced.matches };
  const scenes = $$(".scene");

  function boot() {
    const root = $("#boot");
    if (!root) return;
    if (prefersReduced.matches) {
      root.classList.add("is-done");
      startCounters();
      return;
    }
    const value = $("#boot-value");
    const track = $(".boot__track span");
    const started = performance.now();
    const duration = 1450;
    const tick = now => {
      const progress = Math.min(1, (now - started) / duration);
      const eased = 1 - Math.pow(1 - progress, 3);
      const amount = Math.round(eased * 100);
      value.textContent = amount;
      track.style.width = `${amount}%`;
      if (progress < 1) requestAnimationFrame(tick);
      else setTimeout(() => { root.classList.add("is-done"); startCounters(); }, 180);
    };
    requestAnimationFrame(tick);
  }

  function goTo(id) {
    const target = document.getElementById(id);
    if (!target) return;
    closeMenu(); closeCommand();
    target.scrollIntoView({ behavior: state.motion ? "smooth" : "auto", block: "start" });
  }

  function updateScene(index) {
    if (index < 0 || index >= scenes.length) return;
    state.scene = index;
    const scene = scenes[index];
    const tone = scene.dataset.tone;
    document.documentElement.style.setProperty("--accent", tones[tone]);
    scenes.forEach((item, i) => item.classList.toggle("is-active", i === index));
    $$(".scene-rail [data-go]").forEach(button => button.classList.toggle("is-active", button.dataset.go === scene.id));
    $("#scene-current").textContent = String(index + 1).padStart(2, "0");
    $("#scene-meter").style.height = `${((index + 1) / scenes.length) * 100}%`;
    $("#topbar").classList.toggle("is-scrolled", index > 0 || scrollY > 24);
  }

  function setupSceneObserver() {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= .36) updateScene(scenes.indexOf(entry.target));
      });
    }, { threshold: [.36, .55, .75] });
    scenes.forEach(scene => observer.observe(scene));
    addEventListener("scroll", () => $("#topbar").classList.toggle("is-scrolled", scrollY > 24), { passive: true });
  }

  function setupNavigation() {
    $$('[data-go]').forEach(button => button.addEventListener("click", event => {
      if (button.tagName === "A") event.preventDefault();
      goTo(button.dataset.go);
    }));
    addEventListener("keydown", event => {
      const tag = document.activeElement?.tagName;
      const blocked = ["INPUT", "TEXTAREA", "SELECT"].includes(tag) || $("#command").classList.contains("is-open") || $("#assistant").classList.contains("is-open");
      if (blocked) return;
      if (["PageDown", "ArrowDown"].includes(event.key)) { event.preventDefault(); goTo(scenes[Math.min(state.scene + 1, scenes.length - 1)].id); }
      if (["PageUp", "ArrowUp"].includes(event.key)) { event.preventDefault(); goTo(scenes[Math.max(state.scene - 1, 0)].id); }
    });
  }

  function setupMenu() {
    const trigger = $("#menu-trigger");
    trigger.addEventListener("click", () => trigger.getAttribute("aria-expanded") === "true" ? closeMenu() : openMenu());
  }
  function openMenu() { const menu = $("#menu-panel"); menu.classList.add("is-open"); menu.setAttribute("aria-hidden", "false"); $("#menu-trigger").setAttribute("aria-expanded", "true"); document.body.classList.add("is-locked"); }
  function closeMenu() { const menu = $("#menu-panel"); menu.classList.remove("is-open"); menu.setAttribute("aria-hidden", "true"); $("#menu-trigger").setAttribute("aria-expanded", "false"); if (!$("#command").classList.contains("is-open") && !$("#assistant").classList.contains("is-open")) document.body.classList.remove("is-locked"); }

  function setupMotion() {
    const button = $("#motion-toggle");
    const apply = value => {
      state.motion = value;
      document.documentElement.dataset.motion = value ? "full" : "reduced";
      button.setAttribute("aria-pressed", String(!value));
      button.setAttribute("aria-label", value ? "Reduce motion" : "Enable motion");
      $(".button-label", button).textContent = value ? "Motion" : "Still";
    };
    apply(!prefersReduced.matches);
    button.addEventListener("click", () => { apply(!state.motion); toast(state.motion ? "Full motion enabled" : "Reduced motion enabled"); });
  }

  function setupPointerEffects() {
    addEventListener("pointermove", event => {
      document.documentElement.style.setProperty("--pointer-x", `${event.clientX}px`);
      document.documentElement.style.setProperty("--pointer-y", `${event.clientY}px`);
    }, { passive: true });
    $$(".magnetic").forEach(item => {
      item.addEventListener("pointermove", event => {
        if (!state.motion || innerWidth < 900) return;
        const rect = item.getBoundingClientRect();
        item.style.transform = `translate(${(event.clientX - rect.left - rect.width / 2) * .16}px,${(event.clientY - rect.top - rect.height / 2) * .16}px)`;
      });
      item.addEventListener("pointerleave", () => item.style.transform = "");
    });
    $$(".tilt-card").forEach(card => {
      card.addEventListener("pointermove", event => {
        if (!state.motion || innerWidth < 900) return;
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        card.style.transform = `rotateY(${x * 10}deg) rotateX(${y * -9}deg) translateZ(8px)`;
      });
      card.addEventListener("pointerleave", () => card.style.transform = "");
    });
  }

  function startCounters() {
    $$('[data-count]').forEach(element => {
      const end = Number(element.dataset.count);
      const decimals = Number(element.dataset.decimals || 0);
      if (!state.motion) { element.textContent = end.toFixed(decimals); return; }
      const start = performance.now();
      const duration = 1150;
      const tick = now => {
        const progress = Math.min(1, (now - start) / duration);
        element.textContent = (end * (1 - Math.pow(1 - progress, 3))).toFixed(decimals);
        if (progress < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }

  function setupRoleCycle() {
    const roles = ["Data scientist", "Python developer", "AI systems builder", "Full-stack engineer"];
    let index = 0;
    setInterval(() => {
      if (!state.motion || state.scene !== 0) return;
      const element = $("#role-cycle");
      element.animate([{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: "translateY(-6px)" }], { duration: 220, fill: "forwards" }).finished.then(() => {
        index = (index + 1) % roles.length; element.textContent = roles[index];
        element.animate([{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "translateY(0)" }], { duration: 260, fill: "forwards" });
      });
    }, 2400);
  }

  function setupPrinciples() {
    const cards = $$(".principle-card");
    const render = index => {
      state.principle = (index + cards.length) % cards.length;
      cards.forEach((card, i) => {
        card.classList.toggle("is-active", i === state.principle);
        card.classList.toggle("is-before", i < state.principle);
      });
      $("#principle-progress").style.width = `${((state.principle + 1) / cards.length) * 100}%`;
    };
    $("#principle-prev").addEventListener("click", () => render(state.principle - 1));
    $("#principle-next").addEventListener("click", () => render(state.principle + 1));
    cards.forEach((card, index) => card.addEventListener("click", () => render(index)));
  }

  function radarPoints(values) {
    const center = 210, maxRadius = 175;
    return values.map((value, index) => {
      const angle = -Math.PI / 2 + index * (Math.PI * 2 / 5);
      const radius = maxRadius * value / 100;
      return `${(center + Math.cos(angle) * radius).toFixed(1)},${(center + Math.sin(angle) * radius).toFixed(1)}`;
    }).join(" ");
  }

  function renderMode(key) {
    const mode = modes[key];
    $("#mode-code").textContent = mode.code; $("#mode-title").textContent = mode.title; $("#mode-description").textContent = mode.description; $("#mode-score").textContent = mode.score;
    const points = radarPoints(mode.values);
    $("#radar-shape").setAttribute("points", points);
    $("#radar-dots").innerHTML = points.split(" ").map(point => { const [cx, cy] = point.split(","); return `<circle cx="${cx}" cy="${cy}" r="5"></circle>`; }).join("");
    $("#tool-cloud").innerHTML = mode.tools.map((tool, index) => `<span style="animation-delay:${index * 45}ms">${tool}</span>`).join("");
    $("#signal-log").innerHTML = "<span>Mode loaded. Run the signal test.</span>";
    $$(".mode-tabs button").forEach(button => { const active = button.dataset.mode === key; button.classList.toggle("is-active", active); button.setAttribute("aria-selected", String(active)); });
  }

  function setupCapabilities() {
    $$(".mode-tabs button").forEach(button => button.addEventListener("click", () => renderMode(button.dataset.mode)));
    $("#run-signal").addEventListener("click", async () => {
      const key = $(".mode-tabs button.is-active").dataset.mode;
      const button = $("#run-signal"); const log = $("#signal-log");
      button.classList.add("is-running");
      const steps = ["Initializing capability matrix...", "Testing cross-layer connections...", modes[key].log];
      for (const step of steps) { log.innerHTML = `<span>${step}</span>`; await wait(state.motion ? 520 : 40); }
      button.classList.remove("is-running"); toast(`${modes[key].title} signal verified`);
    });
    renderMode("language");
  }

  function renderProject(index) {
    state.project = (index + projects.length) % projects.length;
    const project = projects[state.project]; const stage = $("#project-stage");
    stage.classList.remove("is-switching"); void stage.offsetWidth; stage.classList.add("is-switching");
    $("#project-number").textContent = `CASE ${String(state.project + 1).padStart(2, "0")} / 06`;
    $("#project-category").textContent = project.category; $("#project-title").textContent = project.title; $("#project-tagline").textContent = project.tagline;
    $("#project-problem").textContent = project.problem; $("#project-proof").textContent = project.proof; $("#project-status").textContent = project.status;
    $("#project-domain").textContent = project.domain; $("#project-metric-label").textContent = project.metricLabel; $("#project-metric").textContent = project.metric;
    $("#project-canvas").dataset.visual = project.visual; $("#project-link").href = project.link;
    $("#project-stack").innerHTML = project.stack.map((tool, i) => `<span style="animation-delay:${i * 35}ms">${tool}</span>`).join("");
    $$(".project-list button").forEach((button, i) => { const active = i === state.project; button.classList.toggle("is-active", active); button.setAttribute("aria-selected", String(active)); });
  }

  function setupProjects() {
    $$(".project-list button").forEach((button, index) => button.addEventListener("click", () => renderProject(index)));
    $("#project-prev").addEventListener("click", () => renderProject(state.project - 1));
    $("#project-next").addEventListener("click", () => renderProject(state.project + 1));
    renderProject(0);
  }

  function setupTimeline() {
    const items = $$(".timeline-item");
    items.forEach((item, index) => item.addEventListener("click", () => {
      items.forEach(entry => entry.classList.toggle("is-active", entry === item));
      $("#timeline-year").textContent = item.dataset.year;
      $("#timeline-detail").textContent = item.dataset.detail;
      const progress = innerWidth <= 820 ? "height" : "width";
      $("#timeline-progress").style[progress] = `${(index / (items.length - 1)) * 100}%`;
      $("#certificate-link").style.visibility = item.dataset.year === "2025" ? "visible" : "hidden";
    }));
    $("#certificate-link").style.visibility = "hidden";
  }

  function setupCommand() {
    $$('[data-open-command]').forEach(button => button.addEventListener("click", openCommand));
    $$('[data-close-command]').forEach(button => button.addEventListener("click", closeCommand));
    const input = $("#command-input");
    input.addEventListener("input", () => {
      const query = input.value.trim().toLowerCase();
      commandItems().forEach(item => item.hidden = !item.dataset.search.includes(query));
      state.commandIndex = 0; selectCommand();
    });
    $$("[data-command]").forEach(button => button.addEventListener("click", () => runCommand(button.dataset.command)));
    addEventListener("keydown", event => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); $("#command").classList.contains("is-open") ? closeCommand() : openCommand(); return; }
      if (event.key === "Escape") { closeCommand(); closeAssistant(); closeMenu(); }
      if (!$("#command").classList.contains("is-open")) return;
      const items = commandItems();
      if (event.key === "ArrowDown") { event.preventDefault(); state.commandIndex = (state.commandIndex + 1) % items.length; selectCommand(); }
      if (event.key === "ArrowUp") { event.preventDefault(); state.commandIndex = (state.commandIndex - 1 + items.length) % items.length; selectCommand(); }
      if (event.key === "Enter") { event.preventDefault(); items[state.commandIndex]?.click(); }
    });
  }
  function commandItems() { return $$("#command-results > *").filter(item => !item.hidden); }
  function selectCommand() { const items = commandItems(); items.forEach((item, index) => item.classList.toggle("is-selected", index === state.commandIndex)); }
  function openCommand() { closeMenu(); const panel = $("#command"); panel.classList.add("is-open"); panel.setAttribute("aria-hidden", "false"); document.body.classList.add("is-locked"); $("#command-input").value = ""; $$("#command-results > *").forEach(item => item.hidden = false); state.commandIndex = 0; selectCommand(); setTimeout(() => $("#command-input").focus(), 150); }
  function closeCommand() { const panel = $("#command"); panel.classList.remove("is-open"); panel.setAttribute("aria-hidden", "true"); if (!$("#assistant").classList.contains("is-open") && !$("#menu-panel").classList.contains("is-open")) document.body.classList.remove("is-locked"); }
  function runCommand(command) { if (command === "assistant") { closeCommand(); openAssistant(); } else goTo(command); }

  function localAnswer(question) {
    const q = question.toLowerCase();
    if (q.includes("backend") || q.includes("fastapi") || q.includes("api")) return "BillFlow AI and OmniCalc are the strongest backend examples. Both use FastAPI, authentication, PostgreSQL-ready persistence, Docker workflows and automated tests; OmniCalc adds typed verification and reproducibility receipts.";
    if (q.includes("ai") || q.includes("machine") || q.includes("model")) return "The AI work spans explainable finance recommendations, verified calculation graphs, YOLOv8 computer vision and responsible model comparison. The recurring theme is making outputs inspectable instead of treating a prediction as the end of the product.";
    if (q.includes("role") || q.includes("fit") || q.includes("job")) return "Best-fit roles include Data Scientist, Data Analyst, Python Developer and junior Full-Stack Developer—especially teams that value someone who can connect analysis, APIs and user experience.";
    if (q.includes("education") || q.includes("cgpa") || q.includes("university")) return "Yashovardhan is pursuing a B.Tech in Computer Science — Data Science at Mohan Babu University, graduating in 2027, with an 8.5/10 CGPA.";
    if (q.includes("project") || q.includes("work")) return "There are six case studies here. Start with BillFlow AI for product depth, OmniCalc for verified AI, BloomSense for multimodal computer vision, or Quick Hire for classic role-based full-stack workflow design.";
    return "Yashovardhan combines data science with Python full-stack delivery. Ask me about a specific project, the technical stack, education, AI experience or suitable roles and I’ll point you to the strongest evidence.";
  }

  function setupAssistant() {
    $$('[data-open-assistant]').forEach(button => button.addEventListener("click", openAssistant));
    $$('[data-close-assistant]').forEach(button => button.addEventListener("click", closeAssistant));
    $$("#assistant-prompts button").forEach(button => button.addEventListener("click", () => { $("#assistant-input").value = button.textContent; $("#assistant-form").requestSubmit(); }));
    $("#assistant-form").addEventListener("submit", async event => {
      event.preventDefault();
      const input = $("#assistant-input"); const question = input.value.trim(); if (!question) return;
      addMessage(question, "user"); input.value = ""; input.disabled = true;
      const typing = addMessage("Reading the evidence…", "bot");
      try {
        let answer;
        if (siteDemo) { await wait(620); answer = localAnswer(question); }
        else {
          const response = await fetch("/api/assistant", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) });
          const data = await response.json(); if (!response.ok) throw new Error(data.error || "Assistant unavailable"); answer = data.answer;
        }
        typing.textContent = answer;
      } catch (error) { typing.textContent = `${localAnswer(question)} (The live assistant endpoint is temporarily unavailable.)`; }
      finally { input.disabled = false; input.focus(); }
    });
  }
  function addMessage(text, type) { const message = document.createElement("div"); message.className = `assistant__message assistant__message--${type}`; message.textContent = text; $("#assistant-messages").append(message); message.scrollIntoView({ block: "end" }); return message; }
  function openAssistant() { closeCommand(); const panel = $("#assistant"); panel.classList.add("is-open"); panel.setAttribute("aria-hidden", "false"); document.body.classList.add("is-locked"); setTimeout(() => $("#assistant-input").focus(), 250); }
  function closeAssistant() { const panel = $("#assistant"); panel.classList.remove("is-open"); panel.setAttribute("aria-hidden", "true"); if (!$("#command").classList.contains("is-open") && !$("#menu-panel").classList.contains("is-open")) document.body.classList.remove("is-locked"); }

  function setupContact() {
    const form = $("#contact-form");
    $$("[data-intent]").forEach(button => button.addEventListener("click", () => {
      $$("[data-intent]").forEach(item => item.classList.toggle("is-active", item === button));
      form.elements.message.value = button.dataset.intent; form.elements.message.focus();
    }));
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const status = $("#form-status"); const submit = $(".send-button", form);
      if (!form.checkValidity()) { form.reportValidity(); status.textContent = "Please complete each field before sending."; return; }
      const payload = Object.fromEntries(new FormData(form).entries());
      submit.disabled = true; submit.classList.add("is-sending"); status.textContent = "Sending your signal…";
      try {
        let reference;
        if (siteDemo) { await wait(850); reference = `DEMO-${Date.now().toString().slice(-6)}`; }
        else {
          const response = await fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
          const data = await response.json(); if (!response.ok) throw new Error(data.error || "Unable to send"); reference = data.reference || "received";
        }
        status.textContent = `Signal received — reference ${reference}.`;
        form.reset(); $$("[data-intent]").forEach(item => item.classList.remove("is-active")); toast("Message interaction completed");
      } catch (error) { status.textContent = error.message || "Something went wrong. Please connect through LinkedIn."; }
      finally { submit.disabled = false; submit.classList.remove("is-sending"); }
    });
  }

  function toast(message) { const element = $("#toast"); element.textContent = message; element.classList.add("is-visible"); clearTimeout(toast.timer); toast.timer = setTimeout(() => element.classList.remove("is-visible"), 2400); }
  function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

  document.addEventListener("DOMContentLoaded", () => {
    setupMotion(); setupNavigation(); setupMenu(); setupSceneObserver(); setupPointerEffects(); setupRoleCycle(); setupPrinciples(); setupCapabilities(); setupProjects(); setupTimeline(); setupCommand(); setupAssistant(); setupContact(); boot();
    updateScene(0);
  });
})();
