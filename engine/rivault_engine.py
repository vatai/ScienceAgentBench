from engine.openai_engine import OpenaiEngine
from openai import OpenAI

import os

RIVAULT_PREFIX = "rivault/"
RIVAULT_BASE_URL = "https://api.class2.llm.ai.r-ccs.riken.jp/v1"


def is_rivault_model(llm_engine_name):
    return llm_engine_name.startswith(RIVAULT_PREFIX)


def strip_rivault_prefix(llm_engine_name):
    return llm_engine_name[len(RIVAULT_PREFIX):]


class RivaultEngine(OpenaiEngine):
    def __init__(self, llm_engine_name):
        self.client = OpenAI(
            api_key=os.environ["RIVAULT_API_KEY"],
            base_url=os.environ.get("RIVAULT_BASE_URL", RIVAULT_BASE_URL),
            max_retries=10,
            timeout=300.0,
        )
        self.llm_engine_name = strip_rivault_prefix(llm_engine_name)
