## 1. Code Generation and Developer Assistants

AI coding assistants place a language model inside the editor, where it
suggests the next lines as you type, writes functions from a comment, explains
unfamiliar code, and drafts tests. The model sees the current file and nearby
code, then predicts what you would write next. Newer *agentic* tools go
further and carry out multi-step tasks themselves — editing several files,
running tests, and retrying on failure. This is the most widely adopted
category of generative AI in software.

**Key business value**
- Cuts time spent on repetitive patterns.
- Speeds up work in unfamiliar languages and APIs.
- Shortens onboarding — new joiners can ask the codebase directly.

**Technical challenges**
- The model sees only part of the repository, so it may reinvent code that
  already exists.
- Inline suggestions must return in a few hundred milliseconds to stay useful.
- Keeping output consistent with team conventions and internal libraries.

**Weak points**
- **Hallucination** — the model invents functions and libraries that do not
  exist, and states them confidently. Looking correct is what makes it risky.
- Nothing is verified; every suggestion needs review and test coverage.

**Existing implementations**
- [GitHub Copilot](https://github.com/features/copilot) — The most widely used
  IDE assistant, with inline completion and chat across major editors.
- [Cursor](https://cursor.com) — An editor built around AI, with
  repository-wide context and multi-file editing.
- [Claude Code](https://claude.com/claude-code) — A terminal agentic tool that
  reads, edits, and runs code across a project.

---

## 2. Retrieval-Augmented Generation over Internal Knowledge

A model only knows what it learned in training — not your company's policies or
incident reports. **RAG** fixes this by looking up relevant documents first and
passing them to the model with the question. Documents are split into passages
(**chunking**), each converted into an **embedding** — numbers representing its
meaning, arranged so similar topics sit close together. These are stored in a
**vector database** built for fast similarity search. At query time the
question is embedded too, the closest passages are retrieved, and the model
answers from that material rather than memory. This is **grounding**, and it
lets answers cite their source.

**Key business value**
- Employees get answers across scattered systems without knowing where files live.
- Knowledge stays current by updating the index — no retraining needed.
- Answers can carry citations, so claims are verifiable.

**Technical challenges**
- Chunk size is a tradeoff: too small loses context, too large dilutes relevance.
- Retrieval quality is usually the bottleneck, not the model.
- Keeping the index fresh as documents change.

**Weak points**
- When retrieval misses, the model answers from memory with identical
  confidence — the user cannot tell.
- Output quality is capped by documentation quality.
- A citation can point to a real document that does not support the claim.

**Existing implementations**
- [Glean](https://www.glean.com) — Enterprise search across connected company
  apps, respecting existing permissions.
- [Microsoft 365 Copilot](https://www.microsoft.com/microsoft-365/copilot) —
  Retrieval over an organization's own documents, mail, and chats.
- [Perplexity Enterprise](https://www.perplexity.ai/enterprise) — Combines web
  retrieval with internal company files.

---

## 3. Visual Content Generation (Image and Video)

Image generators use **diffusion models**. In training they learn to reverse
the addition of random noise to images; to generate, they start from pure noise
and remove it step by step, guided at each step by the text prompt, until an
image emerges. Video extends this across time, and that is where the difficulty
lies: every frame must be plausible alone and consistent with its neighbours so
motion looks continuous — **temporal consistency**. This costs far more compute,
which is why generated clips run seconds rather than minutes while image
generation is already cheap and mature. Common uses are marketing assets,
concept art, product variants, and advertising creative at volume.

**Key business value**
- Collapses the cost of a first draft — twenty directions explored before
  committing to one.
- Localized variants for many markets without separate photoshoots.
- Designers iterate in minutes instead of days.

**Technical challenges**
- Control is imprecise; a specific composition often takes many attempts.
- Consistency across a series — same character, product, or style — is hard and
  needs reference images or fixed random **seeds**.
- Compute cost is high, dramatically so for video.

**Weak points**
- **Copyright and training-data provenance are unresolved** and actively
  litigated.
- Output cannot be guaranteed in advance, which blocks risk-averse brands.
- Physical errors persist: hands, reflections, and objects that shift between
  video frames.
- Deepfakes and likeness misuse are a real harm.
- Style copies from artists whose work was trained on.

**Existing implementations**
- [Midjourney](https://www.midjourney.com) — Image generator known for strong
  aesthetic defaults.
- [Adobe Firefly](https://www.adobe.com/products/firefly.html) — Trained on
  licensed content, positioned as commercially safe.
- [Runway](https://runwayml.com) — Video generation and editing aimed at film
  production workflows.

---