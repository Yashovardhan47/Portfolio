const header = document.querySelector("#site-header");
const progress = document.querySelector("#scroll-progress-bar");
const navToggle = document.querySelector("#nav-toggle");
const navMenu = document.querySelector("#nav-menu");
const navLinks = [...document.querySelectorAll(".nav-menu > a")];
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function updateChrome() {
  const top = window.scrollY;
  const available = document.documentElement.scrollHeight - window.innerHeight;
  header.classList.toggle("scrolled", top > 12);
  progress.style.width = `${available > 0 ? Math.min((top / available) * 100, 100) : 0}%`;
}

window.addEventListener("scroll", updateChrome, { passive: true });
updateChrome();

navToggle.addEventListener("click", () => {
  const open = !navMenu.classList.contains("open");
  navMenu.classList.toggle("open", open);
  navToggle.setAttribute("aria-expanded", String(open));
  navToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
});

navLinks.forEach((link) => link.addEventListener("click", () => {
  navMenu.classList.remove("open");
  navToggle.setAttribute("aria-expanded", "false");
}));

const sections = [...document.querySelectorAll("main section[id]")];
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
    });
  });
}, { rootMargin: "-35% 0px -58% 0px" });
sections.forEach((section) => navObserver.observe(section));

const revealItems = document.querySelectorAll(".reveal");
if (reduceMotion) {
  revealItems.forEach((item) => item.classList.add("visible"));
} else {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.1 });
  revealItems.forEach((item) => revealObserver.observe(item));
}

const contactForm = document.querySelector("#contact-form");
const formStatus = document.querySelector("#form-status");
contactForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!contactForm.reportValidity()) return;
  const button = contactForm.querySelector("button[type='submit']");
  const data = Object.fromEntries(new FormData(contactForm).entries());
  button.disabled = true;
  formStatus.textContent = "Sending…";
  formStatus.className = "";

  try {
    const response = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Unable to send your message.");
    formStatus.textContent = `${result.message} Reference: ${result.reference || "received"}`;
    formStatus.className = "success";
    contactForm.reset();
  } catch (error) {
    formStatus.textContent = error.message;
    formStatus.className = "error";
  } finally {
    button.disabled = false;
  }
});

const assistantPanel = document.querySelector("#assistant-panel");
const assistantClose = document.querySelector("#assistant-close");
const assistantBackdrop = document.querySelector("#panel-backdrop");
const assistantForm = document.querySelector("#assistant-form");
const assistantInput = document.querySelector("#assistant-question");
const assistantMessages = document.querySelector("#assistant-messages");
let assistantTrigger = null;

function openAssistant(event) {
  assistantTrigger = event?.currentTarget || document.activeElement;
  assistantPanel.classList.add("open");
  assistantPanel.setAttribute("aria-hidden", "false");
  assistantBackdrop.hidden = false;
  document.body.classList.add("panel-open");
  window.setTimeout(() => assistantInput.focus(), 180);
}

function closeAssistant() {
  assistantPanel.classList.remove("open");
  assistantPanel.setAttribute("aria-hidden", "true");
  assistantBackdrop.hidden = true;
  document.body.classList.remove("panel-open");
  assistantTrigger?.focus();
}

document.querySelectorAll("[data-open-assistant]").forEach((button) => button.addEventListener("click", openAssistant));
assistantClose.addEventListener("click", closeAssistant);
assistantBackdrop.addEventListener("click", closeAssistant);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && assistantPanel.classList.contains("open")) closeAssistant();
});

function addMessage(text, type, sources = []) {
  const wrapper = document.createElement("div");
  wrapper.className = `message message-${type}`;
  const content = document.createElement("div");
  content.textContent = text;
  wrapper.append(content);

  if (sources.length) {
    const sourceList = document.createElement("div");
    sourceList.className = "message-sources";
    sources.forEach((source) => {
      const link = document.createElement("a");
      link.href = source.url;
      link.target = source.url.startsWith("/") ? "_self" : "_blank";
      link.rel = "noopener";
      link.textContent = source.label;
      sourceList.append(link);
    });
    wrapper.append(sourceList);
  }
  assistantMessages.append(wrapper);
  assistantMessages.scrollTop = assistantMessages.scrollHeight;
  return wrapper;
}

async function askAssistant(question) {
  addMessage(question, "user");
  const pending = addMessage("Looking through verified portfolio evidence…", "assistant");
  try {
    const response = await fetch("/api/assistant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "I could not answer that.");
    pending.remove();
    addMessage(result.answer, "assistant", result.sources || []);
  } catch (error) {
    pending.textContent = error.message;
  }
}

assistantForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = assistantInput.value.trim();
  if (question.length < 3) return;
  assistantInput.value = "";
  askAssistant(question);
});

document.querySelectorAll(".suggested-prompts button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector(".suggested-prompts")?.remove();
    askAssistant(button.textContent.trim());
  });
});

const caseDialog = document.querySelector("#case-dialog");
const projects = JSON.parse(document.querySelector("#project-data").textContent);
document.querySelectorAll("[data-project]").forEach((button) => {
  button.addEventListener("click", () => {
    const project = projects.find((item) => item.id === button.dataset.project);
    if (!project) return;
    document.querySelector("#dialog-category").textContent = project.category;
    document.querySelector("#dialog-title").textContent = project.title;
    document.querySelector("#dialog-tagline").textContent = project.tagline;
    document.querySelector("#dialog-problem").textContent = project.problem;
    document.querySelector("#dialog-solution").textContent = project.solution;
    document.querySelector("#dialog-evidence").textContent = project.evidence;
    const stack = document.querySelector("#dialog-stack");
    stack.replaceChildren(...project.stack.map((item) => {
      const tag = document.createElement("span");
      tag.textContent = item;
      return tag;
    }));
    document.querySelector("#dialog-link").href = project.github;
    caseDialog.showModal();
  });
});

document.querySelector(".dialog-close").addEventListener("click", () => caseDialog.close());
caseDialog.addEventListener("click", (event) => {
  const bounds = caseDialog.getBoundingClientRect();
  const outside = event.clientX < bounds.left || event.clientX > bounds.right ||
    event.clientY < bounds.top || event.clientY > bounds.bottom;
  if (outside) caseDialog.close();
});
