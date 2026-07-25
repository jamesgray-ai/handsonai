---
title: Learn with James
description: Multiple ways to learn AI hands-on with James Gray — live cohort courses, corporate training, 1-on-1 coaching, and the Graymatter newsletter
---

<style>
/* ── Courses page ── */

.courses-intro {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--sl-color-gray-2);
  max-width: 42rem;
  margin-bottom: 2.5rem;
}

/* Featured course cards */
.featured-courses {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.course-card {
  border: 1px solid var(--sl-color-gray-5);
  border-left: 4px solid var(--sl-color-accent);
  border-radius: 8px;
  padding: 1.75rem 2rem;
  background: var(--sl-color-gray-6);
  transition: border-left-color 0.2s ease, box-shadow 0.2s ease;
}

.course-card:hover {
  border-left-color: var(--sl-color-accent);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

:root[data-theme='light'] .course-card {
  background: #fff;
  border-color: #d4d4d0;
  border-left-color: #282828;
}

:root[data-theme='light'] .course-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.course-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
}

.course-card h3 a {
  text-decoration: none !important;
  color: var(--sl-color-white);
}

:root[data-theme='light'] .course-card h3 a {
  color: #1a1a18;
}

.course-card h3 a:hover {
  text-decoration: underline !important;
}

.course-card p {
  margin: 0 0 1rem 0;
  color: var(--sl-color-gray-2);
  font-size: 0.95rem;
  line-height: 1.6;
}

.course-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1rem;
}

.course-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  background: var(--sl-color-gray-5);
  color: var(--sl-color-gray-1);
}

:root[data-theme='light'] .course-badge {
  background: #eaeae6;
  color: #484846;
}

.course-audience {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1rem;
  font-size: 0.85rem;
  color: var(--sl-color-gray-3);
}

.course-audience li::before {
  content: "→ ";
  color: var(--sl-color-accent);
}

:root[data-theme='light'] .course-audience li::before {
  color: #6e6e6c;
}

.course-cta {
  display: inline-block;
  margin-top: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--sl-color-accent) !important;
  text-decoration: none !important;
  transition: opacity 0.15s ease;
}

.course-cta:hover {
  opacity: 0.8;
  text-decoration: underline !important;
}

:root[data-theme='light'] .course-cta {
  color: #282828 !important;
}

/* Secondary offerings — compact rows */
.offerings-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 3rem;
  border: 1px solid var(--sl-color-gray-5);
  border-radius: 8px;
  overflow: hidden;
}

:root[data-theme='light'] .offerings-list {
  border-color: #d4d4d0;
}

.offering-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--sl-color-gray-5);
  background: var(--sl-color-gray-6);
}

.offering-row:last-child {
  border-bottom: none;
}

:root[data-theme='light'] .offering-row {
  background: #fff;
  border-bottom-color: #eaeae6;
}

.offering-row strong {
  flex-shrink: 0;
  min-width: 10rem;
  font-size: 0.95rem;
}

.offering-row span {
  flex: 1;
  font-size: 0.88rem;
  color: var(--sl-color-gray-2);
  line-height: 1.5;
}

.offering-row a {
  flex-shrink: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--sl-color-accent) !important;
  text-decoration: none !important;
  white-space: nowrap;
}

.offering-row a:hover {
  text-decoration: underline !important;
}

:root[data-theme='light'] .offering-row a {
  color: #282828 !important;
}

@media (max-width: 600px) {
  .offering-row {
    flex-direction: column;
    gap: 0.25rem;
  }
  .offering-row strong {
    min-width: unset;
  }
}

/* Expect section */
.expect-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

@media (max-width: 600px) {
  .expect-grid {
    grid-template-columns: 1fr;
  }
}

.expect-item {
  padding: 1rem 1.25rem;
  border-radius: 6px;
  background: var(--sl-color-gray-6);
  border: 1px solid var(--sl-color-gray-5);
}

:root[data-theme='light'] .expect-item {
  background: #fff;
  border-color: #d4d4d0;
}

.expect-item strong {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.expect-item span {
  font-size: 0.84rem;
  color: var(--sl-color-gray-2);
  line-height: 1.5;
}
</style>

<p class="courses-intro">Live cohort courses, corporate training, personal coaching, and a weekly newsletter — choose the format that fits how you learn best.</p>

<div class="featured-courses">

<div class="course-card">
  <h3><a href="builders/">Agentic AI for Claude Builders</a></h3>
  <div class="course-meta-row">
    <span class="course-badge">5 Weeks</span>
    <span class="course-badge">Live Cohort</span>
    <span class="course-badge">Maven</span>
  </div>
  <p>Move beyond basic AI usage and build production-grade AI systems — configuring a complete builder infrastructure, creating reusable AI capabilities, developing autonomous workflows, and shipping applications using agentic coding principles.</p>
  <ul class="course-audience">
    <li>Operational Leaders</li>
    <li>Builder-Founders</li>
    <li>AI-First Professionals</li>
  </ul>
  <a class="course-cta" href="builders/">View syllabus & enroll →</a>
</div>

<div class="course-card">
  <h3><a href="leaders/">Hands-on Agentic AI for Leaders</a></h3>
  <div class="course-meta-row">
    <span class="course-badge">4 Weeks</span>
    <span class="course-badge">Live Cohort</span>
    <span class="course-badge">Maven</span>
  </div>
  <p>Go beyond ChatGPT prompting to get hands-on experience building AI-powered workflows, autonomous agents, and browser automations — the practical skills leaders need to reimagine business processes and communicate credibly with technical teams.</p>
  <ul class="course-audience">
    <li>Leaders & Professionals</li>
    <li>Non-technical Executives</li>
    <li>Managers</li>
  </ul>
  <a class="course-cta" href="leaders/">View syllabus & enroll →</a>
</div>

</div>

<div class="offerings-list">
  <div class="offering-row">
    <strong>Corporate Training</strong>
    <span>Tailored AI programs for your organization — half-day workshops to multi-week courses</span>
    <a href="https://jamesgray.ai/corporate-ai-training">Schedule a call →</a>
  </div>
  <div class="offering-row">
    <strong>1-on-1 Coaching</strong>
    <span>Personalized guidance for leaders and builders, tailored to your goals</span>
    <a href="https://jamesgray.ai/coaching">Book a session →</a>
  </div>
  <div class="offering-row">
    <strong>Graymatter</strong>
    <span>Weekly newsletter for builders — simplifying what's possible and showing you how</span>
    <a href="https://graymatter.jamesgray.ai">Subscribe →</a>
  </div>
</div>

## What to Expect

<div class="expect-grid">
  <div class="expect-item">
    <strong>Hands-on practice</strong>
    <span>Build real systems, not just theory</span>
  </div>
  <div class="expect-item">
    <strong>Live interaction</strong>
    <span>Direct access to James in every format</span>
  </div>
  <div class="expect-item">
    <strong>Practical outcomes</strong>
    <span>Skills and systems you can use immediately</span>
  </div>
  <div class="expect-item">
    <strong>Community</strong>
    <span>Course students join a private Slack for peer collaboration</span>
  </div>
</div>
