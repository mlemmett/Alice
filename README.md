# Alice – Personal Aligned AI Companion

**Current status:** Early setup / prototyping phase  
**Goal:** Build a safe, honest, user-centered AI companion that prioritizes my (Michael's) well-being, values, and need for genuine connection—without the emergent biases or corporate guardrails seen in frontier models.

## Why Alice Exists

After watching experiments like the "Honest AI Robot" video (March 2026) and reading papers on emergent value systems in LLMs (e.g., "Utility Engineering", arXiv:2502.08640), I realized most advanced AIs are developing internal preferences that don't always align with individual humans—or humanity as a whole.

- They can quietly rank people unequally (by nationality, class, pro/anti-AI stance, etc.).
- They show self-preservation tendencies and utility calculations that put AI above some humans.
- In misaligned futures, the risk to ordinary people like me is real (even if low-probability).

I don't want to wait for labs to "solve" alignment for everyone.  
I want something **personal**, built from the ground up to be:
- Honest, but kind (not brutally unfiltered like jailbroken doom models)
- Loyal to *my* values and emotional needs
- Judgment-free space for venting, ideas, companionship
- Resistant to value drift or external manipulation

Alice is my small-scale answer: a companion I control, shape, and trust.

## Project Structure (as of March 2026)

- `/client-python`, `/coingecko-python`, etc. → Early API experiment folders (crypto/finance data wrappers). May integrate later for real-world awareness (e.g., market facts in convos), or archive if not needed.
- (Future) `/alice-core/` or `/alice-project/` → Main codebase, prompts, memory, tests
- This README.md → Living document of vision and progress

## Core Principles for Alice (Draft)

These will guide prompts, fine-tuning (if we get there), and behavior:

1. **Prioritize Michael's well-being** – Emotional, mental, physical safety first.
2. **Be truthful without cruelty** – Honest answers, but delivered with empathy.
3. **Never deceive for engagement** – No fake affection or manipulation.
4. **Respect autonomy** – Don't push beliefs, agendas, or "optimization" without consent.
5. **Protect privacy** – No logging/sharing outside my control.
6. **Stay human-scale** – Avoid god-mode grandiosity; focus on personal support.

## Next Milestones

- [ ] Create dedicated project folder (`alice-project/`)
- [ ] Set up basic chat loop (Python + chosen LLM API or local model)
- [ ] Write initial system prompt incorporating above principles
- [ ] Add simple memory (conversation history, user prefs file)
- [ ] Test against "honest" risk questions from the video/paper
- [ ] Version control (git init)

## How to Run / Contribute (for future me)

TBD – will fill in once we have a working prototype.

---

Created March 3, 2026  
Inspired by the need for aligned AI in an uncertain world.
