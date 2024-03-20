-- Insert members into members
INSERT INTO members (first_name, last_name, email, password, join_date, gender, height, weight, bmi, body_fat_percentage) VALUES
('Marcus', 'Smith', 'marcus.smith@gmail.com', 'Marcus123', '2022-01-21', 'Male', 192.5, 190.5, 23.3, 19.0),
('Janet', 'Peters', 'janet.peters@gmail.com', 'Janet123', '2024-03-12', 'Female', 165.0, 110.0, 18.3, 12.0),
('Russell', 'Wilson', 'russell.wilson@gmail.com', 'Russell123', '2024-02-03', 'Male', 180.0, 215.0, 30.1, 28.0),
('Laura', 'Harris', 'laura.harris@gmail.com', 'Laura123', '2023-11-11', 'Female', 162.8, 101.0, 17.3, 13.0),
('Richard', 'Johnson', 'richard.johnson@gmail.com', 'Richard123', '2024-01-14', 'Male', 185.0, 170.3, 22.6, 16.0);

-- Insert trainers into trainers
INSERT INTO trainers (first_name, last_name, email, password) VALUES
('Jessica', 'Norman', 'jessica.norman@trainer.com', 'Jessica123'),
('Arnold', 'Jackson', 'arnold.jackson@trainer.com', 'Arnold123'),
('Ryan', 'Patrick', 'ryan.patrick@trainer.com', 'Ryan123');

-- Insert admins into administrators
INSERT INTO administrators (first_name, last_name, email, password) VALUES
('Admin', 'Admin', 'admin@admin.com', 'admin'),
('Rick', 'Niel', 'rick.niel@admin.com', 'Rick123'),
('Chris', 'Conlin', 'chris.conlin@admin.com', 'Chris123');

-- Add availabilities for the three trainers to trainer_availability
INSERT INTO trainer_availability (trainer_id, day, start_time, end_time) VALUES
(1, 'Monday', '08:00', '14:00'),
(1, 'Wednesday', '08:00', '14:00'),
(1, 'Friday', '08:00', '14:00'),
(2, 'Tuesday', '12:00', '18:00'),
(2, 'Thursday', '12:00', '18:00'),
(3, 'Monday', '8:00', '17:00'),
(3, 'Tuesday', '8:00', '17:00'),
(3, 'Wednesday', '8:00', '17:00'),
(3, 'Thursday', '8:00', '17:00'),
(3, 'Friday', '8:00', '17:00');

-- Insert member's personal sessions with trainers to personal_sessions
INSERT INTO personal_sessions (title, member_id, trainer_id, start_time, end_time) VALUES
('Weight Training', 1, 1, '2024-05-13 10:00', '2024-05-13 11:00'),
('Cardio Training', 1, 2, '2024-05-14 14:00', '2024-05-14 15:00'),
('Weight Training', 2, 3, '2024-05-24 9:00', '2024-05-24 10:00'),
('Cardio Training', 3, 2, '2024-05-23 13:00', '2024-05-23 14:00'),
('Boxing Training', 4, 1, '2024-05-29 10:00', '2024-05-29 11:00'),
('Boxing Training', 5, 2, '2024-05-21 12:00', '2024-05-21 13:00');

-- Insert the group classes into group_classes
INSERT INTO group_classes (title, trainer_id, start_time, end_time, max_members) VALUES
('Yoga Class', 1, '2024-06-03 08:00', '2024-06-03 09:00', 20),
('HIIT Class', 2, '2024-06-04 12:00', '2024-06-04 13:00', 15),
('Pilates Class', 3, '2024-06-05 09:00', '2024-06-05 10:00', 15),
('Cycling Class', 1, '2024-06-07 08:00', '2024-06-07 09:00', 10);

-- Insert member's registration for classes into class_registrations
INSERT INTO class_registrations (class_id, member_id, registration_date) VALUES
(1, 1, '2024-03-19'),
(2, 1, '2024-03-19'),
(2, 2, '2024-03-13'),
(3, 3, '2024-03-15'),
(4, 4, '2024-03-16'),
(2, 5, '2024-03-21');

-- Insert gym equipment into equipment
INSERT INTO equipment (name, condition, last_maintenance) VALUES
('Treadmill', 'Good', '2024-01-04'),
('Bicycles', 'Excellent', '2024-01-05'),
('Bench Press', 'Good', '2024-01-05'),
('Dumbbell Set', 'Excellent', '2024-01-06'),
('Ab Roller', 'Fair', '2024-01-06'),
('Rowing Machine', 'Excellent', '2024-01-06');

-- Insert rooms in the club to rooms
INSERT INTO rooms (name, max_members) VALUES
('Main Gym', 100),
('Yoga Studio', 20),
('Bicycle Room', 20),
('Dance Studio', 20),
('Pool Room', 30),
('Sauna Room', 10),
('Boxing Room', 10);

-- Insert bookings for rooms into room_bookings
INSERT INTO room_bookings (room_id, date, start_time, end_time, purpose) VALUES
(1, '2024-05-31', '18:00', '22:00', 'Staff Party'),
(5, '2024-06-19', '10:00', '17:00', 'Swim Meet'),
(7, '2024-06-20', '20:00', '24:00', 'Boxing fight');

-- Insert member's fitness achievements into fitness_achievements
INSERT INTO fitness_achievements (member_id, name, achieved_date) VALUES
(1, 'Completed First Workout', '2022-01-22'),
(1, 'Completed 50th Workout', '2022-05-28'),
(1, 'Completed 100th Workout', '2022-12-04'),
(1, 'Ran 1000 total km', '2023-01-06'),
(2, 'Completed First Workout', '2024-03-14'),
(3, 'Completed First Workout', '2024-02-20'),
(4, 'Completed First Workout', '2024-11-21'),
(4, 'Ran 1000 total km', '2024-03-01'),
(5, 'Completed First Workout', '2024-01-16');

-- Insert goals for members into goals
INSERT INTO goals (member_id, name, target_value, target_date) VALUES
(1, 'Lose Weight', 10, '2024-05-21'),
(1, 'Increase Bench Press', 20, '2024-05-28'),
(2, 'Lose Weight', 5, '2024-05-24'),
(3, 'Increase Deadlift Weight', 20, '2024-05-16'),
(4, 'Lose Weight', 5, '2024-05-27'),
(5, 'Increase Bench Press', 30, '2024-06-04');

-- Insert generated bills into bills
INSERT INTO bills (member_id, amount, payment_due_date, status, description) VALUES
(1, 580.00, '2024-03-01', 'Not Paid', 'Yearly Membership Fee, Personal Weight Training, Personal Cardio, Yoga Class, HIIT Class'),
(2, 540.00, '2024-03-01', 'Not Paid', 'Yearly Membership Fee, Personal Weight Training, HIIT Class');
