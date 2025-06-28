#  ASKARI: A Multi-Agent AI Support Chatbot

ASKARI is a modular, multi-agent AI chatbot built to assist internal departments like HR and IT using LangGraph for LLM orchestration and FastAPI + React for full-stack communication. The system dynamically routes queries using an LLM classifier and merges agent responses into a final reply using LangGraph.

---

##  Features

-  Full-stack architecture: React frontend + FastAPI backend
-  Modular agents: HR & IT (plug-and-play architecture)
-  Smart LLM routing via LangGraph
-  Observability using Langfuse
-  RAG-ready design for document retrieval per agent

---

##  Tech Stack

| Layer      | Stack                         |
|------------|-------------------------------|
| Frontend   | React     |
| Backend    | FastAPI, LangGraph            |
| LLM Access | OpenRouter + DeepSeek         |
| Monitoring | Langfuse                      |
| Deployment | GitHub + Uvicorn + Docker-ready (optional) |

---

##  Project Structure

```
LANXESS/
├── backend/
│   └── Askari/
│       ├── main.py                # FastAPI entrypoint
│       ├── agent_registry.py      # Registry for plug-in agents
│       ├── langraph_builder.py    # LangGraph flow orchestration
│       ├── llm_client.py          # LLM client (OpenRouter)
│       ├── agent_state.py         # Shared agent state
│       ├── requirements.txt       # Python dependencies
│       ├── .env                   # Secret config file
│       └── venv/                  # Python virtual environment (ignored)
├── frontend/
│   └── askari-frontend/
│       ├── src/                   # React app source
│       ├── public/                # Static files
│       ├── .env                   # Frontend config
│       └── package.json           # Node dependencies
└── README.md
```

---

##  Requirements

-  Python 3.10
-  Node.js 18+

---

##  1. Clone & Setup

```bash
git clone https://github.com/aniruddh1297/Askari-multi-agent-chatbot.git
cd Askari-multi-agent-chatbot
```

---

##  2. Backend Setup (FastAPI)

```bash
cd backend/Askari
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

###  `.env` Configuration (`backend/Askari/.env`)

```env
OPENROUTER_API_KEY=''
LLM_MODEL=''
LANGFUSE_SECRET_KEY=''
LANGFUSE_PUBLIC_KEY=''
LANGFUSE_HOST=https://cloud.langfuse.com
```

###  `.env` Configuration (`frontend/askari-frontend/.env`)

```env
VITE_BACKEND_URL= BACKEND URL
```

>  Make sure your Langfuse and OpenRouter keys are valid and billing is active if needed.

---

##  3. Frontend Setup (React)

```bash
cd frontend/askari-frontend
npm install
```

##  4. Run the Application

###  Start Backend (with LangGraph)

```bash
cd backend/Askari
uvicorn main:app --reload
```

###  Start Frontend (React)

```bash
cd frontend/askari-frontend
npm run dev
```

Visit: [http://localhost:5173](http://localhost:5173)

---

## 🐳 Docker Deployment

### 🔧 Build & Run Backend (FastAPI)

```bash
# From project root
docker build -t askari-backend -f backend/Askari/Dockerfile .

# Run backend container on port 8000
docker run -d -p 8000:8000 --name askari-backend askari-backend
```

📍 Access API at: [http://localhost:8000](http://localhost:8000)

---

### 🎨 Build & Run Frontend (React/Vite)

```bash
# Navigate to frontend directory
cd frontend/askari-frontend

# Build frontend Docker image
docker build -t askari-frontend .

# Run frontend container on port 3000
docker run -d -p 3000:80 --name askari-frontend askari-frontend
```

📍 Access UI at: [http://localhost:3000](http://localhost:3000)

---

### 🔐 Environment Variables

For local development:

- **Backend** uses: `backend/Askari/.env`
- **Frontend** uses: `frontend/askari-frontend/.env`

For Dockerized deployment:

- Inject env variables using `--env-file`:

```bash
# Run backend with .env file
docker run --env-file backend/Askari/.env -p 8000:8000 askari-backend
```
##  Key Highlights

-  **LLM Router**: DeepSeek-powered OpenRouter route classifier
-  **Agents**: HR & IT with modular logic (more can be added)
-  **LangGraph Flow**: Handles agent calls, merging, fallback
-  **Monitoring**: All calls are logged to Langfuse dashboard
-  **RAG Ready**: Integrate ChromaDB or FAISS per agent

---

##  Future Enhancements

-  RAG for each agent via PDF ingestion
-  Admin dashboard for agent management
-  Docker-based deployment (planned)
-  GitHub Actions CI/CD setup
-  Multi-language support

---

## Learnings

- LangGraph orchestration of multi-agent flows
- Smart fallback handling and LLM-based routing
- Seamless tracing using Langfuse
- FastAPI + React integration for full-stack AI apps

---

##  License

MIT — Feel free to use and extend with attribution.

---

##  Author

Made with by **Aniruddh Sahukar Srinivas**
