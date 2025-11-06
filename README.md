# be_governments Backend Project

This project provides a robust FastAPI backend for the governments application.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
2.  **Activate the virtual environment:**
    *   Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a .env file:**
    Create a `.env` file in the root of the `be_governments` directory and add the following variables:
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_groq_api_key_here"` and `"your_openai_api_key_here"` with your actual API keys.

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Project Structure

-   `app/`: Core application logic
    -   `core/`: Core configurations and utilities
    -   `services/`: Business logic and external API integrations
    -   `clients/`: Clients for external services (e.g., Groq)
-   `tests/`: Unit and integration tests
-   `requirements.txt`: Python dependencies
-   `pandasai.log`: Log file for PandasAI operations
-   `script.py`: Example script for data processing or specific tasks
-   `test.py`: Testing script for various functionalities
-   `main.py`: Main FastAPI application entry point
-   `.env`: Environment variables (ignored by Git)
-   `Dockerfile`: (Optional) For Docker containerization
