# Gemstone Price Prediction - Utkarsh Gaikwad

### Introduction About the Data :

Please this project is of a student. Just wanted to appreciate for knowledge sharing 

**The dataset** The goal is to predict `price` of given diamond (Regression Analysis).

There are 10 independent variables (including `id`):

* `id` : unique identifier of each diamond
* `carat` : Carat (ct.) refers to the unique unit of weight measurement used exclusively to weigh gemstones and diamonds.
* `cut` : Quality of Diamond Cut
* `color` : Color of Diamond
* `clarity` : Diamond clarity is a measure of the purity and rarity of the stone, graded by the visibility of these characteristics under 10-power magnification.
* `depth` : The depth of diamond is its height (in millimeters) measured from the culet (bottom tip) to the table (flat, top surface)
* `table` : A diamond's table is the facet which can be seen when the stone is viewed face up.
* `x` : Diamond X dimension
* `y` : Diamond Y dimension
* `x` : Diamond Z dimension

Target variable:
* `price`: Price of the given Diamond.

Dataset Source Link :
[https://www.kaggle.com/competitions/playground-series-s3e8/data?select=train.csv](https://www.kaggle.com/competitions/playground-series-s3e8/data?select=train.csv)

### It is observed that the categorical variables 'cut', 'color' and 'clarity' are ordinal in nature

### Check this link for details : [American Gem Society](https://www.americangemsociety.org/ags-diamond-grading-system/)

# AWS Deployment Links (Live)

## **Frontend (Vercel)**
- **URL**: [Deploy to Vercel](https://vercel.com) → Import your GitHub repo
- **Repository**: https://github.com/samarpratapsingh67/Self-Learning-Customer-Churn-Model

## **Backend API (EC2)**
- **URL**: `http://43.205.216.10:5000`
- **Health Check**: `http://43.205.216.10:5000/health`
- **Instance**: AWS EC2 (t3.micro, Amazon Linux 2)
- **Region**: ap-south-1 (Mumbai)

## **Database (RDS PostgreSQL)**
- **Endpoint**: `churn-db.c70oe2qu8iu3.ap-south-1.rds.amazonaws.com`
- **Port**: 5432
- **Database**: `postgres`
- **Status**: Available (free tier)

## **Docker Image (DockerHub)**
- **Repository**: `https://hub.docker.com/r/pratapsamar821/churn-backend`
- **Image**: `pratapsamar821/churn-backend:latest`

## **Key AWS Resources**
- **EC2 Security Group**: `churn-backend-sg` (allows port 5000)
- **RDS Security Group**: `churn-db-sg` (PostgreSQL port 5432)
- **VPC**: Default VPC

## **API Endpoints**

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Prediction
```
POST /predictAPI
Body: {customer features as JSON}
Response: {prediction result with probability}
```

### Dashboard Stats
```
GET /dashboardStatsAPI
Response: {
  "total_predictions": count,
  "churned_predictions": count,
  "not_churned_predictions": count,
  "total_retrain_runs": count,
  "latest_retrain_metrics": {...}
}
```

### Manual Retrain
```
POST /retrainAPI
Response: {
  "success": bool,
  "message": "description",
  "metrics": {...}
}
```

## **Testing the Deployment**

### Test Backend API (Windows PowerShell)
```powershell
# Health check
Invoke-WebRequest http://43.205.216.10:5000/health -UseBasicParsing

# Test prediction
$body = @{
    age = 35
    credit_score = 750
    tenure = 5
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://43.205.216.10:5000/predictAPI" `
  -Method POST `
  -Body $body `
  -ContentType "application/json" `
  -UseBasicParsing
```

## **Testing the Deployment**

### Test Backend API (Windows PowerShell)
```powershell
# Health check
Invoke-WebRequest http://43.205.216.10:5000/health -UseBasicParsing

# Test prediction
$body = @{
    age = 35
    credit_score = 750
    tenure = 5
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://43.205.216.10:5000/predictAPI" `
  -Method POST `
  -Body $body `
  -ContentType "application/json" `
  -UseBasicParsing
```

### Test Frontend
1. Open the Vercel deployed URL
2. Go to "Predict" tab
3. Enter customer data
4. Click "Predict" 
5. Go to "Dashboard" tab to see stored predictions

---

## **Deployment Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
                       ▼
       ┌───────────────────────────────────┐
       │    Frontend (Vercel)              │
       │  - React + Vite                   │
       │  - Tailwind CSS                   │
       │  - Real-time dashboard            │
       │  - Manual retrain button          │
       └─────────────┬───────────────────┘
                     │ HTTP (port 5000)
                     ▼
       ┌───────────────────────────────────┐
       │    Backend (EC2)                  │
       │  - Flask + Gunicorn               │
       │  - Docker container               │
       │  - ML model endpoints             │
       │  - Database integration           │
       └─────────────┬───────────────────┘
                     │ TCP (port 5432)
                     ▼
       ┌───────────────────────────────────┐
       │    Database (RDS PostgreSQL)      │
       │  - Prediction records storage     │
       │  - Model metrics storage          │
       │  - Retrain history logs           │
       └───────────────────────────────────┘
```

---

## **How to Deploy (Step-by-Step)**

### **Option 1: Deploy Frontend on Vercel**
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Select your GitHub repo
4. Set **Root Directory** to `frontend`
5. Add **Environment Variable**:
   - `VITE_API_BASE_URL=http://43.205.216.10:5000`
6. Click **Deploy**

### **Option 2: Deploy Backend on EC2 (Docker)**
1. Build Docker image locally:
   ```powershell
   docker build -t churn-backend .
   docker tag churn-backend pratapsamar821/churn-backend:latest
   docker push pratapsamar821/churn-backend:latest
   ```

2. SSH into EC2:
   ```powershell
   ssh -i "churn-key.pem" ec2-user@43.205.216.10
   ```

3. Pull and run container:
   ```bash
   docker pull pratapsamar821/churn-backend:latest
   docker run -d --name churn-backend -p 5000:5000 \
     -e DATABASE_URL="postgresql+psycopg2://postgres:PASSWORD@churn-db.c70oe2qu8iu3.ap-south-1.rds.amazonaws.com:5432/postgres" \
     pratapsamar821/churn-backend:latest
   ```

4. Verify running:
   ```bash
   docker ps
   ```

### **Option 3: Create RDS Database**
1. Go to AWS RDS Console
2. Create PostgreSQL database
3. Make it publicly accessible (for testing)
4. Update security group to allow port 5432

---

## **Local Development Setup**

### Backend
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python application.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## **Features**

### Prediction
- Real-time ML model inference
- Automatic prediction persistence to RDS PostgreSQL
- Support for multiple ML algorithms (CatBoost, XGBoost, KNN ensemble)

### Dashboard & Analytics
- Live prediction statistics (total predictions, churn count)
- Retrain history and metrics tracking
- Model performance comparison

### Model Retraining
- Manual retrain button in dashboard
- Automatic retrain from stored predictions (min. 25 records required)
- Retrain metrics persistence
- Support for both churn classes

### Deployment Ready
- Docker containerized backend
- Vercel-hosted frontend
- AWS RDS for database persistence
- EC2 for scalable compute

---

## **Project Structure**

```
.
├── application.py              # Flask app entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend containerization
├── artifacts/                  # Data files
│   ├── data.csv
│   ├── train.csv
│   └── test.csv
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
│   │   └── services.py         # DB services
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Predict.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── components/
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── notebooks/
│   ├── 1_EDA_Gemstone_price.ipynb
│   ├── 2_Model_Training_Gemstone.ipynb
│   └── 3_Explainability_with_LIME.ipynb
└── README.md
```

---

## **Environment Variables**

### Backend (.env)
```
DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD@host:5432/postgres
PORT=5000
ALLOWED_ORIGINS=*
```

### Frontend (.env.local)
```
VITE_API_BASE_URL=http://43.205.216.10:5000
```

---

## **Troubleshooting**

### Backend not reachable
- Check EC2 security group allows port 5000
- Verify Docker container is running: `docker ps`
- Check container logs: `docker logs churn-backend`

### Database connection failed
- Verify RDS endpoint and password
- Check RDS security group allows port 5432
- Confirm EC2 and RDS are in same VPC or have proper routing

### Frontend API calls failing
- Check CORS is enabled in Flask (`ALLOWED_ORIGINS="*"`)
- Verify `VITE_API_BASE_URL` environment variable is set
- Check browser console for actual error messages

---

# Screenshot of UI

![HomepageUI](./Screenshots/HomepageUI.jpg)

# YouTube Video Link

Link for YouTube Video : Click the below thumbnail to open 

[![https://youtu.be/Xvk5r0t_RQw](https://i.ytimg.com/vi/Xvk5r0t_RQw/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBbp5SouquUm3Y3t-NYfOYsg4N4oQ)](https://youtu.be/Xvk5r0t_RQw)

# AWS API Link

API Link : [http://gemstonepriceutkarshgaikwad-env.eba-7zp3wapg.ap-south-1.elasticbeanstalk.com/predictAPI](http://gemstonepriceutkarshgaikwad-env.eba-7zp3wapg.ap-south-1.elasticbeanstalk.com/predictAPI)

# Postman Testing of API :

![API Prediction](./Screenshots/APIPrediction.jpg)

# Approach for the project 

1. Data Ingestion : 
    * In Data Ingestion phase the data is first read as csv. 
    * Then the data is split into training and testing and saved as csv file.

2. Data Transformation : 
    * In this phase a ColumnTransformer Pipeline is created.
    * for Numeric Variables first SimpleImputer is applied with strategy median , then Standard Scaling is performed on numeric data.
    * for Categorical Variables SimpleImputer is applied with most frequent strategy, then ordinal encoding performed , after this data is scaled with Standard Scaler.
    * This preprocessor is saved as pickle file.

3. Model Training : 
    * In this phase base model is tested . The best model found was catboost regressor.
    * After this hyperparameter tuning is performed on catboost and knn model.
    * A final VotingRegressor is created which will combine prediction of catboost, xgboost and knn models.
    * This model is saved as pickle file.

4. Prediction Pipeline : 
    * This pipeline converts given data into dataframe and has various functions to load pickle files and predict the final results in python.

5. Flask App creation : 
    * Flask app is created with User Interface to predict the gemstone prices inside a Web Application.

# Exploratory Data Analysis Notebook

Link : [EDA Notebook](./notebook/1_EDA_Gemstone_price.ipynb)

# Model Training Approach Notebook

Link : [Model Training Notebook](./notebook/2_Model_Training_Gemstone.ipynb)

# Model Interpretation with LIME 

Link : [LIME Interpretation](./notebook/3_Explainability_with_LIME.ipynb)
