import sys
import subprocess
import argparse

def resolve_ip_addresses(input_file, output_file=None, port=None, protocol=None):
    """Reads a file, resolves each IP address to a hostname, and prints results to stdout and optionally writes to an output file."""
    results = []

    try:
        with open(input_file, 'r') as file:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    try:
                        # Call the `host` command to perform reverse DNS lookup
                        result = subprocess.run(['host', ip_address], capture_output=True, text=True)
                        if result.returncode == 0:
                            output_lines = result.stdout.split('\n')
                            for output_line in output_lines:
                                if 'domain name pointer' in output_line:
                                    hostname = output_line.split(' ')[-1].strip('.')
                                    break
                            else:
                                hostname = "Could_not_resolve_hostname"
                        else:
                            hostname = "Could_not_resolve_hostname"

                        # Format output with optional port and protocol
                        port_part = f":{port}" if port else ""
                        protocol_part = f"/{protocol}" if protocol else ""
                        formatted_output = f"{ip_address}{port_part}{protocol_part} ({hostname})"
                        results.append(formatted_output)

                    except Exception as e:
                        results.append(f"An error occurred while resolving {ip_address}: {e}")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Print results to stdout
    for result in results:
        print(result)

    # Write results to output file if provided
    if output_file:
        try:
            with open(output_file, 'w') as file:
                for result in results:
                    file.write(result + '\n')
        except Exception as e:
            print(f"An error occurred while writing to the file '{output_file}': {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolve IP addresses to hostnames.")
    parser.add_argument('-i', '--input', required=True, help="Input file containing IP addresses.")
    parser.add_argument('-o', '--output', help="Optional output file to write resolved hostnames.")
    parser.add_argument('-p', '--port', type=int, help="Optional port number to include in the output.")
    parser.add_argument('-P', '--protocol', help="Optional protocol to include in the output.")

    args = parser.parse_args()

    resolve_ip_addresses(args.input, args.output, args.port, args.protocol)
