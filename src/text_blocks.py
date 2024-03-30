midnight_logo = r"""
___  ____     _       _       _     _    ___  ___            
|  \/  (_)   | |     (_)     | |   | |   |  \/  |            
| .  . |_  __| |_ __  _  __ _| |__ | |_  | .  . | __ _ _ __  
| |\/| | |/ _` | '_ \| |/ _` | '_ \| __| | |\/| |/ _` | '_ \ 
| |  | | | (_| | | | | | (_| | | | | |_  | |  | | (_| | |_) |
\_|  |_/_|\__,_|_| |_|_|\__, |_| |_|\__| \_|  |_/\__,_| .__/ 
                         __/ |                        | |    
                        |___/                         |_|    

Uncover Industrial Scale Web Attack Surfaces

Gain intelligence into the attack surface of web applications within geographic regions and/or TLDs.
"""

cli_options = r"""

___  ____     _       _       _     _    ___  ___            
|  \/  (_)   | |     (_)     | |   | |   |  \/  |            
| .  . |_  __| |_ __  _  __ _| |__ | |_  | .  . | __ _ _ __  
| |\/| | |/ _` | '_ \| |/ _` | '_ \| __| | |\/| |/ _` | '_ \ 
| |  | | | (_| | | | | | (_| | | | | |_  | |  | | (_| | |_) |
\_|  |_/_|\__,_|_| |_|_|\__, |_| |_|\__| \_|  |_/\__,_| .__/ 
                         __/ |                        | |    
                        |___/                         |_|    
                        
- Midnight Map -

A tool designed to map out attack surfaces for websites in specific countries which can be defined by industry.

This tool will search for web addresses related to keywords defined by TLDs and IP address spaces.


EXAMPLE COMMANDS -

------
python3 midnightmap.py -q "online pharmacy" -p 5 --a2 RU --tld .ru --tt ru --kl ru-ru


------

USAGE - 

Documentation - h

     Display this manual page

Search Query - q (REQUIRED)
    
    Specify a search query which can be any length of text, advanced search parameters can be included in here
    
Page Iterations - p (REQUIRED)

    Specify the number of DuckDuckGo pages that should be scrape for URLs. Search may end sooner if all pages are exhausted.

Country IP Address Space - a2 (REQUIRED)

    Specify an IP Address Space, only one country can be specified at a time. All country code formats are in ISO 3166-1 Alpha 2 
    See - https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

Top Level Domain - tld (OPTIONAL)
    
    Specify a TLD to search against, for example to search for Russian domains you might specify .ru .su .pyc .xn--p1ai
    NOTE: This will also trigger the function to remove common sites, for example, if your TLD was .com, it would remove
    twitter.com, facebook.com etc
    
TranslateTo - tt (OPTIONAL)
    
    Specify a language to translate query to, searching in the local language can often yield better results.
    
InUrl - iu (OPTIONAL)

    Specify a URL that includes a word
    
InTitle - it (OPTIONAL)

    Specify a title that includes a word

Filetype - ft (OPTIONAL)

    Specify a filetype to search against, this will dramatically decrease the number of results

DuckDuckGo Region Search - kl (OPTIONAL)

    xa-ar for Arabia
    xa-en for Arabia (en)
    ar-es for Argentina
    au-en for Australia
    at-de for Austria
    be-fr for Belgium (fr)
    be-nl for Belgium (nl)
    br-pt for Brazil
    bg-bg for Bulgaria
    ca-en for Canada
    ca-fr for Canada (fr)
    ct-ca for Catalan
    cl-es for Chile
    cn-zh for China
    co-es for Colombia
    hr-hr for Croatia
    cz-cs for Czech Republic
    dk-da for Denmark
    ee-et for Estonia
    fi-fi for Finland
    fr-fr for France
    de-de for Germany
    gr-el for Greece
    hk-tzh for Hong Kong
    hu-hu for Hungary
    in-en for India
    id-id for Indonesia
    id-en for Indonesia (en)
    ie-en for Ireland
    il-he for Israel
    it-it for Italy
    jp-jp for Japan
    kr-kr for Korea
    lv-lv for Latvia
    lt-lt for Lithuania
    xl-es for Latin America
    my-ms for Malaysia
    my-en for Malaysia (en)
    mx-es for Mexico
    nl-nl for Netherlands
    nz-en for New Zealand
    no-no for Norway
    pe-es for Peru
    ph-en for Philippines
    ph-tl for Philippines (tl)
    pl-pl for Poland
    pt-pt for Portugal
    ro-ro for Romania
    ru-ru for Russia
    sg-en for Singapore
    sk-sk for Slovak Republic
    sl-sl for Slovenia
    za-en for South Africa
    es-es for Spain
    se-sv for Sweden
    ch-de for Switzerland (de)
    ch-fr for Switzerland (fr)
    ch-it for Switzerland (it)
    tw-tzh for Taiwan
    th-th for Thailand
    tr-tr for Turkey
    ua-uk for Ukraine
    uk-en for United Kingdom
    us-en for United States
    ue-es for United States (es)
    ve-es for Venezuela
    vn-vi for Vietnam
    wt-wt for No region

Exit Codes -

(0) / (1) - Default
(2) - Argument / Argument Parsing Error
(3) - DuckDuckGo Scraping Error

Credit -

With thanks to DuckDuckGo for providing such an amazing search engine and open use policy.

"""