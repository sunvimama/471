-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2025 at 04:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sut`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `id` int(11) NOT NULL,
  `activity_type` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `note_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('017602b47c23');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `note_id` int(11) DEFAULT NULL,
  `video_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `content`, `user_id`, `note_id`, `video_id`, `course_id`, `timestamp`) VALUES
(1, 'working', 3, 25, NULL, NULL, '2025-04-16 09:31:22');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`id`, `title`, `user_id`) VALUES
(1, 'abacus', 2);

-- --------------------------------------------------------

--
-- Table structure for table `course_progress`
--

CREATE TABLE `course_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `is_completed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_progress`
--

INSERT INTO `course_progress` (`id`, `user_id`, `course_id`, `week`, `is_completed`) VALUES
(1, 2, 1, 1, 1),
(2, 2, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `course_video`
--

CREATE TABLE `course_video` (
  `id` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_video`
--

INSERT INTO `course_video` (`id`, `week`, `title`, `file_path`, `course_id`) VALUES
(1, 1, 'Week 1 Video', 'static/uploads/videos/NPE_Intro.mp4', 1),
(2, 2, 'Week 2 Video', 'static/uploads/videos/Battle_Pass_Glitches.webm', 1),
(3, 3, 'Week 3 Video', 'static/uploads/videos/Contract_Glitches.webm', 1);

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `Title` varchar(100) NOT NULL,
  `des` varchar(258) DEFAULT NULL,
  `tags` varchar(50) DEFAULT NULL,
  `categories` varchar(50) DEFAULT NULL,
  `ispublic` tinyint(1) DEFAULT NULL,
  `note` varchar(500) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notes`
--

INSERT INTO `notes` (`Title`, `des`, `tags`, `categories`, `ispublic`, `note`, `id`, `user_id`) VALUES
('ssd', 'asda', 'ASDAS', 'ASD', 1, 'WDDFFWF', 1, 1),
('hi', 'bye', 'ok', 'cool', 1, 'skkkrt', 2, 1),
('welcome', 'thanks', 'wow', 'crazy', 1, 'notttte', 3, 1),
('notepad', 'hello', 'sssd', 'note', 0, 'ooo', 4, 1),
('asdf', 'waeq', 'qweq', 'qweq', 0, 'q', 5, 1),
('as', 'sff', 'safafs', 'asfasf', 0, 'aw', 6, 1),
('hi', 'asd', 'asd', 'asd', 0, 'asda', 7, 1),
('ddd', 'diiddy', 'asasd', 'asdw', 0, 'qwe', 8, 1),
('sdfsdf', 'deded', 'saas', 'asdasd', 0, 's', 9, 1),
('sdfsdf', 'deded', 'saas', 'asdasd', 0, 's', 10, 1),
('qwed', 'qwde', 'qweqweq', 'qweqwe', 0, 'qweqw', 11, 1),
('study', 'emni', 'math', 'math', 0, 'hi', 12, 1),
('test1', 'star testing', '', '', 0, 'test', 13, 1),
('new test', 'new star test', '', '', 0, 'star test', 14, 1),
('test2', 'test star', '', '', 0, 'star test', 15, 1),
('test3', 'star test3', '', '', 0, 'star test3', 16, 1),
('test4', 'test4', '', '', 0, 'test4', 17, 1),
('testttt', 'testtt', '', '', 0, 'testtt', 18, 1),
('gg', 'gg', '', '', 0, 'gg', 19, 1),
('ff', 'ff', '', '', 0, 'ff', 20, 1),
('hh', 'hh', '', '', 0, 'hh', 21, 1),
('ee', 'ee', '', '', 0, '<p>&lt;p&gt;&amp;lt;p&amp;gt;&amp;amp;lt;p&amp;amp;gt;&amp;amp;amp;lt;p&amp;amp;amp;gt;&amp;amp;amp;amp;lt;p&amp;amp;amp;amp;gt;&amp;amp;amp;amp;amp;lt;p&amp;amp;amp;amp;amp;gt;ee&amp;amp;amp;amp;amp;lt;/p&amp;amp;amp;amp;amp;gt;&amp;amp;amp;amp;lt;/p&amp;amp;amp;amp;gt;&amp;amp;amp;lt;/p&amp;amp;amp;gt;&amp;amp;lt;/p&amp;amp;gt;&amp;lt;/p&amp;gt;&lt;/p&gt;</p>', 22, 1),
('jj', 'jj', '', '', 0, '<p>jj</p>', 23, 1),
('hello world', 'hi', '', '', 0, 'bye', 24, 3),
('test final', 'im tired', '', '', 0, '*dies', 25, 3),
('hi', 'wrw', 'math', 'st', 0, 'tutu', 26, 2),
('asdad', 'asdaaf', 'awd', 'fe', 0, 'sdad', 27, 2),
('admin', 'admin', '', '', 0, 'admin', 28, 4);

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `message` varchar(255) NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `card_name` varchar(100) NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `amount` float NOT NULL,
  `expiry` varchar(5) NOT NULL,
  `cvv` varchar(3) NOT NULL,
  `payment_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `starred_note`
--

CREATE TABLE `starred_note` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `note_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `starred_note`
--

INSERT INTO `starred_note` (`id`, `user_id`, `note_id`) VALUES
(10, 3, 13),
(11, 3, 25);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_subscribed` tinyint(1) DEFAULT 0,
  `is_admin` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `is_subscribed`, `is_admin`) VALUES
(1, 'sharanali', 'qwerty', 0, 1),
(2, 'afif', 'asdfg', 1, 0),
(3, 'newuser', '1234', 0, 0),
(4, 'admin', 'admin', 0, 0),
(7, 'arbhalolagena', '$2b$12$4fduMhIATyfAkD0a1Y52V.5y9I2adDmOw5IJCfVHQOp1ih1KTC.XW', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `video`
--

CREATE TABLE `video` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video`
--

INSERT INTO `video` (`id`, `title`, `file_path`, `course_id`, `created_at`) VALUES
(1, 'video1', 'static/uploads/videos/10_04_Homescreen.mp4', NULL, '2025-04-16 15:16:02'),
(2, 'another', 'static/uploads/videos/10_02_Homescreen.mp4', NULL, '2025-04-16 17:55:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `note_id` (`note_id`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `note_id` (`note_id`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `course_progress`
--
ALTER TABLE `course_progress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_progress` (`user_id`,`course_id`,`week`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `course_video`
--
ALTER TABLE `course_video`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `starred_note`
--
ALTER TABLE `starred_note`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `note_id` (`note_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_log`
--
ALTER TABLE `activity_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `course_progress`
--
ALTER TABLE `course_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `course_video`
--
ALTER TABLE `course_video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `starred_note`
--
ALTER TABLE `starred_note`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `video`
--
ALTER TABLE `video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD CONSTRAINT `activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `activity_log_ibfk_2` FOREIGN KEY (`note_id`) REFERENCES `notes` (`id`);

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`note_id`) REFERENCES `notes` (`id`);

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `course_progress`
--
ALTER TABLE `course_progress`
  ADD CONSTRAINT `course_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_progress_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `course_video`
--
ALTER TABLE `course_video`
  ADD CONSTRAINT `course_video_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`);

--
-- Constraints for table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `starred_note`
--
ALTER TABLE `starred_note`
  ADD CONSTRAINT `starred_note_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `starred_note_ibfk_2` FOREIGN KEY (`note_id`) REFERENCES `notes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
