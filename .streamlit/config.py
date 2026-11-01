"""Everything you may want to edit lives here."""

# Hugging Face repo that holds the trained files
HF_REPO = "Abdulroheem/PolyTg"
MODEL_FILE = "polymer_tg_extra_trees.pkl"
AD_FILE = "applicability_domain.pkl"
UNCERTAINTY_FILE = "uncertainty_configuration.pkl"

# Fill these in with your test set results. Leave a value as None to hide it.
MODEL_STATS = {
    "R²": None,
    "MAE (K)": None,
    "RMSE (K)": None,
    "Training polymers": None,
}

ENGINEER = {
    "name": "Agboola Abdulroheem Oyindamola",
    "role": "Machine learning engineer and biochemist",
    "bio": (
        "I graduated with First Class Honours in Biochemistry from the University of Ilorin "
        "and work from Nigeria. My background covers wet lab research, quality control, "
        "data analysis and bioinformatics. I built PolyTg to make polymer property "
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
