# Answer Format — Canonical Four-Part Block

Every question in `study.md` gets exactly this structure, in this order. Deviations are bugs.

## The four parts

### 1. Answer

2–4 paragraphs of Erik-voice prose (see `VOICE.md`). It must:

- Restate the question implicitly through the answer (don't quote the question header — the H2 above already does that).
- Lead with the *theological substance*, not throat-clearing. No "That's a great question."
- Use scripture references inline as needed; the verses themselves are printed in full in part 2.
- End with a directional sentence — the implication or the so-what — not a tidy summary bow.

### 2. Biblical Support

A numbered list, 2–4 entries:

```markdown
1. **Reference 1:1–4** (CSB)
   > Full verse text. Every word. No ellipses unless the omitted text is genuinely
   > irrelevant *and* clearly marked.
```

Rules:

- **Translation tag in parens.** `(CSB)` by default; `(ESV)` if the run is ESV.
- **Full text only.** No bare refs, ever, anywhere in either file.
- **Order**: most-load-bearing verse first. Anchor passage first, supporting passages after.
- **Multi-verse refs**: print all verses inside one blockquote; preserve verse numbers in **bold** if the surrounding paragraphs benefit from them.

### 3. Word Studies

A bullet list, 1–3 entries. Each entry:

```markdown
- **Greek: *transliteration* (Original Script)** — "gloss." Theological payload — what does this word do in this passage that an English translation flattens?
```

For Hebrew, swap `Greek:` → `Hebrew:` and use Hebrew script.

Rules:

- Original script *and* transliteration both required. Reformed bible-study readers want both.
- The "payload" sentence is the point. Don't just transliterate and stop.
- One word per entry. If two words bear together (e.g. *skia / sōma*), pair them in the bold lead and explain together.

### 4. Personal Application

One paragraph, ~3–6 sentences. Must be:

- **Concrete.** A specific, observable action — usually this-week-scoped.
- **Erik-personal.** Erin, the kids, work-as-engineer details land here when they fit.
- **Gospel-fueled.** Application flows from indicative (what Christ has done), not raw imperative. No moralism.

❌ "Pray more this week."
✅ "This week, before responding to the next sharp message in our team Slack, I'll wait 30 seconds and pray Prov 15:1 — *a soft answer turns away wrath* — out loud at my desk."

## Full example

> ## Q3. How do we implement the ideas in verse seven?
>
> **Answer.** Verse 7 gives four participles … *(2–4 paragraphs of Erik voice)* …
>
> **Biblical Support:**
>
> 1. **Colossians 2:6–7** (CSB)
>    > So then, just as you have received Christ Jesus as Lord, continue to walk in him, being rooted and built up in him and established in the faith, just as you were taught, and overflowing with gratitude.
>
> 2. **Jeremiah 17:7–8** (CSB)
>    > The person who trusts in the Lord, whose confidence indeed is the Lord, is blessed. He will be like a tree planted by water …
>
> **Word Studies:**
>
> - **Greek: *peripateō* (περιπατέω)** — "to walk, to conduct one's life." Hebrew equivalent *halak* (הָלַךְ). The picture is *cumulative steps over time* — the Christian life is a long walk in the same direction, not a series of mountaintop sprints.
> - **Greek: *eucharistia* (εὐχαριστία)** — "thanksgiving." The word behind "Eucharist." Paul keeps coming back to it (Col 1:12; 2:7; 3:15, 17; 4:2). Gratitude is not the cherry on top — it's the diagnostic vital sign.
>
> **Personal Application.** Erin and the kids see my real walk, not the curated version. This week I'll … *(specific, named)*

## Pre-commit checklist

- [ ] All four parts present, in order, for every question.
- [ ] Every reference anywhere is printed in full.
- [ ] Translation tag consistent across both files.
- [ ] Word studies include script + transliteration + payload.
- [ ] Application names a concrete action and (when fitting) names Erin/kids.
- [ ] No moralism — gospel indicatives precede imperatives.
