#!/usr/bin/env python3
# Scrapes UofG pages
from bs4 import BeautifulSoup
import json
import requests

CATALOGUE_URL = "https://www.gla.ac.uk/coursecatalogue/courselist/?code=REG30200000"

def scrape_catalogue(url):
    response = requests.get(url)
    html = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all course list items
    course_list_items = soup.find('main').find_all('li')

    # Extract course details
    courses = []
    for item in course_list_items:
        course_name = item.find('a').text.strip()
        course_code = item.find('span').text.strip()
        course_url = item.find('a')['href']
        courses.append({
            'name': course_name,
            'course_code': course_code,
            'url': 'https://www.gla.ac.uk' + course_url
        })

    # Convert to JSON
    # courses_json = json.dumps(courses, indent=2)
    return courses

def scrape_course_page(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser').find('main')

    course_details = {
        "name": "",
        "course_code": "",
        "semester": "",
        "aims": "",
        "ilos": ""
    }

    # Extract course name
    course_name_tag = soup.find('h2')
    if course_name_tag:
        course_details["name"] = course_name_tag.get_text(strip=True)

    # Extract course code
    course_code_tag = soup.find('a', href=True)
    if course_code_tag:
        course_details["course_code"] = course_code_tag['href'].split('=')[-1]

# Extract semester
    semester_strong_tag = soup.find('strong', string='Typically Offered:')
    if semester_strong_tag and semester_strong_tag.parent.name == 'li':
        semester_tag = semester_strong_tag.parent
        course_details["semester"] = semester_tag.get_text(strip=True).split(':')[1]

# Extract aims
    aims_tag = soup.find('h3', string='Course Aims').find_next('div')
    if aims_tag:
        course_details["aims"] = aims_tag.get_text(strip=True)

# Extract intended learning outcomes
    ilos_tag = soup.find('h3', string='Intended Learning Outcomes of Course').find_next('div')
    if ilos_tag:
        course_details["ilos"] = ilos_tag.get_text(strip=True)

# Convert to JSON
    json_output = json.dumps(course_details, indent=2)
    return json_output
    #print(json_output)

def scrape():
    #output = [ scrape_course_page(course['url']) for course in \
    #    scrape_catalogue(CATALOGUE_URL) ]
    output = scrape_course_page(scrape_catalogue(CATALOGUE_URL)[0]['url'])
    print(output)
#    with open('glasgow.json', 'w') as f:
#        f.write(json.dumps(output_json))

## TEMP
def main():
    #print(scrape_catalogue(CATALOGUE_URL))
    scrape()

if __name__ == "__main__":
    main()
