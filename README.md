# Buddy 🚀

## Description

Buddy is your new AI friend 🤗. It has started as a project to be a `Code Buddy` i.e. It will read existing source code 👩‍💻 and allow the developers to ask questions about the code and even help in creating a `Code Change Plan`.

👉 **Note** : As of now `Buddy` only works with `JavaScript` code.

## How it works?

-   It uses `Python` 🐍
-   It uses `tree_sitter` to parse the code.
-   Then it creates a `call graph` for the code using `Networkx`.
-   It then uses `Gemini` as `LLM`.
-   It has an **intelligent** mode where it uses `LangChain` and `Chroma` to save the `Google AI Embeddings` locally to filter `call graph` for the user query before sending it to `Gemini`.

## Why LangChain and Chroma?

-   LangChain and Chroma are used to save the `Google AI Embeddings` locally to filter `call graph`
-   This is done to reduce the `LLM` usage and make `Buddy` efficient.

## Setup Instructions

👉 **Note**: Python 3.12.8 or latter is required.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yadavanuj/buddy.git
    cd buddy
    ```

2. **Create a `.env` file:**

    - In the `buddy` directory, create a file named `.env`.
    - Add the following line to the `.env` file:
        ```
        GEMINI_KEY=your_gemini_key_here
        ```

3. **Install dependencies:**

    - Make sure to install any required dependencies for the project.
        ```
        .\venv\Scripts\activate
        pip install -r requirements.txt
        ```

4. **Run the application:**
    - Follow the instructions to run the application.

## Usage

-   The CLI provides two major commands
    -   code - To create change plan
    -   refresh - To refresh NLTK dependencies and/or Chroma embeddings.
-   `/buddy/viewer` directory uses `Node JS`, `D3` and `Marked` to help you visualize the output.

👇 Call Graph

![alt text](assets/call_graph.png)

👇 Code Change Plan

![alt text](assets/change_plan.png)

## Note

-   Ensure that the `.env` file is included in your `.gitignore` to prevent it from being pushed to the repository.
