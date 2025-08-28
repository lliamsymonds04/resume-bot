#set page(
  paper: "us-letter",
  margin: (top: 0.5in, bottom: 0.5in, left: 0.75in, right: 0.75in),
)

#set text(
  font: "Arial",
  size: 10pt,
)

#show heading: it => [
  #set text(
    weight: "bold",
    size: 12pt,
  )
  #it
  #v(6pt)
]

#let header(name, contact_info, linkedin, github) = [
  #set text(size: 12pt)
  #name #h(1fr) #contact_info | #linkedin | #github
  #v(12pt)
  #line(length: 100%, stroke: 0.5pt)
  #v(12pt)
]

#let summary(summary_text) = [
  #heading("Summary")
  #summary_text
  #v(12pt)
]

#let experience(experience_list) = [
  #heading("Experience")
  #for experience in experience_list {
    let (company, job_title, dates, description) = experience
    [#job_title at #company, #dates]
    #v(6pt)
    [#description]
    #v(12pt)
  }
]

#let education(education_list) = [
  #heading("Education")
  #for education in education_list {
    let (institution, degree, dates) = education
    [#degree at #institution, #dates]
    #v(6pt)
  }
  #v(12pt)
]

#let skills(skills_list) = [
  #heading("Skills")
  #for skill in skills_list {
    [#skill]
  }
]

#let resume(
  name,
  contact_info,
  linkedin,
  github,
  summary_text,
  experience_list,
  education_list,
  skills_list,
) = [
  #header(name, contact_info, linkedin, github)
  #summary(summary_text)
  #experience(experience_list)
  #education(education_list)
  #skills(skills_list)
]

#resume(
  name: "John Doe",
  contact_info: "(123) 456-7890 | johndoe@email.com",
  linkedin: "linkedin.com/in/johndoe",
  github: "github.com/johndoe",
  summary_text: "Highly motivated and detail-oriented professional with 5+ years of experience.",
  experience_list: (
    ("Company A", "Job Title A", "2020-Present", "Description of job responsibilities and achievements."),
    ("Company B", "Job Title B", "2018-2020", "Description of job responsibilities and achievements."),
  ),
  education_list: (
    ("University A", "Bachelor of Science in Computer Science", "2015-2019"),
    ("University B", "Master of Science in Data Science", "2020-2022"),
  ),
  skills_list: (
    "Python",
    "JavaScript",
    "Data Analysis",
    "Machine Learning",
  ),
)