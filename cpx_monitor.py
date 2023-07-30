import argparse
import requests
import time
import collections
import sys
from termcolor import colored
from prettytable import PrettyTable

def get_service_data(args, ip=None):
    url = f'http://{args.host}:{args.port}'  # Use 'args.host' as the hostname
    if ip is not None:
        url = f'{url}/{ip}'
    else:
        url = f'{url}/servers'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as errh:
        print("❌ Http Error:", errh)
        return {}
    except requests.exceptions.ConnectionError as errc:
        print("❌ Error Connecting:", errc)
        return {}
    except requests.exceptions.Timeout as errt:
        print("❌ Timeout Error:", errt)
        return {}
    except requests.exceptions.RequestException as err:
        print("❌ Other error occurred:", err)
        return {}
    return data

def print_service_data(args, servers):
    table = PrettyTable(["IP", "Service", "CPU", "Memory", "Status"])
    for server in servers:
        server_data = get_service_data(args, server)
        cpu = int(server_data['cpu'].strip('%'))
        mem = int(server_data['memory'].strip('%'))
        if cpu < 80 and mem < 80:
            status = colored('✅ Healthy', 'green')
        else:
            status = colored('❌ Unhealthy', 'red')
        table.add_row([server, server_data['service'], server_data['cpu'], server_data['memory'], status])
    print(table)

def print_avg_service_data(avg_data):
    table = PrettyTable(["Service", "Average CPU", "Average Memory"])
    for service, (avg_cpu, avg_mem) in avg_data.items():
        table.add_row([service, f'{avg_cpu}%', f'{avg_mem}%'])
    print(table)

def track_services(args):
    while True:
        try:
            service_stats = get_service_data(args)
            if service_stats is None:
                print("❌ Couldn't connect to the CPX server. Please check if it's running.")
                return
            service_data = {ip: get_service_data(args, ip) for ip in service_stats}
            print_service_data(service_data)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("❗ Stopped tracking services.")
            break

def compute_avg_service_data(service_data):
    service_info = collections.defaultdict(lambda: ([], []))
    for ip, data in service_data.items():
        cpu = int(data['cpu'].strip('%'))
        mem = int(data['memory'].strip('%'))
        service_info[data['service']][0].append(cpu)
        service_info[data['service']][1].append(mem)
    avg_data = {service: (sum(cpus) / len(cpus), sum(mems) / len(mems)) for service, (cpus, mems) in service_info.items()}
    return avg_data

def avg_service_data(args):
    service_stats = get_service_data(args)
    if service_stats is None:
        print("❌ Couldn't connect to the CPX server. Please check if it's running.")
        return
    service_data = {}
    for ip in service_stats:
        try:
            data = get_service_data(args, ip)
            service_data[ip] = data
        except StopIteration:
            # If get_service_data raises StopIteration, it means the IP has no data
            # We'll skip it and move on to the next IP
            pass
    avg_data = compute_avg_service_data(service_data)
    table = PrettyTable(["Service", "Average CPU", "Average Memory"])
    for service, (avg_cpu, avg_mem) in avg_data.items():
        table.add_row([service, f"{avg_cpu}%", f"{avg_mem}%"])
    print(table)
    print(colored('✅ Done!', 'green'))

def flag_services(args):
    service_stats = get_service_data(args)
    if service_stats is None:
        print("❌ Couldn't connect to the CPX server. Please check if it's running.")
        return

    # Count the number of healthy instances for each service
    service_health_counts = collections.defaultdict(int)
    for ip in service_stats:
        service_data = get_service_data(args, ip)
        if 'cpu' not in service_data or 'memory' not in service_data or 'service' not in service_data:
            continue  # Skip this iteration if any required key is missing
        cpu = int(service_data.get('cpu', '0%').strip('%'))
        mem = int(service_data.get('memory', '0%').strip('%'))
        if cpu < 80 and mem < 80:
            service_health_counts[service_data['service']] += 1

    # Flag services with fewer than 2 healthy instances
    unhealthy_services = []
    for service, count in service_health_counts.items():
        if count < 2:
            unhealthy_services.append(service)
            print(colored(f"❗ The service {service} has only {count} healthy instance(s).", 'yellow'))

    # Print a message if there are no unhealthy services
    if not unhealthy_services:
        print(colored("✅ All services have at least 2 healthy instances.", 'green'))

def main():
    parser = argparse.ArgumentParser(description='CPX Monitoring Tool')
    parser.add_argument('--host', type=str, default='localhost', help='Hostname of the CPX server.')
    parser.add_argument('--port', type=int, required=True, help='Port to connect to the CPX server.')
    parser.add_argument('--interval', type=int, default=2, help='Time interval (in seconds) at which to fetch and print data in "track_services" mode.')

    args = parser.parse_args()
    print(args)

    while True:
        try:  # Catching keyboard interrupt at a higher level
            print("\nPlease select an option:")
            print("1. Print running services to stdout.")
            print("2. Print out average CPU/Memory of services of the same type.")
            print("3. Flag services which have fewer than 2 healthy instances running.")
            print("4. Exit.")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                servers = get_service_data(args)
                if servers:
                    print_service_data(args, servers)
            elif choice == '2':
                avg_service_data(args)
            elif choice == '3':
                flag_services(args)  
            elif choice == '4':
                print("✨ Exiting the program.")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 4.")
        except KeyboardInterrupt:
            print("\n❗ Interrupted! Returning to the main menu.")

if __name__ == '__main__':
    main()