
-- Table to hold the members of the club
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE,
    gender VARCHAR(20) NOT NULL,
    height DECIMAL(5,2) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    bmi DECIMAL(5,2),
    body_fat_percentage DECIMAL(5,2)
);

-- Table to hold trainers of the club
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE
);

-- Table to hold admins of the club
CREATE TABLE administrators (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

--Table to hold day and time slots that a trainer is available
CREATE TABLE trainer_availability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INTEGER REFERENCES trainers(trainer_id),
    day VARCHAR(20) NOT NULL, 
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- Table to hold personal sessions booked by members with trainers
CREATE TABLE personal_sessions (
    session_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    member_id INTEGER REFERENCES members(member_id),
    trainer_id INTEGER REFERENCES trainers(trainer_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

-- Table to hold group fitness classes
CREATE TABLE group_classes (
    class_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    trainer_id INTEGER REFERENCES trainers(trainer_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    max_members INTEGER NOT NULL
);

-- Table to hold Member registrations for group classes
CREATE TABLE class_registrations (
    registration_id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES group_classes(class_id),
    member_id INTEGER REFERENCES members(member_id),
    registration_date DATE DEFAULT CURRENT_DATE
);

-- Table to hold equipment available in the gym
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    condition VARCHAR(50) NOT NULL,
    last_maintenance DATE NOT NULL
);

-- Table to hold rooms in the fitness club
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    max_members INTEGER NOT NULL
);

-- Table to store room bookings
CREATE TABLE room_bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(room_id),
    date DATE NOT NULL, 
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    purpose VARCHAR(255) NOT NULL
);

-- Table to store fitness achievements for members
CREATE TABLE fitness_achievements (
    achievement_id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES members(member_id),
    name VARCHAR(255) NOT NULL,
    achieved_date DATE DEFAULT CURRENT_DATE
);

-- Table to hold goals for members
CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES members(member_id),
    name VARCHAR(255) NOT NULL,
    target_value DECIMAL(10, 2),
    target_date DATE NOT NULL
);

-- Table to hold generated bills
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES members(member_id),
    amount DECIMAL(10, 2) NOT NULL,
    bill_created_date DATE DEFAULT CURRENT_DATE,
    payment_due_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    description TEXT
);