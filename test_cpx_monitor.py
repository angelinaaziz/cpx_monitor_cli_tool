import unittest
from unittest.mock import patch
from io import StringIO
import argparse
from cpx_monitor import print_service_data, flag_services, compute_avg_service_data, avg_service_data, print_avg_service_data

class TestCPXMonitor(unittest.TestCase):

    def test_print_service_data(self):
        args = argparse.Namespace(host='localhost', port=8080, interval=2)
        servers = ['10.58.1.1', '10.58.1.2', '10.58.1.3']

        # Example response data for servers
        server_data_1 = {
            'service': 'web',
            'cpu': '50%',
            'memory': '60%',
        }
        server_data_2 = {
            'service': 'db',
            'cpu': '90%',
            'memory': '70%',
        }
        server_data_3 = {
            'service': 'web',
            'cpu': '75%',
            'memory': '85%',
        }

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Mock get_service_data to return the example response data
            with patch('cpx_monitor.get_service_data', side_effect=[server_data_1, server_data_2, server_data_3]):
                print_service_data(args, servers)
                output = fake_out.getvalue()

        # Check if the output contains the expected values
        self.assertIn('10.58.1.1', output)
        self.assertIn('web', output)
        self.assertIn('50%', output)
        self.assertIn('60%', output)
        self.assertIn('✅ Healthy', output)
        self.assertIn('10.58.1.2', output)
        self.assertIn('db', output)
        self.assertIn('90%', output)
        self.assertIn('70%', output)
        self.assertIn('❌ Unhealthy', output)
        self.assertIn('10.58.1.3', output)
        self.assertIn('web', output)
        self.assertIn('75%', output)
        self.assertIn('85%', output)
        self.assertIn('❌ Unhealthy', output)

    def test_compute_avg_service_data(self):
        service_data = {
            '10.58.1.1': {
                'service': 'web',
                'cpu': '50%',
                'memory': '60%',
            },
            '10.58.1.2': {
                'service': 'db',
                'cpu': '90%',
                'memory': '70%',
            },
            '10.58.1.3': {
                'service': 'web',
                'cpu': '75%',
                'memory': '85%',
            },
        }
        avg_data = compute_avg_service_data(service_data)

        # Check if the average data is computed correctly
        self.assertIn('web', avg_data)
        self.assertAlmostEqual(avg_data['web'][0], 62.5)
        self.assertAlmostEqual(avg_data['web'][1], 72.5)
        self.assertIn('db', avg_data)
        self.assertAlmostEqual(avg_data['db'][0], 90.0)
        self.assertAlmostEqual(avg_data['db'][1], 70.0)

    def test_avg_service_data(self):
        # Update the test data to match the response data in the test method
        service_data = {
            '10.58.1.1': {
                'service': 'web',
                'cpu': '50%',
                'memory': '60%',
            },
            '10.58.1.2': {
                'service': 'web',
                'cpu': '70%',
                'memory': '80%',
            },
            '10.58.1.3': {
                'service': 'db',
                'cpu': '90%',
                'memory': '70%',
            },
        }
        avg_data = compute_avg_service_data(service_data)

        # Check if the average data is computed correctly
        self.assertIn('web', avg_data)
        self.assertAlmostEqual(avg_data['web'][0], 60.0)
        self.assertAlmostEqual(avg_data['web'][1], 70.0)
        self.assertIn('db', avg_data)
        self.assertAlmostEqual(avg_data['db'][0], 90.0)
        self.assertAlmostEqual(avg_data['db'][1], 70.0)

    def test_print_avg_service_data(self):
        avg_data = {
            'web': (62.5, 72.5),
            'db': (90.0, 70.0),
        }

        with patch('sys.stdout', new=StringIO()) as fake_out:
            print_avg_service_data(avg_data)
            output = fake_out.getvalue()

        # Check if the output contains the expected values
        self.assertIn('web', output)
        self.assertIn('62.5%', output)
        self.assertIn('72.5%', output)
        self.assertIn('db', output)
        self.assertIn('90.0%', output)
        self.assertIn('70.0%', output)

if __name__ == '__main__':
    unittest.main()