# Cost Guardrails

- Scheduled OpenAI API runs occur only from the repository default branch.
- The current `N_RUNS` value for the paid workflow is `3`.
- Do not add `push` or `pull_request` triggers to the paid workflow.
- Do not increase `N_RUNS` without explicit approval.
- Manual `workflow_dispatch` runs may trigger paid OpenAI API calls.
