# DSA Progress & Revision Analyzer

## 1. Problem Statement

Students preparing for technical interviews solve a large number of Data Structures and Algorithms (DSA) problems across different topics and difficulty levels. However, simply recording solved problems does not provide enough insight into learning progress.

Students need a system that can track solved, attempted, and unsolved problems, analyze topic-wise performance, identify weak areas, monitor consistency, and schedule revisions so that previously solved problems are not forgotten.

The DSA Progress & Revision Analyzer is a command-line based Python application that provides centralized DSA tracking, progress analytics, and spaced-repetition based revision scheduling using SQLite.

## 2. Scope

The project focuses on personal DSA progress management through a terminal-based interface.

The system supports:

* Adding and managing DSA problems
* Searching and filtering problems
* Tracking problem status and solved dates
* Topic-wise and difficulty-wise analytics
* Weekly progress analysis
* Current and longest solving streaks
* Weak-topic identification
* Spaced-repetition revision scheduling
* Revision history tracking
* Due and upcoming revision detection
* TXT, JSON, and CSV report generation
* JSON-based sample data import
* Application logging
* Automated testing

The project does not attempt to connect to external coding platforms or automatically retrieve user activity from LeetCode, CodeChef, or other platforms.

## 3. Target Users

The primary target users are:

* College students preparing for coding interviews
* DSA learners tracking their problem-solving progress
* Students preparing for placement coding rounds
* Beginners who want a structured revision schedule

## 4. High-Level Features

### Problem Management

Users can:

* Add a DSA problem
* View a problem
* Update problem details
* Delete a problem
* List all problems
* Search problems by title
* Filter by topic, difficulty, status, and platform

### Progress Analytics

The system calculates:

* Total tracked problems
* Solved/attempted/unsolved distribution
* Easy/Medium/Hard distribution
* Topic-wise problem distribution
* Solved problems by topic
* Weekly solving progress
* Current streak
* Longest streak
* Weak topics

### Revision Scheduler

The application uses spaced repetition intervals of:

* 1 day
* 3 days
* 7 days
* 14 days
* 30 days

Revision performance can be recorded using:

* Again
* Hard
* Good
* Easy

The revision result determines the next revision date.

### Reporting

Users can generate reports in:

* TXT
* JSON
* CSV

### Data Storage

SQLite is used for persistent local storage.

The database contains:

* `problems`
* `revision_log`

### Testing and Reliability

The project contains automated pytest tests covering:

* Problem management
* Validation
* Searching and filtering
* Analytics
* Streak calculations
* Revision scheduling
* Error handling
* Data import

## 5. Project Objective

The main objective is to transform basic DSA problem tracking into a useful progress-analysis and revision system that helps students understand their preparation patterns and maintain consistent revision.