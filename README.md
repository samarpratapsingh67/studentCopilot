# Customer Churn Model - AWS Deployment

A production-ready ML application with real-time predictions, database persistence, and model retraining capabilities.

---

## 🚀 **LIVE DEPLOYMENT LINKS**

### **Frontend (Vercel)**
- **Status**: Ready for deployment
- **Guide**: See "Deploy Frontend on Vercel" section below
- **Repository**: https://github.com/samarpratapsingh67/Self-Learning-Customer-Churn-Model

### **Backend API (EC2)**
- **URL**: `http://43.205.216.10:5000`
- **Health Check**: `http://43.205.216.10:5000/health`
- **Instance**: AWS EC2 t3.micro (Amazon Linux 2)
- **Region**: ap-south-1 (Mumbai)
- **Docker Image**: `pratapsamar821/churn-backend:latest`

### **Database (RDS PostgreSQL)**
- **Endpoint**: `churn-db.c70oe2qu8iu3.ap-south-1.rds.amazonaws.com`
- **Port**: 5432
- **Status**: Available (free tier eligible)

---

## 📋 **API ENDPOINTS**

```bash
# Health Check
GET /health
Response: {"status": "healthy"}

# Make Prediction
POST /predictAPI
Body: {customer_features_as_json}
Response: {prediction, probability, segment}

# Get Dashboard Stats
GET /dashboardStatsAPI
Response: {total_predictions, churned_count, not_churned_count, retrain_metrics}

# Trigger Model Retrain
POST /retrainAPI
Response: {success, message, metrics}
```

---

## 🧪 **QUICK TEST COMMANDS**

### Test Backend (Windows PowerShell)
```powershell
# Health check
Invoke-WebRequest http://43.205.216.10:5000/health -UseBasicParsing

# Get dashboard stats
Invoke-WebRequest http://43.205.216.10:5000/dashboardStatsAPI -UseBasicParsing
```

---

## 🏗️ **ARCHITECTURE**

```
Browser (Vercel)
    ↓ HTTPS
React + Vite Frontend
    ↓ HTTP:5000
Flask Backend (EC2 Docker)
    ↓ TCP:5432
PostgreSQL (RDS)
```

---

## 📦 **FEATURES**

✅ **Real-time Predictions** - ML inference with automatic database storage  
✅ **Dashboard Analytics** - Live statistics from stored predictions  
✅ **Model Retraining** - Manual retrain button using historical data (min 25 records)  
✅ **Persistence** - All predictions and metrics saved to RDS PostgreSQL  
✅ **Containerized** - Docker backend for easy scaling  
✅ **Cloud-Ready** - Deployed on AWS (EC2, RDS, free tier eligible)  

---

## 📥 **DEPLOYMENT GUIDE**

### **Step 1: Deploy Frontend on Vercel**

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **Add New** → **Project**
4. Select: `Self-Learning-Customer-Churn-Model`
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add **Environment Variable**:
   ```
   VITE_API_BASE_URL = http://43.205.216.10:5000
   ```
7. Click **Deploy**
8. Wait 2-3 minutes for build to complete
9. Open the live URL provided by Vercel

---

### **Step 2: Backend Already Running on EC2**

The backend Docker container is already deployed and running at:
```
http://43.205.216.10:5000
```

To verify it's working:
```powershell
Invoke-WebRequest http://43.205.216.10:5000/health -UseBasicParsing
```

---

### **Step 3: Test End-to-End**

1. Open your Vercel frontend URL
2. Navigate to **Predict** tab
3. Enter customer data (age, credit_score, tenure, etc.)
4. Click **Predict**
5. See the prediction result
6. Go to **Dashboard** tab
7. Verify prediction is stored and appears in statistics

---

## 💻 **LOCAL DEVELOPMENT**

### Backend Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python application.py
# Backend runs on http://localhost:5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

---

## 🔧 **ENVIRONMENT VARIABLES**

### Backend (.env or container env)
```
DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD@churn-db.c70oe2qu8iu3.ap-south-1.rds.amazonaws.com:5432/postgres
PORT=5000
ALLOWED_ORIGINS=*
```

