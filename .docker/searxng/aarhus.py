# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Aarhus Municipality Search Engine

Search engine for the official Aarhus municipality website (aarhus.dk).
This engine searches for municipal information, services, and content from
the Aarhus Municipality in Denmark.

The site uses Cludo search API which requires a two-step process:
1. Fetch the search page to get a CSRF token
2. Use the token to call the Cludo API
"""

import json
import re

# Engine metadata
about = {
    "website": 'https://aarhus.dk',
    "wikidata_id": 'Q25319',  # Wikidata ID for Aarhus
    "official_api_documentation": None,
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# Engine configuration
categories = ['general']
paging = True
time_range_support = False
safesearch = False

# URL configuration
base_url = 'https://aarhus.dk'
search_page_url = base_url + '/soegeresultat?query={query}'
api_url = base_url + '/api/Cludo/Search'

# Cludo configuration
search_page_id = 208702
pagesize = 10


def get_user_agent():
    """
    Get the User-Agent string for HTTP requests.

    Returns:
        str: User-Agent string
    """
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def request(query, params):
    """
    Build the search request for aarhus.dk Cludo API.

    This requires a two-step process:
    1. First, we need to fetch the search page to get the CSRF token
    2. Then we can make the API request with the token

    Args:
        query (str): search query
        params (dict): request parameters

    Returns:
        params (dict): modified parameters with URL and headers
    """
    # Calculate page number (Cludo uses 1-based pagination)
    page = params.get('pageno', 1)

    # Store the query for the response function
    params['query'] = query
    params['page'] = page

    # First request: Get the search page to extract CSRF token
    # We'll use the search page URL for the initial request
    params['url'] = search_page_url.format(query=query)

    # Set headers to mimic a real browser
    params['headers'] = {
        'User-Agent': get_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'da,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    # Mark that we need to do a two-step request
    params['is_cludo_first_step'] = True

    return params


def response(resp):
    """
    Parse the search results from aarhus.dk Cludo API.

    This is a two-step process:
    1. Parse the HTML to get the CSRF token
    2. Make an API request with the token to get results

    Args:
        resp: HTTP response object

    Returns:
        list: List of result dictionaries
    """
    results = []

    try:
        from lxml import html as lxml_html
        import re

        # Step 1: Extract CSRF token from the HTML
        dom = lxml_html.fromstring(resp.text)

        # Find the CSRF token in the hidden input field
        csrf_token_elements = dom.xpath('//input[@name="__RequestVerificationToken"]/@value')

        if not csrf_token_elements:
            # No CSRF token found, return empty results
            return results

        csrf_token = csrf_token_elements[0]

        # Extract cookies from the response for session handling
        cookies = getattr(resp, 'cookies', None)

        # Step 2: Make API request to get search results
        # Extract query from the URL since SearXNG doesn't pass search_params to response
        query = ''
        page = 1

        # Parse query from URL (convert URL object to string first)
        url = str(resp.url)

        if '?query=' in url:
            # Extract query parameter from URL
            query_match = re.search(r'query=([^&]+)', url)
            if query_match:
                from urllib.parse import unquote
                query = unquote(query_match.group(1))

        # Prepare API request
        api_data = {
            'searchPageId': search_page_id,
            'pagesize': pagesize,
            'page': page,
            'query': query,
            'category': '',
            'allowdocs': True
        }

        # Make the API request using SearXNG's network module
        from searx import network
        import json as json_lib

        api_headers = {
            'User-Agent': get_user_agent(),
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrf_token,
            'Accept': 'application/json',
            'Referer': search_page_url.format(query=query),
            'Origin': base_url,
        }

        # Serialize data to JSON string
        json_data = json_lib.dumps(api_data)

        api_response = network.post(
            api_url,
            headers=api_headers,
            cookies=cookies,
            data=json_data
        )

        if api_response.status_code != 200:
            return results

        # Parse JSON response
        data = api_response.json()

        # Extract results from the response
        documents = data.get('typedDocuments', [])

        for doc in documents:
            try:
                fields = doc.get('fields', {})

                # Extract URL
                url_field = fields.get('url')
                if not url_field or not isinstance(url_field, dict):
                    continue
                url = url_field.get('value', '')
                if not url:
                    continue

                # Extract title
                title_field = fields.get('title')
                if not title_field or not isinstance(title_field, dict):
                    continue
                title = title_field.get('value', '')
                if not title:
                    continue

                # Extract description (try description first, then manchettext as fallback)
                description = ''
                desc_field = fields.get('description')
                if desc_field and isinstance(desc_field, dict):
                    # Get all values from the values array and join them
                    values = desc_field.get('values', [])
                    if values and len(values) > 0:
                        # Join all values with comma and space
                        description = ', '.join(v.strip() for v in values if v.strip())
                    else:
                        description = desc_field.get('value', '').strip()

                if not description:
                    manchet_field = fields.get('manchettext')
                    if manchet_field and isinstance(manchet_field, dict):
                        description = manchet_field.get('value', '').strip()

                # Build result dictionary
                result = {
                    'url': url,
                    'title': title,
                    'content': description,
                }

                # Optional: Extract additional metadata
                # Category
                category_field = fields.get('category')
                if category_field and isinstance(category_field, dict):
                    category = category_field.get('value', '')
                    if category:
                        result['metadata'] = category

                results.append(result)

            except Exception:
                # Skip malformed results
                continue

    except Exception:
        # Handle parsing errors gracefully
        pass

    return results
