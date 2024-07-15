# Scraper Architecture

Given a course catalogue URL for a particular subject area, each scraper must
get the name, course code, semester, aims, ILOs for each course.

Input: Course Catalogue URL
Output: For each course, JSON of the form --

```
[
    { name: <course name>,
      course_code: <course code>,
      semester: <semester>,
      summary: <summary / aims>,
      ilos: <ILOs>
    }
]
```

