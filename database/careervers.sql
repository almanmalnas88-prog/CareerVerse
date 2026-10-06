DROP DATABASE IF EXISTS careerverse;

CREATE DATABASE careerverse;

USE careerverse;


-- =========================================
-- STUDENTS
-- =========================================

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    education VARCHAR(100),
    city VARCHAR(100),
    family_occupation VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================
-- CAREERS
-- =========================================

CREATE TABLE careers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    education_required TEXT,
    skills_required TEXT
);


-- =========================================
-- QUESTIONS
-- =========================================

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL
);


-- =========================================
-- OPTIONS
-- =========================================

CREATE TABLE options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,

    FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);


-- =========================================
-- STUDENT ANSWERS
-- =========================================

CREATE TABLE student_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    question_id INT NOT NULL,
    option_id INT NOT NULL,

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE,

    FOREIGN KEY (option_id)
        REFERENCES options(id)
        ON DELETE CASCADE
);


-- =========================================
-- CAREERS DATA
-- =========================================

INSERT INTO careers
(name, category, description, education_required, skills_required)
VALUES

(
'Actor',
'Entertainment',
'Work in films, television, theatre, advertisements and digital media.',
'Acting training, theatre experience or relevant education.',
'Acting, communication, confidence, expression'
),

(
'Singer',
'Entertainment',
'Professional career in singing, music and live performance.',
'Music training can be useful but is not always mandatory.',
'Singing, rhythm, voice control, performance'
),

(
'Dancer',
'Entertainment',
'Professional career in dance, choreography and performance.',
'Dance training and practical experience.',
'Dance, rhythm, fitness, discipline'
),

(
'Film Director',
'Entertainment',
'Lead the creative direction of films and video productions.',
'Film education or practical filmmaking experience.',
'Storytelling, leadership, creativity'
),

(
'Graphic Designer',
'Creative',
'Create visual designs for brands, websites and media.',
'Design education or portfolio-based learning.',
'Creativity, design, typography, visual thinking'
),

(
'Software Developer',
'Technology',
'Build websites, applications and software systems.',
'Computer science or programming education can help.',
'Programming, logic, problem solving'
),

(
'AI Engineer',
'Technology',
'Build artificial intelligence and machine learning systems.',
'Computer science, mathematics or related education.',
'Python, mathematics, AI, problem solving'
),

(
'Data Scientist',
'Technology',
'Use data and statistics to solve real-world problems.',
'Statistics, mathematics, computer science or related education.',
'Python, statistics, SQL, analysis'
),

(
'Cybersecurity Specialist',
'Technology',
'Protect computers, networks and digital information.',
'Cybersecurity or computer science education.',
'Networking, security, problem solving'
),

(
'Web Developer',
'Technology',
'Build and maintain websites and web applications.',
'Web development or computer science education.',
'HTML, CSS, JavaScript, programming'
),

(
'Entrepreneur',
'Business',
'Create, manage and grow a business or startup.',
'No single degree is mandatory.',
'Leadership, sales, communication, decision making'
),

(
'Business Consultant',
'Business',
'Help organizations solve business and strategic problems.',
'Business or related education can help.',
'Strategy, analysis, communication'
),

(
'Marketing Manager',
'Business',
'Develop marketing strategies and grow brands.',
'Marketing, business or related education.',
'Marketing, communication, creativity'
),

(
'Lawyer',
'Law',
'Provide legal advice and represent clients in legal matters.',
'Law degree and applicable professional requirements.',
'Legal research, communication, reasoning'
),

(
'Legal Consultant',
'Law',
'Provide professional guidance on legal and regulatory matters.',
'Law education and applicable professional requirements.',
'Legal knowledge, analysis, communication'
),

(
'Teacher',
'Education',
'Teach and guide students in academic and practical subjects.',
'Relevant degree and teaching qualifications where required.',
'Communication, patience, subject knowledge'
),

(
'Doctor',
'Healthcare',
'Diagnose and treat patients and provide medical care.',
'Medical degree and required licensing.',
'Medical knowledge, communication, decision making'
),

(
'Nurse',
'Healthcare',
'Provide patient care and support healthcare teams.',
'Nursing education and applicable licensing.',
'Patient care, responsibility, communication'
),

(
'Architect',
'Design',
'Design buildings, spaces and structures.',
'Architecture degree and applicable professional requirements.',
'Design, mathematics, visualization'
),

(
'Civil Engineer',
'Engineering',
'Design and manage infrastructure such as buildings, roads and bridges.',
'Civil engineering degree.',
'Mathematics, engineering, planning'
),

(
'Agricultural Scientist',
'Agriculture',
'Use science and technology to improve farming and agriculture.',
'Agriculture, biology or related education.',
'Agriculture, research, science'
),

(
'Agribusiness Manager',
'Agriculture',
'Manage businesses connected to farming and agricultural products.',
'Agriculture, business or related education.',
'Business, agriculture, management'
),

(
'Food Technologist',
'Agriculture',
'Work with food production, safety and processing.',
'Food technology or related education.',
'Science, food technology, quality control'
);


-- =========================================
-- QUESTIONS
-- =========================================

INSERT INTO questions (question_text)
VALUES

('What activity do you enjoy the most?'),

('Which skill describes you best?'),

('What type of work environment do you prefer?'),

('What motivates you the most?'),

('Which area interests you the most?');


-- =========================================
-- QUESTION 1 OPTIONS
-- =========================================

INSERT INTO options
(question_id, option_text, category)
VALUES

(1, 'Acting, singing, dancing or making videos', 'Entertainment'),

(1, 'Coding, computers and technology', 'Technology'),

(1, 'Business, selling and building ideas', 'Business'),

(1, 'Law, arguments and understanding rules', 'Law'),

(1, 'Farming, plants, animals and nature', 'Agriculture');


-- =========================================
-- QUESTION 2 OPTIONS
-- =========================================

INSERT INTO options
(question_id, option_text, category)
VALUES

(2, 'Communication and performance', 'Entertainment'),

(2, 'Logical thinking and problem solving', 'Technology'),

(2, 'Leadership and decision making', 'Business'),

(2, 'Researching and understanding rules', 'Law'),

(2, 'Practical work and understanding nature', 'Agriculture');


-- =========================================
-- QUESTION 3 OPTIONS
-- =========================================

INSERT INTO options
(question_id, option_text, category)
VALUES

(3, 'Creative and expressive environment', 'Entertainment'),

(3, 'Technology and innovation environment', 'Technology'),

(3, 'Business and leadership environment', 'Business'),

(3, 'Professional and analytical environment', 'Law'),

(3, 'Outdoor and practical environment', 'Agriculture');


-- =========================================
-- QUESTION 4 OPTIONS
-- =========================================

INSERT INTO options
(question_id, option_text, category)
VALUES

(4, 'Creativity and self-expression', 'Entertainment'),

(4, 'Innovation and solving difficult problems', 'Technology'),

(4, 'Independence and financial growth', 'Business'),

(4, 'Justice and solving legal problems', 'Law'),

(4, 'Working with nature and creating useful things', 'Agriculture');


-- =========================================
-- QUESTION 5 OPTIONS
-- =========================================

INSERT INTO options
(question_id, option_text, category)
VALUES

(5, 'Music, film, dance and arts', 'Entertainment'),

(5, 'Computer science and mathematics', 'Technology'),

(5, 'Business, economics and management', 'Business'),

(5, 'Law, society and regulations', 'Law'),

(5, 'Farming, biology and environmental science', 'Agriculture');


-- CHECK DATABASE
-- SELECT * FROM careers;

-- SELECT * FROM questions;

-- SELECT * FROM options;

select * from students;