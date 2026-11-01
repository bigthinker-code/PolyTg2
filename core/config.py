"""Everything you may want to edit lives here."""

# Hugging Face repo that holds the trained files
HF_REPO = "Abdulroheem/PolyTg"
MODEL_FILE = "polymer_tg_extra_trees.pkl"
AD_FILE = "applicability_domain.pkl"
UNCERTAINTY_FILE = "uncertainty_configuration.pkl"

# Test set results (15% held out)
MODEL_STATS = {
    "MAE": "26.47 K",
    "RMSE": "38.90 K",
    "R²": "0.879",
    "Interval coverage": "90.23%",
}

EVAL_DETAILS = [
    ("Curated dataset", "7,367 polymers"),
    ("Retained dataset", "7,363 polymers"),
    ("Training set (70%)", "5,154"),
    ("Calibration set (15%)", "1,104"),
    ("Test set (15%)", "1,105"),
    ("Model", "Extra Trees Regressor"),
    ("Number of estimators", "700"),
    ("Input descriptors", "100"),
    ("Conformal interval threshold", "62.447 K"),
    ("Average interval width", "124.893 K"),
]

GROUPED_CV = {"MAE": "41.456 K", "RMSE": "54.128 K", "R²": "0.639"}

AD_STATS = [
    ("Inside the domain", "1,045 test samples", "MAE 26.043 K"),
    ("Outside the domain", "60 test samples", "MAE 33.969 K"),
]
AD_NOTE = (
    "Nearest neighbour distance and prediction error are weakly but significantly linked "
    "(Spearman 0.177, p = 3.36 × 10⁻⁹)."
)

ENGINEER = {
    "name": "Agboola Abdulroheem Oyindamola",
    "role": "Machine learning engineer and biochemist",
    "bio": (
        "I graduated with First Class Honours in Biochemistry from the University of Ilorin "
        "and work from Nigeria. My background covers wet lab research, quality control, green chemistry, sustainable catalysis "
        "data analysis and chemoinformatics. I built PolyTg to make polymer property "
        "prediction easier to use and easier to question."
    ),
    "photo": "assets/photo.jpg",  # optional, add the file to show it
}

# Empty links are not shown
LINKS = {
    "GitHub": "https://github.com/bigthinker-code",
    "Hugging Face": "https://huggingface.co/Abdulroheem",
    "Medium": "",
    "Portfolio": "",
    "LinkedIn": "",
}
