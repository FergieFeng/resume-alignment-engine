# Non-Technical Workflow

This version explains the workflow for non-technical readers.

For the technical version (flowchart + JSON contracts), see `docs/architecture/workflow_technical.md`.

## What the system does

The system helps a job seeker answer three practical questions:

1. Should I apply for this role?
2. What might be risky or hard in this role?
3. If I apply, what should I improve in my resume first?

## How it works (simple view)

1. You provide two things:
   - the job description,
   - your resume.
2. The system reads both and compares them.
3. It checks where your background is strong and where gaps exist.
4. It can optionally detect hidden expectations in the role (for example, ownership level).
5. It can optionally attach evidence to explain each major conclusion.
6. It gives you a final recommendation:
   - `Apply`, `Edge Apply`, or `No Apply`.
7. It gives a short action list to improve your resume.

## What is optional

- Hidden expectation analysis (optional)
- Evidence mapping for explainability (optional)

If these optional parts are off, the system still gives a valid final recommendation.

## Example (non-technical)

### Input

- Job asks for strong SQL, stakeholder communication, and ownership.
- Candidate resume shows SQL, dashboard projects, and team collaboration.

### Output

- Decision: `Edge Apply`
- Why: good SQL fit, but limited evidence of senior ownership and measurable impact.
- Suggested improvements:
  1. Add one bullet showing end-to-end ownership.
  2. Add one bullet with measurable business impact.

## What this does not do

- It does not guarantee interview outcomes.
- It does not fully rewrite resumes automatically by default.
- It gives decision support and targeted improvement guidance.
