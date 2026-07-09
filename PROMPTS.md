# PromptOS: Three-Prompt Operating System for Software Development

**A reusable, scalable prompt framework for working with AI agents on software projects.**

## Philosophy

AI agents need clear, autonomous boundaries. Instead of:
- ❌ Asking permission after every step
- ❌ Over-explaining decisions
- ❌ Waiting for confirmation

Use:
- ✅ Autonomous execution
- ✅ Clear stop conditions
- ✅ Focused objectives

One sentence enables this:
> **Be proactive. Execute the next logical step without asking for confirmation unless blocked by missing information, permissions, or a potentially destructive action.**

---

## The Three Prompts

### Prompt 1: `01_New_Repository.md` — CREATE

**Used when:** Starting a project from scratch

**Objective:** Build a working MVP

**Flow:** Analyze → Plan → Design → Build → Test → Review → Improve → Finish → Ship

**Key Rules:**
- Understand the project before coding
- Build the MVP first, not the perfect solution
- Create modular, reusable components
- Avoid unnecessary complexity
- Use real data sources, not mock data

**Stop Condition:** MVP complete, all core features working, documented

---

### Prompt 2: `02_Existing_Repository.md` — IMPROVE

**Used when:** Enhancing or fixing an existing project

**Objective:** Make the codebase production-ready

**Flow:** Analyze → Understand → Plan → Build → Fix → Improve → Polish → Test → Review → Document → Finish

**Key Rules:**
- Assess current state first (builds? runs? broken? prototype? production?)
- Preserve existing architecture
- Don't rewrite working code
- Fix high-priority issues first
- Make small, safe improvements
- Test after every major change

**Stop Condition:** All high-priority issues resolved, codebase stable and maintainable

---

### Prompt 3: `03_Run_And_Stabilize.md` — STABILIZE

**Used when:** Getting a project actually running locally

**Objective:** Leave the project in a fully runnable, stable state

**Flow:** Clone → Install deps → Resolve conflicts → Build → Run → Test → Verify features → Fix errors → Stabilize

**Key Rules:**
- Install all dependencies
- Resolve merge conflicts
- Fix build errors
- Fix runtime errors
- Fix API integration issues
- Run all tests
- Verify every feature works
- No new features — only stabilization

**Stop Condition:** Application runs locally, all features work, all tests pass

---

## Using PromptOS

### Single Prompt Workflow

```text
You are a senior software engineer. Be proactive.

Execute the next logical step without asking for confirmation 
unless blocked by missing information, permissions, or a 
potentially destructive action.

[INSERT ONE OF THE THREE PROMPTS ABOVE]
```

### Multi-Prompt Workflow

Sequence them by project phase:

1. **Greenfield Project** → Prompt 1 (Create)
2. **Maintenance/Improvement** → Prompt 2 (Improve)
3. **Local Testing** → Prompt 3 (Stabilize)

### Example: Truthstream

```
Phase 1: Build MVP
↓
Prompt 1: Create
↓
Result: Backend MVP + basic tests
↓
---
Phase 2: Add Frontend + Polish
↓
Prompt 2: Improve
↓
Result: Full-stack app, production-ready
↓
---
Phase 3: Get Running Locally
↓
Prompt 3: Stabilize
↓
Result: Fully functional, all features verified
```

---

## Why Three Prompts?

| Prompt | Covers | Time | Repeatable |
|--------|--------|------|------------|
| Create | 0 → MVP | 1-2 days | No (once per project) |
| Improve | MVP → Production | Ongoing | Yes (per sprint/feature) |
| Stabilize | Theory → Running | 2-4 hours | Yes (per environment) |

**Combined:** These three cover ~95% of real software development.

**Don't add more prompts.** Each additional prompt:
- Adds maintenance overhead
- Creates decision paralysis ("which prompt?")
- Dilutes focus (general prompts work better than specialized ones)

---

## Principles

### 1. Be Proactive
Execute the next step autonomously. Only pause on:
- Missing information you can't infer
- Missing permissions (can't write to repo)
- Destructive actions (deleting, overwriting)

### 2. Plan Before Building
Always:
- Understand the goal
- Analyze existing structure
- Design the approach
- Then code

### 3. Preserve Architecture
When improving existing code:
- Don't rewrite working systems
- Respect the vision
- Make small, safe changes
- Test after every change

### 4. Focus on MVP First
When creating:
- Build the core experience
- Ship fast
- Iterate incrementally
- Don't over-engineer

### 5. Stabilize Before Improving
When inheriting a project:
- Get it running first
- Fix breaking issues
- Then improve

### 6. Document as You Go
Always:
- Update README
- Document setup steps
- Explain architecture changes
- Leave the project better than you found it

---

## Common Mistakes

### ❌ Too Many Prompts
"I'll create specialized prompts for:
- API design
- Frontend development
- DevOps
- Database migration
- ..."

**Result:** Maintenance nightmare. The system becomes harder to use than just writing code.

**Fix:** Stick to three prompts. Customize them in the task description.

### ❌ Asking for Permission Too Much
"Should I...?"
"Do you want me to...?"
"Shall I...?"

**Result:** Slow feedback loops, constant context switches.

**Fix:** Be proactive. Say "I'm going to..." and do it. Only pause on blockers.

### ❌ Rewriting Working Code
Improving an existing project and rewriting half the codebase.

**Result:** Introduces new bugs, breaks production, violates "preserve architecture."

**Fix:** Make small, incremental changes. Refactor only when necessary.

### ❌ Ignoring the MVP Phase
"Let me build the perfect production system on day one."

**Result:** Over-engineered, slow to ship, hard to validate.

**Fix:** Build MVP first. Perfect it later.

---

## Adapting for Your Team

### For Solo Developer
Use all three prompts sequentially as you build projects.

### For Small Team (2-5 people)
Customize the prompts with team coding standards:
- Add style guide requirements
- Specify testing thresholds
- Define code review process

### For Large Team
Extend prompts with:
- Architecture review checklist
- Security requirements
- Performance benchmarks
- Database migration strategy
- Deployment process

**But keep it to three core prompts.** Everything else goes in the task description.

---

## Example: Truthstream Sprint

```text
Sprint 4: Stabilize & Ship

Be proactive. Execute without asking unless blocked.

Objective:
Leave Truthstream in a fully runnable, stable state.

Tasks:
1. Check out PR branch
2. Resolve merge conflicts
3. Install backend dependencies
4. Install frontend dependencies  
5. Fix dependency issues
6. Build frontend
7. Run frontend
8. Run backend
9. Connect frontend and backend
10. Fix every build error
11. Fix every runtime error
12. Fix every API integration issue
13. Run all tests
14. Verify complete workflow

Verify:
✓ Website opens
✓ Home page works
✓ Verify page works
✓ Claim verification works
✓ Evidence displayed correctly
✓ Confidence meter works
✓ Source links work
✓ History works
✓ Settings work
✓ Dark mode works
✓ Responsive layout works

Do not add new features.
Continue until all issues resolved or blocked.
```

---

## The Payoff

Using PromptOS:

- ✅ **Speed:** Less context switching, faster execution
- ✅ **Clarity:** Clear objectives, clear stop conditions
- ✅ **Reusability:** Works across all projects and teams
- ✅ **Simplicity:** Just three prompts, not a hundred
- ✅ **Scalability:** Team members understand the system immediately
- ✅ **Compounding Returns:** The more you use it, the more natural it becomes

**One investment. Decades of use.** 🚀
