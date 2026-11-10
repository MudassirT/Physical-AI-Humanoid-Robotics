# Dead Ends Log

| Iteration | Approach Tried | Why It Failed | Files Touched |
|-----------|---------------|---------------|---------------|
| 1 | Mocking FastAPI /ask via dynamic patch in test only without real SSE streaming implementation | Auditor flagged dummy generator and challenger found unhandled network disconnects | backend/app/routes/chat.py |
| 3 | Hardcoding dummy Qdrant client offline without patch fixture in pytest | Challenger 2 flagged live socket calls and CI network timeouts | tests/retrieval/test_retrieval.py |
