import os
import getopt
import sys
import warnings
import geoip2.database
import geoip2.errors
from duckduckgo_search import DDGS
import webtech
import requests
from bs4 import BeautifulSoup
import re
from text_blocks import *
import time
import random
from urllib.parse import urlparse
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

# Suppress RuntimeWarning from asyncio for Windows devices
warnings.filterwarnings("ignore")

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# DuckDuckGo Advanced Search - https://duckduckgo.com/duckduckgo-help-pages/settings/params/

GEOIP2_DATABASE_DIR = f"{os.getcwd().rstrip('/src')}/data/GeoLite2-Country.mmdb"
GEOIP_READER = geoip2.database.Reader(GEOIP2_DATABASE_DIR)
TARGET_COUNTRY = "RU"

TOP100_DIR = f"{os.getcwd().rstrip('/src')}data/top100/"


def verify_ip_origin_country(ip_addr, target_c):
    try:
        response = GEOIP_READER.country(ip_addr)
        if target_c == response.country.iso_code:
            return True
        else:
            return False
    except geoip2.errors.AddressNotFoundError:
        return False


def unpack_domains_from_txt(domain_file):
    domains = []

    with open(domain_file, 'r', newline='') as textfile:

        for row in textfile.readlines():
            domains.append(row.rstrip("\n"))

    return domains


def extract_domains(compiled_html):
    domains = []

    for html_block in compiled_html:
        try:
            # Find all the link-text span elements and extract text
            domain_element = html_block.find_all("span", class_="link-text")
            for element in domain_element:
                domains.append(element.text)

        # If no elements are found, continue to next html block
        except AttributeError:
            continue

    return domains


def clean_domain_names(domain_list):
    clean_domains = []
    # Go through each domain and apply urlparse function. netloc requires https:// prefix
    for domain in domain_list:
        clean_domains.append(urlparse(f"https://{domain}").netloc.replace("www.", ""))

    # Return the list without duplicate
    return list(set(clean_domains))


def generate_start_url(query, query_variables, url_variables):
    # Base URL
    base_url = r"https://lite.duckduckgo.com/lite/"

    # Dynamically generate the query from the dictionary
    for key, value in query_variables.items():
        if value is not None:
            query += f" {key}:{value} "

    custom_url = f"{base_url}?q={query}"

    # Add URL parameters
    for key, value in url_variables.items():
        if value is not None:
            custom_url += f"&{key}={value}"

    # TODO Consider URL encoding the URL fully
    custom_url = custom_url.replace(" ", "%20")
    return custom_url


# Translates query to desired language
def ddg_translate_query(query, lang):
    with DDGS() as ddgs:
        return [r for r in ddgs.translate(query, to=lang)][0]["translated"]


# Sends GET Request and Parses output to pull the HTML and
def ddg_get_request(search_query):

    # Random User-Agent
    user_agent = user_agent_rotator.get_random_user_agent()

    # Send GET request with user-agent or else it will return an error
    response = requests.get(search_query, headers={"User-Agent": user_agent})

    # Use BS4 html parser
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finds the unique form "next_form"
    url_form = soup.find('input', {'value': 'Next Page >'}).find_parent('form')

    # Checks if the form exists
    if url_form:
        # Finds the comment within the form
        comment = url_form.find(string=lambda text: isinstance(text, str) and 'Next Page' in text)

        # Uses regex to search for and match the url from the comment
        if comment:
            href_url = re.compile(r'<a\s.*?href="([^"]*)".*?>')
            match = href_url.search(comment)

            # Gets the match and returns the next page URL and parsed HTML
            if match:
                next_page_url = match.group(1)
                return next_page_url, soup

            else:
                return None, None

        else:
            return None, None
    else:
        return None, None


