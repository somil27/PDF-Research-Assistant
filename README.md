# PDF Research Assistant - Advanced RAG Application

A modern, full-stack AI-powered PDF research assistant built with Next.js, FastAPI, and Supabase. Upload PDFs, ask questions, and get AI-generated answers with source citations.

## 🎯 Features

- **PDF Upload & Processing**: Drag-and-drop interface with automatic text extraction
- **AI Chat Interface**: Real-time streaming responses with conversation memory
- **Vector Search**: Semantic similarity search across multiple PDFs using Supabase pgvector
- **Source Citations**: See which PDFs and pages were used to generate answers
- **Document Management**: Upload, view, and manage your PDF documents
- **Chat History**: Persistent conversation history across sessions
- **Dark Mode**: Beautiful dark/light theme support
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🏗️ Architecture

```
frontend/          → Next.js 14 + TypeScript + Tailwind CSS
backend/           → FastAPI + LangChain + OpenAI
shared/            → Shared types and utilities
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase account
- OpenAI API key

### Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/somil27/PDF-Research-Assistant.git
cd PDF-Research-Assistant
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Run migrations
python migrate.py

# Start server
uvicorn main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
cd ../frontend
npm install

# Copy environment variables
cp .env.example .env.local

npm run dev
```

Visit `http://localhost:3000` to access the application.

## 📖 API Documentation

### Backend Endpoints

- `POST /api/upload` - Upload a PDF file
- `POST /api/chat` - Send a message and get AI response
- `GET /api/documents` - List uploaded documents
- `DELETE /api/documents/{id}` - Delete a document
- `POST /api/search` - Semantic search across documents

See `backend/README.md` for detailed API documentation.

## 🔧 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
DATABASE_URL=your_database_url
```

## 💾 Database Schema

The application uses Supabase PostgreSQL with pgvector extension:

- `documents` - Store PDF metadata
- `document_chunks` - Store text chunks with embeddings
- `conversations` - Store conversation sessions
- `messages` - Store chat messages

See `backend/migrations/` for schema details.

## 🤖 RAG Pipeline

1. **PDF Upload** → Extract text using PyPDF2
2. **Chunking** → Recursive text splitting with overlap
3. **Embeddings** → Generate using OpenAI text-embedding-3-small
4. **Vector Storage** → Store in Supabase pgvector
5. **Retrieval** → Semantic similarity search
6. **Generation** → GPT-4-turbo generates response with context
7. **Streaming** → Stream response token-by-token to frontend

## 📱 UI Components

Built with shadcn/ui and Tailwind CSS:
- Upload area with drag-and-drop
- Chat interface with message history
- Document sidebar
- Chat history panel
- Loading skeletons
- Markdown rendering
- Syntax highlighting

## 🛠️ Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- React Query
- Zustand (state management)

### Backend
- FastAPI
- LangChain
- OpenAI API
- Supabase Python client
- PyPDF2
- Uvicorn

### Infrastructure
- Supabase (PostgreSQL + pgvector)
- OpenAI GPT-4-turbo & Embeddings
- Docker (optional)

## 📝 Project Structure

```
PDF-Research-Assistant/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── chat/
│   │   └── documents/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── models/
│   ├── migrations/
│   ├── requirements.txt
│   └── .env.example
├── shared/
│   └── types.ts
└── README.md
```

## 🚢 Deployment

### Frontend (Vercel)
```bash
vercel deploy
```

### Backend (Railway/Render/Heroku)
```bash
# Push to your hosting provider
```

## 📚 Documentation

- [Frontend Setup](./frontend/README.md)
- [Backend Setup](./backend/README.md)
- [API Documentation](./backend/docs/API.md)
- [Database Schema](./backend/docs/DATABASE.md)
- [RAG Pipeline Guide](./backend/docs/RAG_PIPELINE.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT and embedding models
- Supabase for PostgreSQL and pgvector
- Vercel for Next.js framework
- shadcn/ui for beautiful components

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Built with ❤️ as a portfolio project showcasing full-stack AI/ML development
