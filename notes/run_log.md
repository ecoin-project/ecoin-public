## 2026-04-03
- First v2 live run completed successfully.
- Trigger type: manual workflow_dispatch
- Batch ID: 20260403_7e0a52
- Config: PROMPT_FILE=fixed_prompt_v2.json, N_RUNS=3
- Outputs generated successfully, including weekly_summary, latest_summary, master_summary, and trend plots.
- GitHub Actions warning was non-fatal and related to Node.js action deprecation.

---

## 2026-04-04
- Second v2 run completed successfully.
- Trigger type: scheduled weekly workflow
- Batch ID: 20260404_0f52a8
- Config: PROMPT_FILE=fixed_prompt_v2.json, N_RUNS=3
- Outputs generated successfully, including weekly_summary, latest_summary, master_summary, and trend plots.
- master_summary.csv now contains the second v2 longitudinal row.
- Prior mixed-schema history remains preserved in master_summary_legacy.csv.
- GitHub Actions warning was non-fatal and related to Node.js action deprecation.
