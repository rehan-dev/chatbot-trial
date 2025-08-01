#  Chatbot with Memory & Authentication

- FastAPI
- Authentication pyJWT
- SQLite
- OPENAI API (for AI response)
- Conversation and each conversation have messages

### .env
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_KEY=your-openai-key

### RUN
docker compose up -d