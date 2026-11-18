
"""
model_loader.py

Loads and unloads the fine-tuned BGE model for inference.
"""

import gc
from pathlib import Path

import torch
from transformers import AutoModel, AutoTokenizer


class ModelLoader:

    _model = None
    _tokenizer = None

    @classmethod
    def load(cls):

        if cls._model is not None:
            return cls._tokenizer, cls._model

        project_root = Path(__file__).resolve().parents[3]

        model_path = (
            project_root
            / "models"
            / "bge_finetuned"
            / "best"
        )

        print(f"Loading model from:\n{model_path}")

        cls._tokenizer = AutoTokenizer.from_pretrained(model_path)

        cls._model = AutoModel.from_pretrained(model_path)

        cls._model.eval()

        print("[SUCCESS] Model loaded successfully")

        return cls._tokenizer, cls._model

    # ==========================================
    # UNLOAD MODEL AND RELEASE MEMORY
    # ==========================================

    @classmethod
    def unload(cls):

        if cls._model is not None:
            del cls._model
            cls._model = None

        if cls._tokenizer is not None:
            del cls._tokenizer
            cls._tokenizer = None

        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        print("[SUCCESS] BGE model unloaded.")
