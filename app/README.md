# Referrer Finder

## Setup Instructions

1. **Create a local `.env` file**  
    Containing values for all the variables used in `db.py`.

2. **Ensure Python Environment**  
    Make sure you're on a Python environment running Python version >= 3.10.

3. **Install Dependencies**  
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the App**  
    ```sh
    streamlit run main.py
    ```

## OR to run it with docker

1. **Make sure the `.env` file exists in root directory**

2. **Launch Docker on your local machine**

3. **Run the following command:**
   ```sh
   docker-compose --env-file .env up --build
   ```
