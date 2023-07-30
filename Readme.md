 <!-- Table of Contents -->
 <details>
<summary>Table of Contents</summary>
<ol>
<li><a href="#about-the-project">About The Project</a></li>
<li><a href="#getting-started">Getting Started</a>
    <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#running-in-docker">Running in Docker</a></li>
        <li><a href="#running-locally">Running Locally</a></li>
    </ul>
</li>
<li><a href="#features">Features</a>
    <ul>
        <li><a href="#print-service-data">Print Service Data</a></li>
        <li><a href="#flag-services">Flag Services</a></li>
        <li><a href="#compute-average-service-data">Compute Average Service Data</a></li>
        <li><a href="#average-service-data">Average Service Data</a></li>
    </ul>
</li>
<li><a href="#testing">Testing</a></li>
<li><a href="#choices-made">Choices Made</a></li>
<li><a href="#trade-offs">Trade-offs</a></li>
<li><a href="#future-improvements">Future Improvements</a></li>
</ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
CPX Monitor is a command-line tool designed to monitor the health of services running on multiple servers. It provides information about the CPU and memory usage of each service and flags services that have only one healthy instance. The tool interacts with a backend API to retrieve server and service data.

### Prerequisites
Before running CPX Monitor, make sure you have the following installed:

- Docker (if you want to run the tool inside a Docker container)

### Running in Docker
This would be the recommended way to run the tool. To run the tool in Docker, follow the steps below:

1. Build the Docker image
```sh
docker-compose build
```

2. Run the Docker container
```sh
 docker-compose run --service-ports cpx_monitor
```

### Running locally
1. Clone the repository to your local machine
```sh
git clone https://github.com/angelinaaziz/cpx-monitor_cli_tool.git
cd cpx-monitor_cli_tool
```

2. Install the required dependencies
```sh
pip install -r requirements.txt
```

3. Run the CPX monitor tool
```sh
python cpx_monitor.py --host localhost --port 8080 --interval 5
```
Replace the --host, --port, and --interval options with the appropriate values. The --host option specifies the backend API host, --port specifies the port number, and --interval specifies the time interval (in seconds) between data fetches.

<!-- FEATURES -->
## Features

### Print service data
The print_service_data function prints the CPU and memory usage of services running on specified servers. It fetches data from the backend API and displays the information in tabular form.

### Flag services
The flag_services function checks the health status of services on the servers. If a service has only one healthy instance, it will be flagged with a warning message. This function uses the avg_service_data function to calculate the average CPU and memory usage for each service.

### Compute average service data
The compute_avg_service_data function calculates the average CPU and memory usage for each service based on the data retrieved from the backend API.

### Average service data
The avg_service_data function displays the average CPU and memory usage for each service in tabular form. It calls compute_avg_service_data to get the average data.

### Testing
The test_cpx_monitor.py file contains unit tests for the CPX Monitor tool. To run the tests, use the following command:
```sh
python -m unittest test_cpx_monitor.py
```
The test suite includes several test cases to verify the functionality of the CPX Monitor tool.

## Choices Made
- **Python**: Python was chosen as the programming language due to its simplicity, ease of use, and availability of libraries for making HTTP requests and parsing JSON data.

- **Requests**: The Requests library was used to make HTTP requests to the backend API. It is a simple and elegant library that provides a high-level interface for making HTTP requests.

- **Command-line Interface**: The tool is designed to be run from the command line, making it convenient for administrators to monitor the CPX environment without the need for a graphical interface.

- **Docker**: The tool is packaged as a Docker container to simplify the installation process and ensure that it runs consistently across different environments.

- **Mocking**: Unit tests use the `unittest.mock` library to mock server responses, ensuring that the tests are independent of the actual server data.

## Trade-offs
- **Real-time Data**: The tool fetches data from the CPX servers at the time of execution. For real-time monitoring, the tool needs to be executed at regular intervals.

- **Error Handling**: The tool currently assumes that the CPX servers will respond with the expected data format. More robust error handling and data validation could be implemented for production use.

- **Data Storage**: The tool does not store any data. For historical data analysis, the tool would need to be modified to store the data in a database.

- **Scalability**: The tool is designed to monitor a small number of servers. For larger deployments, the tool would need to be modified to handle a larger number of servers and services.

## Future Improvements
- **Logging**: Add logging functionality to record important events and errors, providing better visibility into the tool's behavior.

- **Authentication**: Implement secure authentication mechanisms, such as API tokens or OAuth, to access the CPX servers securely.

- **Web Interface**: Develop a web-based interface to visualize the service data, historical trends, and health status.

- **Alerting System**: Integrate an alerting system to notify administrators when services become unhealthy or resource usage exceeds defined thresholds.

- **Continuous Integration**: Set up a continuous integration (CI) system to automatically run tests whenever changes are pushed to the repository.

---
This README provides an overview of the CPX Monitor project, how to run it, its features, testing, choices made during development, trade-offs, and potential future improvements.