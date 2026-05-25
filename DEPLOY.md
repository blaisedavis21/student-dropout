# Deploy to Hugging Face Spaces

## 1. Create a Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space name:** e.g. `student-dropout-retainai` (or `group-f-dropout`)
3. **License:** MIT
4. **SDK:** Streamlit
5. **Visibility:** Public (or Private if your course allows)
6. Click **Create Space**

## 2. Install Git LFS (one-time, for .pkl files)

Download: [git-lfs.com](https://git-lfs.com/)

```powershell
git lfs install
```

## 3. Push your project

Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with your Hugging Face username and space name.

```powershell
cd "c:\Users\blais\OneDrive\Desktop\assignment"

git init
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add app.py requirements.txt README.md .gitignore
git add best_model.pkl scaler.pkl label_encoder.pkl feature_columns.pkl
git commit -m "Deploy RetainAI Streamlit app to Hugging Face"

git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push -u origin main
```

When prompted for password, use a **Hugging Face Access Token** (not your account password):

1. [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create token with **Write** permission
3. Paste as password when `git push` asks

## 4. Wait for build

The Space builds automatically (2–5 minutes). Your live URL:

`https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## Files uploaded (only what the app needs)

| File | Purpose |
|------|---------|
| `app.py` | Streamlit app |
| `requirements.txt` | Python dependencies |
| `README.md` | Space config + description |
| `best_model.pkl` | Model |
| `scaler.pkl` | Feature scaling |
| `label_encoder.pkl` | Class labels |
| `feature_columns.pkl` | Feature order |

**Not uploaded:** notebook, `all_models.pkl`, CSV (saves space and build time).

## Troubleshooting

- **Build fails on sklearn:** `requirements.txt` pins `scikit-learn==1.6.1` to match your saved model.
- **LFS errors:** Run `git lfs install` before `git add`.
- **Push rejected:** Ensure the Space exists and the remote URL matches exactly.
