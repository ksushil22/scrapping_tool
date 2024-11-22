# **FastAPI Product Scraping Tool**

This tool is a web scraper built using **FastAPI** that extracts product information (name, price, and image) from paginated e-commerce catalogs. It stores the scraped data locally in JSON format. The application supports proxy configuration, pagination and caching to optimize performance.

## **Installation**

### **Prerequisites**

1. Python 3.8 or higher.
2. Recommended: Virtual environment (e.g., `venv` or `conda`).

### **Setup Instructions**

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/scraping-tool.git
   cd scraping-tool
   ```
2. Create and activate a virtual environment:
    ```
    python -m venv env
    source env/bin/activate    # For Linux/macOS
    env\Scripts\activate       # For Windows
    ```
3. Install dependencies
    ```
    pip install -r requirements.txt
    ```


### **Usage**

1. Run the Application
    ```bash
    uvicorn app.main:app
    ```
2. Send API request:
    ```
    curl -X POST "http://127.0.0.1:8000/scrape/" \
    -H "Authorization: Bearer STATIC_SECURE_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://dentalstall.com/shop/",
      "page_limit": 5,
      "proxy": {}
    }'
    ```

### **Reponse**

1. On Success:
    ```
      {
        "message": "Scraping completed successfully.",
        "products_scraped": 120
      }
    ```
2. On failure:
    ```
    {
      "error": "Failed to fetch the URL. Please check your input."
    }
    ```