def ddg_get_loop_request(url, first_page_html, iterations):

    compiled_parsed_html = [first_page_html]

    next_url = rf"https://lite.duckduckgo.com{url}"

    for _ in range(1, iterations):
        time.sleep(random.randint(15, 20))

        # Random User-Agent
        user_agent = user_agent_rotator.get_random_user_agent()

        # Send GET request with user-agent or else it will return an error
        response = requests.get(next_url, headers={"User-Agent": user_agent})

        # Use BS4 html parser
        soup = BeautifulSoup(response.text, 'html.parser')

        compiled_parsed_html.append(soup)

        # Finds the unique form "next_form"
        try:
            url_form = soup.find('input', {'value': 'Next Page >'}).find_parent('form')

        except AttributeError:

            # If the next page form can't be found, check if it is the end of results
            try:
                no_more_results = soup.find("span", class_="no-results")
                if no_more_results:
                    print("End of Results...")
                    return compiled_parsed_html

            except AttributeError:
                print("Captcha Detected...")
                return compiled_parsed_html

            return compiled_parsed_html

        # Checks if the form exists
        if url_form:
            # Finds the comment within the form
            comment = url_form.find(string=lambda text: isinstance(text, str) and 'Next Page' in text)

            # Uses regex to search for and match the url from the comment
            if comment:
                href_url = re.compile(r'<a\s.*?href="([^"]*)".*?>')
                match = href_url.search(comment)

                # Gets the match and returns the next page URL and parsed HTML
                if match:
                    next_url = rf"https://lite.duckduckgo.com{match.group(1)}"
                    continue

                else:
                    break

            else:
                break
        else:
            break

    return compiled_parsed_html


def main():
    # Create variables and set to None for later
    # tld from documentation is named site in the script for query generation
    query, page_iter, alpha2, site, region, translateto, inurl, intitle, filetype = None, None, None, None, None, None, None, None, None

    # Get the arguments and handle any errors
    # q, p, a2, tld, kl
    try:
        options, args = getopt.getopt(sys.argv[1:], "hq:p:", ["a2=", "tld=", "kl=", "tt=", "iu=", "it=", "ft="])

    except getopt.GetoptError:
        print(cli_options), sys.exit(2)

    # Assign options and overwrite None values
    for opt, arg in options:
        if opt == "-h":
            print(cli_options), sys.exit(0)
        elif opt == "-q":
            query = arg

        elif opt == "-p":
            page_iter = int(arg)

        elif opt == "--a2":
            alpha2 = arg

        elif opt == "--tld":
            site = arg

        elif opt == "--tt":
            translateto = arg

        elif opt == "--iu":
            inurl = arg

        elif opt == "--it":
            intitle = arg

        elif opt == "--ft":
            filetype = arg

        elif opt == "--kl":
            region = arg

    if any(var is None for var in (query, alpha2, page_iter)):
        print("Query and Alpha2 Code are Required, Use -h for more Information \n Exiting..."), sys.exit(2)

    # URL Dictionary on contains one value as of now but more can be added to scale URL
    url_var_dict = {
        "kl": region
    }
    query_var_dict = {
        "site": site,
        "inurl": inurl,
        "intitle": intitle,
        "filetype": filetype
    }

    if translateto:
        query = ddg_translate_query(query, translateto)

    # Generate custom url from CLI arguments
    custom_url = generate_start_url(query, query_variables=query_var_dict, url_variables=url_var_dict)

    # Get DDG generated URL and first page HTML
    next_page_url, request_html = ddg_get_request(custom_url)

    # Extract the HTML for subsequent pages and compile HTML
    compiled_html = ddg_get_loop_request(next_page_url, request_html, page_iter)

    # Extract the URLs/domains from the compiled HTML
    domain_list = extract_domains(compiled_html)

    # Urlparse and remove duplicate urls/domains
    final_domain_list = clean_domain_names(domain_list)

    if site:
        # Return list of the top 100 domains for the TLD...
        # This will help remove social media and popular ecommerce sites etc
        try:
            top_domains = unpack_domains_from_txt(f"{TOP100_DIR}{site.lstrip('.')}.txt")

            # Iterate through domains and removes common ones to refine results
            for domain in final_domain_list:

                if domain in top_domains:
                    final_domain_list.remove(domain)

                else:
                    continue
        except FileNotFoundError:
            print(final_domain_list)
            print(f"Total Number of Unique Domains: {len(final_domain_list)}")

        print(final_domain_list)
        print(f"Total Number of Unique Domains: {len(final_domain_list)}")


GEOIP_READER.close()
