# Quickstart: RAG Frontend Integration

**Feature**: `009-rag-frontend-docusaurus-integration`

This guide provides instructions on how to set up and run the Docusaurus frontend with the integrated RAG chat widget.

## Prerequisites

1.  **Node.js and npm**: Ensure Node.js (LTS version recommended) and npm (or yarn) are installed.
2.  **FastAPI RAG Backend**: The backend from `008-rag-agent-openai-fastapi` must be running and accessible. Refer to its `quickstart.md` for instructions on how to start it.
    -   **Local Development**: Typically runs on `http://127.0.0.1:8000`.
    -   **Deployed Backend**: Use the URL of your deployed instance.
3.  **Docusaurus Dependencies**: Install Docusaurus project dependencies.
    ```bash
    cd <project_root>
    npm install
    # or yarn install
    ```

## Configuration

The frontend needs to know the URL of the FastAPI backend. This can be configured via Docusaurus environment variables.

1.  **Create/Edit `.env` file**: In the root of your Docusaurus project (e.g., `C:\Users\bisma\Desktop\Spec-Driven-Development-hackathon`), create or edit a `.env` file and add the following:

    ```
    REACT_APP_FASTAPI_BASE_URL=http://127.0.0.1:8000
    ```
    Replace `http://127.0.0.1:8000` with the actual URL of your running FastAPI backend.

2.  **Accessing in Docusaurus**: This environment variable will be accessible in your React components as `process.env.REACT_APP_FASTAPI_BASE_URL`.

## Running the Docusaurus Frontend

1.  **Start the FastAPI Backend**: Ensure your FastAPI RAG agent backend is running as per its quickstart guide.
2.  **Navigate to Docusaurus Root**: Open your terminal and navigate to the root directory of this Docusaurus project.
3.  **Start Development Server**: Run the Docusaurus development server:

    ```bash
    npm start
    # or yarn start
    ```

    This will open your Docusaurus website in your browser (usually `http://localhost:3000`).

## Interacting with the Chat Widget

Once the Docusaurus site is running:

1.  Navigate to the page where the `ChatWidget` component is embedded.
2.  Type a question into the chat input field.
3.  Press Enter or click the send button.
4.  Observe the agent's response, which should be grounded in the book content.
