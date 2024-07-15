#!/usr/bin/env python3
# Scrapes Deakin University, Australia pages
from bs4 import BeautifulSoup
import json
import requests
import os

import json
from bs4 import BeautifulSoup

CATALOGUE_URL = "https://www.deakin.edu.au/current-students-courses/course.php?course=S406&version=1&year=2024"

def scrape_catalogue(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    courses = []

    for a in soup.find_all('a', href=True):
        if 'unit.php' in a['href']:
            course_code = a.text.strip()
            course_name = a.find_next('td').text.strip()
            url = a['href']
            courses.append({
                'name': course_name,
                'course_code': course_code,
                'url': url
            })

    return courses

def scrape_course_page(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Extract course name and code
    course_header = soup.find('h1').text.strip()
    course_code, course_name = course_header.split(' - ', 1)
    print(f"Scraping {course_name}")

    # Extract semesters
    semester_data = soup.find_all('td')[1].text.strip().replace('\n', ' ')

    # Extract aims
    aims_header = soup.find('h3', string='Content')
    aims = aims_header.find_next('p').text.strip()

    # Extract ILOs
    ilos_table = aims_header.find_next('table')
    ilos = []
    for row in ilos_table.find_all('tr')[1:]:
        ilos.append(row.find_all('td')[1].text.strip())

    course_details = {
        'name': course_name,
        'course_code': course_code,
        'semester': semester_data,
        'aims': aims,
        'ilos': "\n".join(ilos)
    }

    return course_details

def scrape():
    output = [ scrape_course_page(course['url']) for course in \
              scrape_catalogue(CATALOGUE_URL) ]
    with open(os.path.join('courses', 'deakin.json'), 'w') as f:
        f.write(json.dumps(output, indent=True))


def main():
    scrape()

if __name__ == "__main__":
    main()

