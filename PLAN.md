# Goal

Run ScienceAgentBench with RiVault suitable models.

# Steps

1. [done] Python env: `uv venv .venv` + `uv pip install -r requirements.txt` (litellm pinned to 1.53.1, httpx<0.28; no conda on this host).
2. [done] HF dataset `osunlp/ScienceAgentBench` (102 tasks, split `verified`; `run_infer.py` fixed to use it).
3. [blocked] Download `benchmark_verified.zip` from the SharePoint link in README (needs browser login), unzip with password `scienceagentbench` into `benchmark/`.
4. [done] RiVault backend: `engine/rivault_engine.py`; use model names `rivault/<model>` with `$RIVAULT_API_KEY`. Unknown models get zero cost in `agent.py`.
5. [blocked] List RiVault models (`GET /v1/models` returned HTTP 502 on 2026-10-13); pick candidates.
6. [todo] Smoke-test `run_infer.py --llm_engine_name rivault/<model>` on 1-2 tasks (no `--use_self_debug`: it requires conda env `sci-agent-eval`).
7. [todo] Full inference run via sbatch (`$SBATCH_ACCOUNT`), one job per model.
8. [todo] Evaluation with docker harness (`run_evaluation.sh`); visual judge needs `OPENAI_API_KEY` or a RiVault substitute.
9. [todo] `calculate_metrics.py`; record results here.
