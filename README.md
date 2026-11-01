PolyTg
Predicts polymer glass transition temperature (Tg) from a polymer SMILES, with a 90% conformal
interval and an applicability domain check. Built with Streamlit. Model files are hosted on
Hugging Face and loaded at runtime (see `core/config.py`).
Run locally: `pip install -r requirements.txt` then `streamlit run app.py`.
Model
Extra Trees Regressor with 700 estimators on 100 PolyMetriX descriptors. The curated dataset
has 7,367 polymers, of which 7,363 were retained and split 70% training (5,154), 15% calibration
(1,104) and 15% test (1,105).
Test set results
Metric	Result
MAE	26.473 K
RMSE	38.904 K
R²	0.879
Interval coverage (90% target)	90.23%
Conformal interval threshold	62.447 K
Average interval width	124.893 K
Generalisation
Grouped cross-validation (GroupKFold) gives MAE 41.456 K, RMSE 54.128 K and R² 0.639.
Performance is weaker when evaluation separates polymer classes, so predictions for classes that
are rare in the training data may be less reliable.
Applicability domain
Group	Test samples	MAE
Inside the domain	1,045	26.043 K
Outside the domain	60	33.969 K
Nearest neighbour distance and prediction error have a Spearman correlation of 0.177
(p = 3.36 × 10⁻⁹). The domain flag and the conformal interval are caution indicators.
Neither guarantees prediction accuracy.
Author
Agboola Abdulroheem Oyindamola, Biochemistry graduate, University of Ilorin, Nigeria.
