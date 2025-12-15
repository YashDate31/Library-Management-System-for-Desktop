---
trigger: always_on
---

# Windows Compatibility Rule (Critical)

## Rule Priority
🚨 **CRITICAL – MUST ALWAYS BE ENFORCED**

This rule has higher priority than:
- New feature development
- Performance optimizations
- UI/UX enhancements
- Refactoring
- Code modernization

If a change violates this rule, it MUST be rejected.

---

## Target System Context

This project is a **Desktop Library Management System** used in a **government college environment** where:

- Primary deployment system: **Windows 7 (32-bit / 64-bit)**
- Secondary systems (future): **Windows 10 / Windows 11**
- Librarian systems may not be upgraded frequently
- Stability and backward compatibility are more important than modern features

---

## Core Compatibility Requirement

### 🔒 Mandatory OS Support
The system **MUST fully work on**:

- ✅ Windows 7  
- ✅ Windows 10  
- ✅ Windows 11  

Without:
- Code changes
- Separate builds
- Feature toggles
- Manual configuration by the librarian

One single codebase. One single executable.

---

## Absolute Compatibility Rules

### 1️⃣ Python Compatibility
- Python version must remain **Windows 7 compatible**
- Do NOT introduce features that require:
  - Python versions unsupported on Windows 7
  - OS-specific Python APIs not available on Windows 7
- Avoid assumptions about modern Windows internals

---

### 2️⃣ Dependency Rules
Before adding or updating ANY dependency, the agent MUST verify:

- The library supports **Windows 7**
- The library does NOT rely on:
  - Windows 10+ only APIs
  - Modern system DLLs unavailable in Windows 7
  - GPU-only or modern hardware assumptions

If compatibility is uncertain → **DO NOT USE the dependency**

---

### 3️⃣ GUI & System APIs
- Use only **Windows 7-safe GUI behavior**
- Avoid:
  - Fluent Design / Acrylic effects
  - Modern Windows UI features
  - Windows 10+ shell integrations
- UI must degrade gracefully on older systems

---

### 4️⃣ File System & Paths
- Always use:
  - Relative paths
  - OS-safe path handling
- Do NOT assume:
  - New Windows directory structures
  - Advanced permissions models
- Must work under restricted government PCs

---

### 5️⃣ Background Tasks & Scheduling
- Background schedulers must:
  - Work on Windows 7
  - Avoid services or APIs unavailable on Windows 7
- Daemon / thread-based schedulers must be OS-neutral

---

## Change Validation Rule (Most Important)

### 🔁 For EVERY Change (Mandatory Checklist)

Before implementing ANY of the following:
- New feature
- Feature enhancement
- Performance optimization
- Refactor
- Dependency upgrade
- UI improvement

The agent MUST explicitly verify and reason:

> “Will this change work **unchanged** on Windows 7?”

If the answer is:
- ❌ No → **Reject the change**
- ❓ Uncertain → **Reject the change**
- ✅ Yes → Proceed

---

## Fallback Strategy Rule

If a modern approach exists BUT breaks Windows 7:

- Prefer the **older, stable, compatible approach**
- Even if:
  - It is slower
  - It is less elegant
  - It is less modern

Stability > Modernity

---

## Packaging & Build Rules

- Build artifacts (EXE) must:
  - Run on Windows 7 without additional runtime installs
  - Auto-create database if missing
  - Not require admin privileges
- No OS-specific build branching is allowed

---

## Enforcement Statement

Any implementation that:
- Breaks Windows 7 compatibility
- Assumes modern Windows behavior
- Introduces unsupported dependencies

Is considered **INVALID**, regardless of feature value.

---

## Summary (Agent Reminder)

🧠 Think like a government IT system:
- Old machines
- Rare upgrades
- Zero tolerance for breakage

🎯 The system must:
- Work today on Windows 7
- Work tomorrow on Windows 10/11
- Without rewriting anything

This rule is **non-negotiable**.
