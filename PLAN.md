# Goal

Run ScienceAgentBench with RiVault suitable models.

# Steps

1. [done] Python env: `uv venv .venv` + `uv pip install -r requirements.txt` (litellm pinned to 1.53.1, httpx<0.28; no conda on this host).
2. [done] HF dataset `osunlp/ScienceAgentBench` (102 tasks, split `verified`; `run_infer.py` fixed to use it).
3. [blocked] Download `benchmark_verified.zip` from the SharePoint link in README (needs browser login), unzip with password `scienceagentbench` into `benchmark/`.
4. [done] RiVault backend: `engine/rivault_engine.py`; use model names `rivault/<model>` with `$RIVAULT_API_KEY`. Unknown models get zero cost in `agent.py`.
5. [done] RiVault back up 2026-10-13. Chat models: RiVault/{Agentic,Instruction,Reasoning}-{Tiny..Large}, moonshotai/Kimi-K3, zai-org/GLM-5.2, zai-org/GLM-5.3-Flash, deepseek-ai/DeepSeek-V4-Flash(-reasoning), Qwen/Qwen3.8-27B, Qwen/Qwen3.6-35B-A3B, ByteDance-Seed/Seed-OSS-36B-Instruct, meta-llama/Llama-4-Scout-17B-16E-Instruct, Llama-3.2-3B, granite-4.2-3b.
   Candidates (first pass): RiVault/Agentic-Medium, RiVault/Reasoning-Medium, deepseek-ai/DeepSeek-V4-Flash, zai-org/GLM-5.3-Flash, Qwen/Qwen3.8-27B.
6. [done] Smoke-test OK with rivault/RiVault/Agentic-Medium (1 task, ~5 s; `--max_tasks N` added). Smoke-test `run_infer.py --llm_engine_name rivault/<model>` on 1-2 tasks (no `--use_self_debug`: it requires conda env `sci-agent-eval`).
7. [todo] Full inference run via sbatch (`$SBATCH_ACCOUNT`), one job per model.
8. [todo] Evaluation with docker harness (`run_evaluation.sh`); visual judge needs `OPENAI_API_KEY` or a RiVault substitute.
9. [todo] `calculate_metrics.py`; record results here.