### Frontend (.env.local or Vercel)
```
VITE_API_BASE_URL=http://43.205.216.10:5000
```

---

## 📁 **PROJECT STRUCTURE**

```
.
├── application.py              # Flask app with API routes
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend containerization
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   ├── predict_pipeline.py
│   │   ├── train_pipeline.py
│   │   └── retrain_pipeline.py
│   ├── database/
│   │   ├── models.py           # SQLAlchemy models
│   │   └── services.py         # DB CRUD operations
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Predict.jsx     # Prediction UI
│   │   │   └── Dashboard.jsx   # Analytics dashboard
│   │   ├── services/
│   │   │   └── api.js          # API client (points to EC2)
│   │   └── App.jsx
│   ├── vite.config.js
│   └── package.json
├── artifacts/
│   ├── train.csv
│   ├── test.csv
│   └── data.csv
└── notebooks/
    ├── 1_EDA_Gemstone_price.ipynb
    ├── 2_Model_Training_Gemstone.ipynb
    └── 3_Explainability_with_LIME.ipynb
```

---

## 🚨 **TROUBLESHOOTING**

### ❌ "Unable to connect to backend"
- Check EC2 security group allows port 5000
- Verify Docker container is running: `docker ps`
- SSH into EC2 and check logs: `docker logs churn-backend`

### ❌ "Database connection failed"
- Verify RDS endpoint is correct
- Check RDS password is correct
- Verify RDS security group allows port 5432 from EC2

### ❌ "Frontend API calls failing"
- Check `VITE_API_BASE_URL` env var is set on Vercel
- Verify Flask CORS is enabled: `ALLOWED_ORIGINS=*`
- Check browser console for detailed error messages

---

## 📊 **KEY AWS RESOURCES**

| Resource | Details |
|----------|---------|
| **EC2 Instance** | t3.micro, 43.205.216.10, Amazon Linux 2 |
| **EC2 Security Group** | `churn-backend-sg`, allows port 5000 |
| **RDS Database** | PostgreSQL, free tier, publicly accessible |
| **RDS Security Group** | `churn-db-sg`, allows port 5432 |
| **Docker Image** | pratapsamar821/churn-backend:latest |
| **Frontend Host** | Vercel (auto-deployed from GitHub) |

---

## 🔄 **DEPLOYMENT WORKFLOW**

```
1. Edit code locally
   ↓
2. Push to GitHub
   ↓
3. Vercel auto-deploys frontend
   ↓
4. Backend already running on EC2
   ↓
5. Test at Vercel URL
```

---

## 📝 **ORIGINAL PROJECT INFO**

**Original Dataset**: Gemstone Price Prediction  
**Dataset Source**: [Kaggle Playground Series](https://www.kaggle.com/competitions/playground-series-s3e8/data)  

### Model Approach:
1. **Data Ingestion** - CSV loading and train/test split
2. **Data Transformation** - Feature engineering with ColumnTransformer
3. **Model Training** - CatBoost, XGBoost, KNN ensemble with hyperparameter tuning
4. **Prediction Pipeline** - Real-time inference with database persistence
5. **Flask App** - Web UI for predictions and dashboard

### Original Notebooks:
- [EDA Analysis](./notebook/1_EDA_Gemstone_price.ipynb)
- [Model Training](./notebook/2_Model_Training_Gemstone.ipynb)
- [LIME Explainability](./notebook/3_Explainability_with_LIME.ipynb)

---

## 🎯 **NEXT STEPS**

1. ✅ Deploy frontend on Vercel (follow Step 1 above)
2. ✅ Test predictions at your Vercel URL
3. ✅ Monitor dashboard stats
4. ✅ Test manual retrain feature
5. ✅ Share your live deployment link!

---

## 📧 **SUPPORT**

- **Backend Issues**: SSH to EC2 and check `docker logs churn-backend`
- **Database Issues**: Check RDS console for endpoint/security groups
- **Frontend Issues**: Check Vercel deployment logs
- **API Testing**: Use Postman or PowerShell commands above

---

**Status**: 🟢 Production Ready | All services running | AWS free tier eligible
