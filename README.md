---
title: RetainAI — Student Dropout Prediction
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# RetainAI — Student Success Dashboard

**Group F · Makerere University · Machine Learning Project**

An interactive dashboard for academic advisors to estimate student dropout risk and receive prioritized intervention recommendations. Built with XGBoost on the UCI *Predict Students' Dropout and Academic Success* dataset.

## Features

- Instant dropout probability score with risk tiers (Low / Medium / High)
- Predicted outcome: Dropout, Enrolled, or Graduate
- Color-coded, category-specific intervention cards
- 46 engineered features including semester performance and financial signals

## How to use

1. Enter student background and semester grades
2. Click **Analyze Dropout Risk**
3. Review the risk assessment and recommended actions

## Model files (included in this Space)

- `best_model.pkl` — XGBoost classifier
- `scaler.pkl`, `label_encoder.pkl`, `feature_columns.pkl`

## Disclaimer

This is a screening tool for advisors. Predictions should be reviewed by qualified staff. The model was trained on Portuguese polytechnic data.

## Team

| Name | ID |
|------|-----|
| Tusiime Mark | 2400711684 |
| Namuyimbwa Martha | 2400709436 |
| Ssebyala Denis Tendo | 2400711123 |
| Mulema Blaise Davis | 2400700763 |
| Okure Enock | 2400710690 |
