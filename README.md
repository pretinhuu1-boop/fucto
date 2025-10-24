# fucto Project Description

This project provides a FastAPI service compatible with the OpenAI API and includes an example script for directly testing the WebSocket interface.

## Project Structure

- `openai_api_server.py`: FastAPI implementation of a `/v1/chat/completions` compatible service, supporting round-robin polling of multiple Cookies and communication with CTO.NEW's backend service.
- `websocket_example.py`: Command-line interactive example demonstrating how to interact directly with the engine via HTTP + WebSocket and receive real-time responses.
- `requirements.txt`: List of third-party dependencies required for execution.
- `cookies.txt` (needs manual creation): Stores available Cookie strings, one per line. The service will automatically poll and use them.

## Quick Start

1.  **Environment Setup**
    -   Python 3.10+ is recommended.
    -   (Optional) Create and activate a virtual environment.
    -   Execute `pip install -r requirements.txt` to install dependencies.

2.  **Configure Cookies**
    -   Log in to the website, capture network traffic, find the request headers for https://clerk.cto.new/v1/client/sessions/sess..., and copy the cookies, starting with【__client=】
    -   Create `cookies.txt` in the project root directory.
    -   Write multiple Cookie strings into the file, one per line. Lines starting with `#` can be added as comments.
    -   Each request will automatically use a different Cookie in a round-robin fashion, achieving simple load balancing.

3.  **Start the API Service**
    ```bash
    python openai_api_server:app --host 0.0.0.0 --port 8000
    ```
    -   The FastAPI service will provide two main endpoints: `/v1/chat/completions` and `/v1/models`.
    -   The default response format is compatible with OpenAI Chat Completions and can be used directly by existing clients.

4.  **Run the WebSocket Example**
    ```bash
    python websocket_example.py
    ```
    -   On the first run, it will save `chat_id.txt` in the current directory, allowing you to choose whether to reuse or create a new conversation.
    -   Input messages according to the prompt to receive real-time model replies.

## FAQ

-   **Cookie Expiration**: If a 401 or 403 error occurs, update the entries in `cookies.txt` and save the file to continue use. No service restart is needed.
-   **Missing Dependencies**: Ensure the installation command is executed in the correct virtual environment; reinstall packages like `websockets`, `fastapi` if necessary.
