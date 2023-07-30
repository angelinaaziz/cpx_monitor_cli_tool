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
git clone https://github.com/angelinaaziz/cpx-monitor.git
cd cpx-monitor
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

This README provides an overview of the CPX Monitor tool and explains how to use it. It also covers the features, testing, contribution guidelines, and Dockerization. Please modify this README as needed to fit your project's specifics.