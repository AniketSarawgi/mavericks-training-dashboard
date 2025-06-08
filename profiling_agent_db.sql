-- CREATE DATABASE mavericks_training;
-- USE mavericks_training;

-- CREATE TABLE fresher_profiles (
--     fresher_id VARCHAR(20) PRIMARY KEY,
--     name VARCHAR(100)
-- );

-- CREATE TABLE assessments (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     fresher_id VARCHAR(20),
--     assessment_type VARCHAR(50),
--     score VARCHAR(10),
--     FOREIGN KEY (fresher_id) REFERENCES fresher_profiles(fresher_id) ON DELETE CASCADE
-- );

-- CREATE TABLE certifications (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     fresher_id VARCHAR(20),
--     certification_name VARCHAR(100),
--     FOREIGN KEY (fresher_id) REFERENCES fresher_profiles(fresher_id) ON DELETE CASCADE
-- );

-- CREATE TABLE learning_progress (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     fresher_id VARCHAR(20),
--     topic VARCHAR(100),
--     status VARCHAR(50),
--     FOREIGN KEY (fresher_id) REFERENCES fresher_profiles(fresher_id) ON DELETE CASCADE
-- );
SELECT 
    a.fresher_id,
    a.assessment_type,
    a.score,
    c.certification_name,
    f.name,
    l.topic,
    l.status
FROM assessments a
LEFT JOIN certifications c ON a.fresher_id = c.fresher_id
LEFT JOIN fresher_profiles f ON a.fresher_id = f.fresher_id
LEFT JOIN learning_progress l ON a.fresher_id = l.fresher_id;







