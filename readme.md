# OLX Price Search

## Description
This project is a web scraper that searches and compares product prices on OLX, presenting the results in a user-friendly web interface.

## Features
- Product search by name
- Display of maximum, minimum, and average price
- List of ads with direct links
- Interactive web interface using Gradio

## Running with Docker Compose
You can also run the project using Docker Compose. Follow the steps below:

1. Make sure you have Docker and Docker Compose installed on your machine.
2. Navigate to the project directory:
    ```bash
    cd OLX-Price-Search
    ```
3. Build and start the containers:
    ```bash
    docker-compose up --build
    ```
4. After the build completes, run:
    ```bash
    docker-compose up -d
    ```
5. Access the address http://localhost:7878/

## Technologies Used
- Python
- Selenium
- Gradio
- Docker
- Chrome Webdriver

## How to Use
1. Clone the repository:
    ```bash
    git clone https://github.com/alex-des-santos/OLX-Price-Search.git
    ```
2. Navigate to the project directory:
    ```bash
    cd OLX-Price-Search
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the main script:
    ```bash
    python main.py
    ```
5. Access the address http://localhost:7878/

## Contributing
1. Fork the project
2. Create a branch for your feature:
    ```bash
    git checkout -b my-feature
    ```
3. Commit your changes:
    ```bash
    git commit -m 'My new feature'
    ```
4. Push to the remote repository:
    ```bash
    git push origin my-feature
    ```
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Limitations and Future Improvements
- **Error Handling:** The scraper could be improved with more robust error handling to gracefully manage situations like network issues or changes in OLX's website structure.
- **Scalability:** Currently, the scraper might not be optimized for handling a very large number of searches concurrently. Future improvements could focus on improving scalability and performance.
- **Data Persistence:** Consider adding a mechanism to persist scraped data for offline access or analysis.
- **Advanced Search Options:** Expanding search capabilities to include filters (e.g., price range, location) would enhance the user experience.
