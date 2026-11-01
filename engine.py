import joblib
import numpy as np
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download
from polymetrix.featurizers.polymer import Polymer
from rdkit import Chem

from featurizer import get_featurizer
from core import config


def validate_psmiles(text: str) -> str:
    s = (text or "").strip()
    if not s:
        raise ValueError("Enter a polymer SMILES to start.")
    if s.count("*") != 2:
        raise ValueError(
            "A polymer SMILES needs exactly two [*] markers, one at each end of the "
            "repeat unit. Example: [*]CC([*])c1ccccc1"
        )
    if Chem.MolFromSmiles(s) is None:
        raise ValueError(
            "RDKit could not read this structure. Check the brackets, rings and atom symbols."
        )
    return s


class Engine:
    def __init__(self, model, ad, uncertainty, featurizer, feature_columns):
        self.model = model
        self.ad = ad
        self.uncertainty = uncertainty
        self.featurizer = featurizer
        self.generated = list(feature_columns)
        self.expected = list(ad["feature_columns"])

        if len(set(self.generated)) != len(self.generated):
            raise ValueError("Duplicate feature names were generated.")
        if set(self.generated) != set(self.expected):
            missing = [n for n in self.expected if n not in self.generated]
            unexpected = [n for n in self.generated if n not in self.expected]
            raise ValueError(
                f"Feature names do not match the trained model. Missing: {missing}. "
                f"Unexpected: {unexpected}."
            )
        pos = {n: i for i, n in enumerate(self.generated)}
        self.order = [pos[n] for n in self.expected]

    def predict(self, psmiles: str) -> dict:
        psmiles = validate_psmiles(psmiles)
        polymer = Polymer.from_psmiles(psmiles)
        feats = np.asarray(self.featurizer.featurize(polymer))
        if feats.ndim == 1:
            feats = feats.reshape(1, -1)
        if feats.shape[1] != len(self.generated):
            raise ValueError("Generated feature count does not match the feature labels.")
        X = pd.DataFrame(feats[:, self.order], columns=self.expected)

        pred = float(self.model.predict(X)[0])
        margin = float(self.uncertainty["conformal_threshold"])

        scaled = self.ad["scaler"].transform(X)
        dist = float(self.ad["nearest_neighbors"].kneighbors(scaled, n_neighbors=1)[0][0][0])
        threshold = float(self.ad["ad_threshold"])

        return {
            "psmiles": psmiles,
            "tg_k": round(pred, 2),
            "tg_c": round(pred - 273.15, 2),
            "lower": round(pred - margin, 2),
            "upper": round(pred + margin, 2),
            "width": round(2 * margin, 2),
            "distance": round(dist, 3),
            "threshold": round(threshold, 3),
            "in_domain": dist <= threshold,
        }


@st.cache_resource(show_spinner="Loading the PolyTg model from Hugging Face...")
def get_engine() -> Engine:
    model = joblib.load(hf_hub_download(config.HF_REPO, config.MODEL_FILE))
    ad = joblib.load(hf_hub_download(config.HF_REPO, config.AD_FILE))
    unc = joblib.load(hf_hub_download(config.HF_REPO, config.UNCERTAINTY_FILE))
    featurizer, columns = get_featurizer()
    return Engine(model, ad, unc, featurizer, columns)
