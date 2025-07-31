# import csv
# import tldextract

# # File paths
# input_csv = "/home/zsroot/Deepak/main domian/input_domains.csv"  # Replace with the name of your input CSV
# output_csv = "/home/zsroot/Deepak/main domian/output_main_domains.csv"  # Replace with the name of your output CSV

# # Function to extract the main domain
# def extract_main_domain(domain):
#     # Remove any port numbers or paths
#     domain = domain.split(":")[0].split("/")[0]
#     extracted = tldextract.extract(domain)
#     return f"{extracted.domain}.{extracted.suffix}"

# # Set to store unique main domains
# unique_domains = set()

# # Read domains from the input CSV and write only unique main domains to the output CSV
# with open(input_csv, mode="r", newline="", encoding="utf-8") as infile, \
#      open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
    
#     csv_reader = csv.reader(infile)
#     csv_writer = csv.writer(outfile)

#     # Write header to the output CSV
#     header = next(csv_reader)  # Read the header row
#     if "Main Domain" not in header:
#         header.append("Main Domain")  # Add a new column for main domains
#     csv_writer.writerow(header)
    
#     # Process each row
#     for row in csv_reader:
#         # Assuming the domain is in the first column, update the column index as needed
#         domain_column_index = 0
#         domain = row[domain_column_index]
#         main_domain = extract_main_domain(domain)
        
#         # Only process unique domains
#         if main_domain not in unique_domains:
#             unique_domains.add(main_domain)  # Add domain to the unique set
#             row.append(main_domain)  # Append the extracted main domain
#             csv_writer.writerow(row)  # Write the row with the unique main domain

# print(f"Unique main domains have been written to {output_csv}")



import csv
import tldextract
import requests  # To handle URL requests and check redirection

# File paths
input_csv = "/home/zsroot/Deepak/main domian/input_domains.csv"  # Replace with the name of your input CSV
output_csv = "/home/zsroot/Deepak/main domian/output_main_domains.csv"  # Replace with the name of your output CSV

# Function to extract the main domain
def extract_main_domain(domain):
    # Remove any port numbers or paths
    domain = domain.split(":")[0].split("/")[0]
    extracted = tldextract.extract(domain)
    return f"{extracted.domain}.{extracted.suffix}"

# Function to check redirection and get the final URL
def check_redirection(domain):
    try:
        # Send a HEAD request to check redirection
        response = requests.head(domain, allow_redirects=True, timeout=10)
        if response.url != domain:  # If URL alters, redirection occurred
            return response.url
        else:
            return domain  # No redirection detected
    except requests.RequestException as e:
        print(f"Error checking redirection for {domain}: {e}")
        return domain  # Return the original domain in case of an error

# Set to store unique main domains
unique_domains = set()

# Read domains from the input CSV and write only unique main domains to the output CSV
with open(input_csv, mode="r", newline="", encoding="utf-8") as infile, \
     open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
    
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    # Write header to the output CSV
    header = next(csv_reader)  # Read the header row
    if "Main Domain" not in header:
        header.append("Main Domain")  # Add a new column for main domains
    if "Final Redirected URL" not in header:
        header.append("Final Redirected URL")  # Add a column for redirected URLs
    csv_writer.writerow(header)
    
    # Process each row
    for row in csv_reader:
        # Assuming the domain is in the first column, update the column index as needed
        domain_column_index = 0
        domain = row[domain_column_index]
        
        # Extract the main domain
        main_domain = extract_main_domain(domain)
        
        # Check for redirection
        redirected_url = check_redirection(domain)
        redirected_main_domain = extract_main_domain(redirected_url)  # Extract main domain from the redirected URL
        
        # Update main domain if redirection leads to a different domain
        final_domain_to_store = redirected_main_domain if redirected_main_domain != main_domain else main_domain
        
        # Only process unique domains
        if final_domain_to_store not in unique_domains:
            unique_domains.add(final_domain_to_store)  # Add domain to the unique set
            row.append(final_domain_to_store)  # Append the extracted main domain
            row.append(redirected_url)  # Append the final redirected URL
            csv_writer.writerow(row)  # Write the row with both main domain and redirection

print(f"Unique main domains and redirection details have been written to {output_csv}")