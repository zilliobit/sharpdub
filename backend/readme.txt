 uvicorn main:app --reload 
 uvicorn main:app --host localhost --port 8000 --reload
 uvicorn main:app --host 127.0.0.1 --port 8000 --reload //for API to work
alembic init -t async migrations
alembic revision --autogenerate -m "create todos table"
alembic upgrade head
netstat -ano | findstr :3000
taskkill /PID <PID> /F
 http://localhost:8000/docs


 Client (Nuxt)
 ├─ Generates DPoP keypair (WebCrypto)
 ├─ Login request + DPoP proof
 ├─ Receives cookies:
 │    - access_token (HttpOnly, Secure)
 │    - refresh_token (HttpOnly, Secure)
 │    - csrf_token (Readable)
 └─ For every request:
      - Cookies auto-attached
      - Fresh DPoP proof header
      - X-CSRF-Token header

Server (FastAPI)
 ├─ Validates DPoP proof
 ├─ Verifies cnf thumbprint binding
 ├─ CSRF validation
 ├─ Redis session validation
 └─ Executes business logic