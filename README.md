

# GovernomicsCR Project

This repository contains both the backend (FastAPI) and frontend (Next.js) for the GovernomicsCR application. 

This study introduces GovernomicsCR, an AI driven analytical system designed to examine and compare Costa Rica’s economic growth across presidential administrations. The system integrates structured datasets, a multi agent pipeline orchestrated with LangGraph, Langchain, and a FastAPI backend for automated report generation. Additionally, a React based frontend using the shadcnui component library provides an interactive interface that allows users to formulate queries, select predefined questions, and receive structured analytical outputs. 

GovernomicsCR processes historical GDP data, synthesizes sectoral, industrial, regime based, and expenditure related indicators, and produces coherent analytical reports. The results show the feasibility of using large language models to support economic monitoring and policy analysis.

---


## 1. Project Structure


### Backend (`be_government`)

- `.env`: Environment variables (not tracked by Git)
- `requirements.txt`: Python dependencies
- `app/`:
  - `agents/`
  - `api/`
  - `clients/`
  - `core/`
  - `data/`
  - `models/`
  - `pipelines/`
  - `prompts/`
  - `services/`
  - `utils/`

### Frontend (`fe_government`)
- [Next.js](https://nextjs.org) project bootstrapped with `create-next-app`
- `app/`: Main pages and components
- `assets/`: Static resources (CSS, images, etc.)
- `notebooks/`: Jupyter notebooks for analysis
- `scripts/`: Utility scripts
- `data/`: Frontend data files

---

## 2. Installation & Setup

### Backend
#### 2.1. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```
#### 2.2. Install dependencies
```bash
pip install -r requirements.txt
```
#### 2.3. Configure environment variables
Create a `.env` file in the root of `be_government` with:
```
GROQ_API_KEY="your_groq_api_key"
OPENAI_API_KEY="your_openai_api_key"
```
#### 2.4. Run the backend
```bash
uvicorn app.main:app --reload
```

### Frontend
#### 2.1. Install dependencies
```bash
cd fe_government
npm install
```
#### 2.2. Run the frontend
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser to view the app.

---

## 3. Usage & Development

### Backend
- Entry point: `main.py`
- Modify logic in `app/` and add services, agents, or endpoints as needed
- Run tests in `tests/`

### Frontend
- Edit pages in `app/page.tsx` or components in `app/`
- Changes are reflected automatically in the browser

---

## 4. Resources & Documentation

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)

### Frontend
- [Next.js Documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
- [Next.js GitHub](https://github.com/vercel/next.js)

---

## 5. Deployment

### Backend
- Run locally using Uvicorn (see above)
- For production, deploy using your preferred Python hosting solution

### Frontend
- The easiest way to deploy Next.js is on [Vercel](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme)
- See [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying)

