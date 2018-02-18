# --------------------------------------------------------------------------------------
# ************************************ SYNOPSIS ****************************************
# --------------------------------------------------------------------------------------
# Name of the program: Conversational Agent
# Author             : Partha Barua (Lincoln)
# Date created       : November 2017
# Date updated       : January 2018
# Purpose            : Prepared for Assignment-I (Unit:'Artificial Intelligence-COMP329')
# Awarded Grade      : HD (95%)
#****************************************************************************************


import re
import datetime
import calendar
import random
import sqlite3
import textwrap


store_ans = {}  # stores time-table information
store_tw_ans = {}  # stores track-work information

dow = {d: i for i, d in # day of the week manipulation
       enumerate('Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday'.split(','))}

stations = [] # station names
lines = []  # lines on the network

# ------ Built-in messages -----------
qs_type_1 = {'1': 'Computer: Do you want Timetable or Trackwork Information? \n',
             '2': 'Computer: Please Enter ' + '\'' + 'Timetable' + '\'' + ' ,' + '\'' + ' Trackwork' + '\'' + ' ,' + '\'' + 'Help' + '\'' + ' or' + '\'' + ' Quit' + '\' \n',
             '3': 'Computer: Please Enter Either Timetable, Trackwork, Help or Quit \n',
             '4': 'Computer: How Can I Help you? \n',
             '5': 'Computer: What Information would you like? \n',
             '6': 'Computer: Please type one of the following options: [Timetable]..[Trackwork]..[Help]..[Quit] \n'
            }

qs_type_2 = {'1': 'Computer: Do you need anymore information? [Type yes/No] \n',
             '2': 'Computer: Anything else i can do for you today [yes/No]? \n',
             '3': 'Computer: Please don' + '\'t' + ' hesitate, if you need any more information [Type Yes/No] \n',
             '4': 'Computer: Please type [Yes] for more information or [No] to quit \n',
             '5': 'Computer: Do you like any other information? [Type Yes/No] \n'
            }
# ------------------------------------
def activate_db():

    conn = sqlite3.connect('train.db')
    print('Please wait...')

    # ------------------------------------------------------------
    # Drop existing tables in database
    # ------------------------------------------------------------

    conn.execute('DROP TABLE IF EXISTS Station')

    conn.execute('DROP TABLE IF EXISTS Line')

    conn.execute('DROP TABLE IF EXISTS Station_Line')

    conn.execute('DROP TABLE IF EXISTS Train')

    conn.execute('DROP TABLE IF EXISTS Schedule')

    conn.execute('DROP TABLE IF EXISTS Trackwork')

    # ------------------------------------------------------------
    # Create new tables in database
    # ------------------------------------------------------------

    conn.execute('''CREATE TABLE Station
                         (Station_ID     INT PRIMARY KEY   NOT NULL,
                          Station_Name   VARCHAR(200)      NOT NULL)''')

    conn.execute('''CREATE TABLE Line
                         (Line_ID        INT PRIMARY KEY   NOT NULL,
                          Line_Name      VARCHAR(200)      NOT NULL)''')

    conn.execute('''CREATE TABLE Station_Line
                         (Station_ID     INT               NOT NULL,
                          Line_ID        INT               NOT NULL,
                          Prior_Station  INT,
                          Next_Station   INT,
                          FOREIGN KEY    (Prior_Station) REFERENCES Station (Station_ID),
                          FOREIGN KEY    (Next_Station) REFERENCES Station (Station_ID),
                          FOREIGN KEY    (Line_ID) REFERENCES Line (Line_ID),
                          PRIMARY KEY    (Station_ID, Line_ID))''')

    conn.execute('''CREATE TABLE Train
                         (Train_ID        INT PRIMARY KEY   NOT NULL,
                          Line_ID        INT               NOT NULL,
                          Origin         INT               NOT NULL,
                          Destination    INT               NOT NULL,
                          Part_Of_Week   CHAR(2)           NOT NULL CONSTRAINT Pow CHECK ( Part_of_Week IN ('WD', 'WE') ),
                          Direction      CHAR(2)           NOT NULL CONSTRAINT DIR CHECK ( Direction IN ('UP', 'DN') ),
                          FOREIGN KEY    (Line_ID) REFERENCES Line (Line_ID))''')

    conn.execute('''CREATE TABLE Schedule
                         (Train_ID       INT               NOT NULL,
                          Station_ID     INT               NOT NULL,
                          Departure_Time TEXT              NOT NULL,
                          FOREIGN KEY    (Station_ID) REFERENCES Station (Station_ID),
                          FOREIGN KEY    (Train_ID) REFERENCES Train (Train_ID),
                          PRIMARY KEY    (Train_ID, Station_ID) )''')

    conn.execute('''CREATE TABLE Trackwork
                         (Message_ID     INT PRIMARY KEY   NOT NULL,
                          Line_ID        INT               NOT NULL,
                          Start_Date     TEXT              NOT NULL,
                          End_Date       TEXT              NOT NULL,
                          Message        TEXT              NOT NULL,
                          FOREIGN KEY    (Line_ID) REFERENCES Line (Line_ID) )''')

    print("Conversational Agent is running...")

    # ------------------------------------------------------------
    # Populate database tables
    # ------------------------------------------------------------

    conn.executemany('INSERT INTO Station (Station_ID, Station_Name) VALUES (?, ?)',
                     [(1, 'Hornsby'),
                      (2, 'Normanhurst'),
                      (3, 'Thornleigh'),
                      (4, 'Pennant Hills'),
                      (5, 'Beecroft'),
                      (6, 'Cheltenham'),
                      (7, 'Epping'),
                      (8, 'Eastwood'),
                      (9, 'Denistone'),
                      (10, 'West Ryde'),
                      (11, 'Meadowbank'),
                      (12, 'Rhodes'),
                      (13, 'Concord West'),
                      (14, 'North Strathfield'),
                      (15, 'Strathfield'),
                      (16, 'Burwood'),
                      (17, 'Redfern'),
                      (18, 'Central'),
                      (19, 'Town Hall'),
                      (20, 'Wynyard'),
                      (21, 'Milsons Point'),
                      (22, 'North Sydney'),
                      (23, 'Waverton'),
                      (24, 'Wollstonecraft'),
                      (25, 'St Leonards'),
                      (26, 'Artarmon'),
                      (27, 'Chatswood')])

    # conn.execute("INSERT INTO Line VALUES (1, 'Northern Line')")
    conn.executemany('INSERT INTO Line (Line_ID, Line_Name) VALUES (?, ?)',
                     [(1, 'Northern Line'),
                      (2, 'Southern Line'),
                      (3, 'Western Line'),
                      (4, 'Bankstown Line')])

    conn.executemany('INSERT INTO Station_Line (Station_ID, Line_ID, Prior_Station, Next_Station) VALUES (?, ?, ?, ?)',
                     [(1, 1, None, 2),
                      (2, 1, 1, 3),
                      (3, 1, 2, 4),
                      (4, 1, 3, 5),
                      (5, 1, 4, 6),
                      (6, 1, 5, 7),
                      (7, 1, 6, 8),
                      (8, 1, 7, 9),
                      (9, 1, 8, 10),
                      (10, 1, 9, 11),
                      (11, 1, 10, 12),
                      (12, 1, 11, 13),
                      (13, 1, 12, 14),
                      (14, 1, 13, 15),
                      (15, 1, 14, 16),
                      (16, 1, 15, 17),
                      (17, 1, 16, 18),
                      (18, 1, 17, 19),
                      (19, 1, 18, 20),
                      (20, 1, 19, 21),
                      (21, 1, 20, 22),
                      (22, 1, 21, 23),
                      (23, 1, 22, 24),
                      (24, 1, 23, 25),
                      (25, 1, 24, 26),
                      (26, 1, 25, 27),
                      (27, 1, 26, None)])

    conn.executemany(
        'INSERT INTO Train (Train_ID, Line_ID, Origin, Destination, Part_of_Week, Direction) VALUES (?, ?, ?, ?, ?, ?)',
        [(1, 1, 1, 18, 'WD', 'UP'),
         (2, 1, 7, 27, 'WD', 'UP'),
         (3, 1, 1, 7, 'WD', 'UP'),
         (4, 1, 7, 27, 'WD', 'UP'),
         (5, 1, 1, 7, 'WD', 'UP'),
         (6, 1, 1, 18, 'WD', 'UP'),
         (7, 1, 7, 27, 'WD', 'UP'),
         (8, 1, 1, 7, 'WD', 'UP'),
         (9, 1, 7, 27, 'WD', 'UP'),
         (10, 1, 1, 7, 'WD', 'UP'),

         (20, 1, 27, 7, 'WD', 'DN'),
         (21, 1, 7, 1, 'WD', 'DN'),
         (22, 1, 27, 7, 'WD', 'DN'),
         (23, 1, 18, 1, 'WD', 'DN'),
         (24, 1, 7, 1, 'WD', 'DN'),
         (25, 1, 27, 7, 'WD', 'DN'),
         (26, 1, 7, 1, 'WD', 'DN'),
         (27, 1, 27, 7, 'WD', 'DN'),
         (28, 1, 18, 1, 'WD', 'DN'),
         (29, 1, 7, 1, 'WD', 'DN'),
         (30, 1, 27, 7, 'WD', 'DN'),

         (31, 1, 1, 18, 'WE', 'UP'),
         (32, 1, 1, 7, 'WE', 'UP'),
         (33, 1, 7, 27, 'WE', 'UP'),
         (34, 1, 1, 7, 'WE', 'UP'),
         (35, 1, 1, 18, 'WE', 'UP'),
         (36, 1, 1, 7, 'WE', 'UP'),
         (37, 1, 7, 27, 'WE', 'UP'),
         (38, 1, 1, 7, 'WE', 'UP'),
         (39, 1, 1, 18, 'WE', 'UP'),
         (40, 1, 1, 7, 'WE', 'UP'),

         (41, 1, 27, 7, 'WE', 'DN'),
         (42, 1, 7, 1, 'WE', 'DN'),
         (43, 1, 18, 1, 'WE', 'DN'),
         (44, 1, 7, 1, 'WE', 'DN'),
         (45, 1, 27, 7, 'WE', 'DN'),
         (46, 1, 7, 1, 'WE', 'DN'),
         (47, 1, 18, 1, 'WE', 'DN'),
         (48, 1, 7, 1, 'WE', 'DN'),
         (49, 1, 27, 7, 'WE', 'DN'),
         (50, 1, 7, 1, 'WE', 'DN')

         ])

    conn.executemany('INSERT INTO Schedule (Train_ID, Station_ID, Departure_Time) VALUES (?, ?, ?)',
                     [(1, 1, '10:20'),
                      (1, 7, '10:30'),
                      (1, 8, '10:33'),
                      (1, 15, '10:43'),
                      (1, 18, '10:56'),

                      (2, 7, '10:32'),
                      (2, 8, '10:35'),
                      (2, 9, '10:37'),
                      (2, 10, '10:39'),
                      (2, 11, '10:41'),
                      (2, 12, '10:44'),
                      (2, 13, '10:46'),
                      (2, 14, '10:48'),
                      (2, 15, '10:54'),
                      (2, 16, '10:56'),
                      (2, 17, '11:05'),
                      (2, 18, '11:09'),
                      (2, 19, '11:12'),
                      (2, 20, '11:15'),
                      (2, 21, '11:18'),
                      (2, 22, '11:22'),
                      (2, 23, '11:24'),
                      (2, 24, '11:26'),
                      (2, 25, '11:29'),
                      (2, 26, '11:31'),
                      (2, 27, '11:35'),

                      (3, 1, '10:26'),
                      (3, 2, '10:28'),
                      (3, 3, '10:31'),
                      (3, 4, '10:33'),
                      (3, 5, '10:36'),
                      (3, 6, '10:38'),
                      (3, 7, '10:41'),

                      (4, 7, '10:47'),
                      (4, 8, '10:50'),
                      (4, 9, '10:52'),
                      (4, 10, '10:54'),
                      (4, 11, '10:55'),
                      (4, 12, '10:59'),
                      (4, 13, '11:01'),
                      (4, 14, '11:03'),
                      (4, 15, '11:09'),
                      (4, 16, '11:11'),
                      (4, 17, '11:20'),
                      (4, 18, '11:24'),
                      (4, 19, '11:27'),
                      (4, 20, '11:30'),
                      (4, 21, '11:33'),
                      (4, 22, '11:37'),
                      (4, 23, '11:39'),
                      (4, 24, '11:41'),
                      (4, 25, '11:44'),
                      (4, 26, '05:46'),
                      (4, 27, '05:50'),

                      (5, 1, '10:41'),
                      (5, 2, '10:43'),
                      (5, 3, '10:46'),
                      (5, 4, '10:48'),
                      (5, 5, '10:51'),
                      (5, 6, '10:53'),
                      (5, 7, '10:56'),

                      (6, 1, '10:50'),
                      (6, 7, '11:00'),
                      (6, 8, '11:03'),
                      (6, 15, '11:13'),
                      (6, 18, '11:26'),

                      (7, 7, '11:02'),
                      (7, 8, '11:05'),
                      (7, 9, '11:07'),
                      (7, 10, '11:09'),
                      (7, 11, '11:11'),
                      (7, 12, '11:14'),
                      (7, 13, '11:16'),
                      (7, 14, '11:18'),
                      (7, 15, '11:24'),
                      (7, 16, '11:26'),
                      (7, 17, '11:35'),
                      (7, 18, '11:39'),
                      (7, 19, '11:42'),
                      (7, 20, '11:45'),
                      (7, 21, '11:48'),
                      (7, 22, '11:52'),
                      (7, 23, '11:54'),
                      (7, 24, '11:56'),
                      (7, 25, '11:59'),
                      (7, 26, '12:01'),
                      (7, 27, '12:05'),

                      (8, 1, '10:56'),
                      (8, 2, '10:58'),
                      (8, 3, '11:01'),
                      (8, 4, '11:03'),
                      (8, 5, '11:06'),
                      (8, 6, '11:08'),
                      (8, 7, '11:11'),

                      (9, 7, '11:17'),
                      (9, 8, '11:20'),
                      (9, 9, '11:22'),
                      (9, 10, '11:24'),
                      (9, 11, '11:26'),
                      (9, 12, '11:29'),
                      (9, 13, '11:31'),
                      (9, 14, '11:33'),
                      (9, 15, '11:39'),
                      (9, 16, '11:41'),
                      (9, 17, '11:50'),
                      (9, 18, '11:54'),
                      (9, 19, '11:57'),
                      (9, 20, '12:00'),
                      (9, 21, '12:03'),
                      (9, 22, '12:07'),
                      (9, 23, '12:09'),
                      (9, 24, '12:11'),
                      (9, 25, '12:14'),
                      (9, 26, '12:16'),
                      (9, 27, '12:20'),

                      (10, 1, '11:11'),
                      (10, 2, '11:13'),
                      (10, 3, '11:16'),
                      (10, 4, '11:18'),
                      (10, 5, '11:21'),
                      (10, 6, '11:23'),
                      (10, 7, '11:26'),

                      (20, 27, '10:19'),
                      (20, 26, '10:21'),
                      (20, 25, '10:23'),
                      (20, 24, '10:26'),
                      (20, 23, '10:28'),
                      (20, 22, '10:32'),
                      (20, 21, '10:34'),
                      (20, 20, '10:38'),
                      (20, 19, '10:42'),
                      (20, 18, '10:46'),
                      (20, 17, '10:48'),
                      (20, 16, '10:57'),
                      (20, 15, '11:00'),
                      (20, 14, '11:03'),
                      (20, 13, '11:05'),
                      (20, 12, '11:08'),
                      (20, 11, '11:10'),
                      (20, 10, '11:12'),
                      (20, 9, '11:14'),
                      (20, 8, '11:17'),
                      (20, 7, '11:20'),

                      (21, 7, '11:31'),
                      (21, 6, '11:34'),
                      (21, 5, '11:37'),
                      (21, 4, '11:39'),
                      (21, 3, '11:41'),
                      (21, 2, '11:44'),
                      (21, 1, '11:48'),

                      (22, 27, '10:34'),
                      (22, 26, '10:36'),
                      (22, 25, '10:38'),
                      (22, 24, '10:41'),
                      (22, 23, '10:43'),
                      (22, 22, '10:47'),
                      (22, 21, '10:49'),
                      (22, 20, '10:53'),
                      (22, 19, '10:57'),
                      (22, 18, '11:01'),
                      (22, 17, '11:03'),
                      (22, 16, '11:12'),
                      (22, 15, '11:15'),
                      (22, 14, '11:18'),
                      (22, 13, '11:20'),
                      (22, 12, '11:23'),
                      (22, 11, '11:25'),
                      (22, 10, '11:27'),
                      (22, 9, '11:29'),
                      (22, 8, '11:32'),
                      (22, 7, '11:35'),

                      (23, 18, '11:15'),
                      (23, 15, '11:28'),
                      (23, 8, '11:37'),
                      (23, 7, '11:40'),
                      (23, 1, '11:52'),

                      (24, 7, '11:46'),
                      (24, 6, '11:49'),
                      (24, 5, '11:52'),
                      (24, 4, '11:54'),
                      (24, 3, '11:56'),
                      (24, 2, '11:59'),
                      (24, 1, '12:03'),

                      (25, 27, '10:49'),
                      (25, 26, '10:51'),
                      (25, 25, '10:53'),
                      (25, 24, '10:56'),
                      (25, 23, '10:58'),
                      (25, 22, '11:02'),
                      (25, 21, '11:04'),
                      (25, 20, '11:08'),
                      (25, 19, '11:12'),
                      (25, 18, '11:16'),
                      (25, 17, '11:18'),
                      (25, 16, '11:27'),
                      (25, 15, '11:30'),
                      (25, 14, '11:33'),
                      (25, 13, '11:35'),
                      (25, 12, '11:38'),
                      (25, 11, '11:40'),
                      (25, 10, '11:42'),
                      (25, 9, '11:44'),
                      (25, 8, '11:47'),
                      (25, 7, '11:50'),

                      (26, 7, '12:01'),
                      (26, 6, '12:04'),
                      (26, 5, '12:07'),
                      (26, 4, '12:09'),
                      (26, 3, '12:11'),
                      (26, 2, '12:14'),
                      (26, 1, '12:18'),

                      (27, 27, '11:04'),
                      (27, 26, '11:06'),
                      (27, 25, '11:08'),
                      (27, 24, '11:11'),
                      (27, 23, '11:13'),
                      (27, 22, '11:17'),
                      (27, 21, '11:19'),
                      (27, 20, '11:23'),
                      (27, 19, '11:27'),
                      (27, 18, '11:31'),
                      (27, 17, '11:33'),
                      (27, 16, '11:42'),
                      (27, 15, '11:45'),
                      (27, 14, '11:48'),
                      (27, 13, '11:50'),
                      (27, 12, '11:53'),
                      (27, 11, '11:55'),
                      (27, 10, '11:57'),
                      (27, 9, '11:59'),
                      (27, 8, '12:02'),
                      (27, 7, '12:05'),

                      (28, 18, '11:45'),
                      (28, 15, '11:58'),
                      (28, 8, '12:08'),
                      (28, 7, '12:11'),
                      (28, 1, '12:25'),

                      (29, 7, '12:16'),
                      (29, 6, '12:19'),
                      (29, 5, '12:22'),
                      (29, 4, '12:24'),
                      (29, 3, '12:26'),
                      (29, 2, '12:29'),
                      (29, 1, '12:33'),

                      (30, 27, '11:19'),
                      (30, 26, '11:21'),
                      (30, 25, '11:23'),
                      (30, 24, '11:26'),
                      (30, 23, '11:28'),
                      (30, 22, '11:32'),
                      (30, 21, '11:34'),
                      (30, 20, '11:38'),
                      (30, 19, '11:42'),
                      (30, 18, '11:46'),
                      (30, 17, '11:48'),
                      (30, 16, '11:57'),
                      (30, 15, '12:00'),
                      (30, 14, '12:03'),
                      (30, 13, '12:05'),
                      (30, 12, '12:08'),
                      (30, 11, '12:10'),
                      (30, 10, '12:12'),
                      (30, 9, '12:14'),
                      (30, 8, '12:17'),
                      (30, 7, '12:20'),

                      (31, 1, '10:04'),
                      (31, 7, '10:14'),
                      (31, 8, '10:17'),
                      (31, 15, '10:27'),
                      (31, 18, '10:40'),

                      (32, 1, '10:10'),
                      (32, 2, '10:12'),
                      (32, 3, '10:15'),
                      (32, 4, '10:17'),
                      (32, 5, '10:20'),
                      (32, 6, '10:22'),
                      (32, 7, '10:25'),

                      (33, 7, '10:29'),
                      (33, 8, '10:32'),
                      (33, 9, '10:34'),
                      (33, 10, '10:37'),
                      (33, 11, '10:39'),
                      (33, 12, '10:41'),
                      (33, 13, '10:44'),
                      (33, 14, '10:46'),
                      (33, 15, '10:51'),
                      (33, 16, '10:53'),
                      (33, 17, '11:03'),
                      (33, 18, '11:06'),
                      (33, 19, '11:09'),
                      (33, 20, '11:12'),
                      (33, 21, '11:15'),
                      (33, 22, '11:19'),
                      (33, 25, '11:25'),
                      (33, 26, '11:27'),
                      (33, 27, '11:31'),

                      (34, 1, '10:26'),
                      (34, 2, '10:28'),
                      (34, 3, '10:31'),
                      (34, 4, '10:33'),
                      (34, 5, '10:36'),
                      (34, 6, '10:38'),
                      (34, 7, '10:41'),

                      (35, 1, '10:34'),
                      (35, 7, '10:44'),
                      (35, 8, '10:47'),
                      (35, 15, '10:57'),
                      (35, 18, '11:10'),

                      (36, 1, '10:40'),
                      (36, 2, '10:42'),
                      (36, 3, '10:45'),
                      (36, 4, '10:47'),
                      (36, 5, '10:50'),
                      (36, 6, '10:52'),
                      (36, 7, '10:55'),

                      (37, 7, '10:59'),
                      (37, 8, '11:02'),
                      (37, 9, '11:04'),
                      (37, 10, '11:07'),
                      (37, 11, '11:09'),
                      (37, 12, '11:11'),
                      (37, 13, '11:14'),
                      (37, 14, '11:16'),
                      (37, 15, '11:21'),
                      (37, 16, '11:21'),
                      (37, 17, '11:33'),
                      (37, 18, '11:36'),
                      (37, 19, '11:39'),
                      (37, 20, '11:42'),
                      (37, 21, '11:45'),
                      (37, 22, '11:49'),
                      (37, 25, '11:55'),
                      (37, 26, '11:57'),
                      (37, 27, '12:01'),

                      (38, 1, '10:56'),
                      (38, 2, '10:58'),
                      (38, 3, '11:01'),
                      (38, 4, '11:02'),
                      (38, 5, '11:06'),
                      (38, 6, '11:08'),
                      (38, 7, '11:11'),

                      (39, 1, '11:04'),
                      (39, 7, '11:14'),
                      (39, 8, '11:17'),
                      (39, 15, '11:27'),
                      (39, 18, '11:40'),

                      (40, 1, '11:10'),
                      (40, 2, '11:12'),
                      (40, 3, '11:15'),
                      (40, 4, '11:17'),
                      (40, 5, '11:20'),
                      (40, 6, '11:22'),
                      (40, 7, '11:25'),

                      (41, 27, '09:58'),
                      (41, 26, '10:00'),
                      (41, 25, '10:02'),
                      (41, 22, '10:10'),
                      (41, 21, '10:12'),
                      (41, 20, '10:16'),
                      (41, 19, '10:20'),
                      (41, 18, '10:24'),
                      (41, 17, '10:26'),
                      (41, 16, '10:36'),
                      (41, 15, '10:39'),
                      (41, 14, '10:42'),
                      (41, 13, '10:44'),
                      (41, 12, '10:47'),
                      (41, 11, '10:49'),
                      (41, 10, '10:51'),
                      (41, 9, '10:53'),
                      (41, 8, '10:54'),
                      (41, 7, '10:58'),

                      (42, 7, '11:02'),
                      (42, 6, '11:05'),
                      (42, 5, '11:08'),
                      (42, 4, '11:10'),
                      (42, 3, '11:12'),
                      (42, 2, '11:15'),
                      (42, 1, '11:19'),

                      (43, 18, '10:45'),
                      (43, 15, '10:58'),
                      (43, 8, '11:07'),
                      (43, 7, '11:10'),
                      (43, 1, '11:22'),

                      (44, 7, '11:16'),
                      (44, 6, '11:19'),
                      (44, 5, '11:22'),
                      (44, 4, '11:24'),
                      (44, 3, '11:26'),
                      (44, 2, '11:29'),
                      (44, 1, '11:33'),

                      (45, 27, '10:28'),
                      (45, 26, '10:30'),
                      (45, 25, '10:32'),
                      (45, 22, '10:40'),
                      (45, 21, '10:42'),
                      (45, 20, '10:46'),
                      (45, 19, '10:50'),
                      (45, 18, '10:54'),
                      (45, 17, '10:56'),
                      (45, 16, '11:06'),
                      (45, 15, '11:09'),
                      (45, 14, '11:12'),
                      (45, 13, '11:14'),
                      (45, 12, '11:17'),
                      (45, 11, '11:19'),
                      (45, 10, '11:21'),
                      (45, 9, '11:23'),
                      (45, 8, '11:25'),
                      (45, 7, '11:28'),

                      (46, 7, '11:32'),
                      (46, 6, '11:35'),
                      (46, 5, '11:38'),
                      (46, 4, '11:40'),
                      (46, 3, '11:42'),
                      (46, 2, '11:45'),
                      (46, 1, '11:49'),

                      (47, 18, '11:15'),
                      (47, 15, '11:28'),
                      (47, 8, '11:37'),
                      (47, 7, '11:40'),
                      (47, 1, '11:52'),

                      (48, 7, '11:46'),
                      (48, 6, '11:49'),
                      (48, 5, '11:52'),
                      (48, 4, '11:54'),
                      (48, 3, '11:56'),
                      (48, 2, '11:59'),
                      (48, 1, '12:03'),

                      (49, 27, '10:58'),
                      (49, 26, '11:00'),
                      (49, 25, '11:02'),
                      (49, 22, '11:10'),
                      (49, 21, '11:12'),
                      (49, 20, '11:16'),
                      (49, 19, '11:20'),
                      (49, 18, '11:24'),
                      (49, 17, '11:26'),
                      (49, 16, '11:36'),
                      (49, 15, '11:39'),
                      (49, 14, '11:42'),
                      (49, 13, '11:44'),
                      (49, 12, '11:47'),
                      (49, 11, '11:49'),
                      (49, 10, '11:51'),
                      (49, 9, '11:53'),
                      (49, 8, '11:55'),
                      (49, 7, '11:58'),

                      (50, 7, '12:02'),
                      (50, 6, '12:05'),
                      (50, 5, '12:08'),
                      (50, 4, '12:10'),
                      (50, 3, '12:12'),
                      (50, 2, '12:15'),
                      (50, 1, '12:19')
                      ])

    conn.executemany('INSERT INTO Trackwork (Message_ID, Line_ID, Start_Date, End_Date, Message) VALUES (?, ?, ?, ?, ?)',
                     [(1, 1, '2018-06-16 02:00', '2018-06-18 02:00',
                      'Buses replace trains between Hornsby and Strathfield via Eastwood.'),
                     (2, 2, '2018-05-16 02:00', '2018-05-17 02:00',
                      'Buses replace trains between City and Cronulla via Airport.'),
                     (3, 3, '2018-07-16 02:00', '2018-07-19 02:00',
                      'Buses replace trains between Ashfield and Parramatta via Strathfield.'),
                     (4, 4, '2018-08-16 02:00', '2018-08-16 02:00',
                      'Buses replace trains between Lidcombe and Bankstown via Fairfield.')])

    conn.commit()
    # Load Line names in to lines list
    cur_l = conn.execute('SELECT Line_Name FROM Line')
    all_l_rec = cur_l.fetchall()
    for rec in all_l_rec:
        for e in rec:
            lines.append(e)

    # load station names in to the station list
    cur_sta = conn.execute('SELECT Station_Name FROM Station')
    all_rec = cur_sta.fetchall()
    for e_rec in all_rec:
        for e in e_rec:
            stations.append(e)
    print('===================================================================')
    print(textwrap.fill('*** Welcome to Sydney Train' + '\'s' + ' text-based rail' \
                  ' service.' + '\n' + 'This service will help you' \
                  ' finding convenient ways to travel ' + '\n' + 'by' \
                  ' asking you a number of questions.' + '\n' + 'You can ' \
                  + '\'' + 'quit' + '\'' + ' the conversation anytime. ***'))
    print('===================================================================')
    return conn  # to the main


def sql_query_timetable(conn, query):

    # ------------------------------------------------------------
    #                      SQL query: Timetable
    # ------------------------------------------------------------

    sql = "SELECT '" + query['FROM'] + "', x.Departure_Time,'" + query['TO'] + "'," \
        " strftime('%H:%M',datetime(y.Departure_Time, '-1 minute'))" \
        " FROM   Schedule x, Schedule y" \
        " WHERE  x.Station_ID = (SELECT x.Station_ID FROM Station x" \
        " WHERE  x.Station_Name = '" + query[
        'FROM'] + "')" \
            " AND EXISTS (SELECT y.Station_ID" \
            " WHERE  y.Train_ID = x.Train_ID" \
            " AND y.Station_ID = (SELECT Station_ID FROM Station" \
            " WHERE  Station_Name = '" + query['TO'] + "')" \
                        " AND  x.Departure_Time < y.Departure_Time)" \
                        " AND (SELECT Part_Of_Week" \
                        " FROM   Train" \
                        " WHERE  Train_ID = x.Train_ID) = '" + query[
              'WEEKDAY_OR_WEEKEND'] + "'" \
              " ORDER BY" \
              " ABS(strftime('%s', x.Departure_Time) - strftime('%s','" + query[
              'TIME'] + "')) ASC;"

    cursor1 = conn.execute(sql)

    return cursor1


    # ------------------------------------------------------------
    #                      SQL query: Trackwork
    # ------------------------------------------------------------

def sql_query_track_work(conn, u_info):
    # ------------------------------------------------------------
    #                      SQL query: Track-work
    # ------------------------------------------------------------

    cursor2 = conn.execute("SELECT Line_Name, Start_Date, End_Date, Message "
                            "FROM  Trackwork x, Line y " 
                            "WHERE x.Line_ID = y.LINE_ID AND Line_Name = '" + u_info['LINE'] + "' AND "
                            "(strftime( '%s', Start_Date ) <= strftime( '%s', '2017-09-16 10:00') AND "
                            "strftime( '%s', End_Date )   >= strftime( '%s', '2017-09-16 10:00') )")

    for row in cursor2:
        print('************************************************ >> TRACKWORK <<  ********************************************************')
        print(row)
        print('************************************************ >>    END    <<  ********************************************************')
    print('\n')


def scroll_data_set(lst_rec):  # record navigation

    # ----- scrolling purpose variables -----
    pos = 0
    changed_msg = ''
    next_rec = True
    default_res = True
    # ---------------------------------------

    tpl_count = len(lst_rec)  # get the total no.s of records
    rec = lst_rec

    try:

        while next_rec:

            if rec is not None:  # assuming record set is not empty

                if default_res:
                    res = input('Computer: Let me see! I have a train leaving ' + str(rec[pos][0]) +
                                ' at ' + str(rec[pos][1]) + ' and arriving at ' + str(rec[pos][3]) +
                                '. Would you like an earlier or later train?\n')
                else:
                    res = input(changed_msg)

                if res.lower() == 'earlier':

                    if pos != 0:
                        pos = pos - 1
                        default_res = True
                    else:
                        changed_msg = 'Computer: Sorry! This is the earliest one. Would you like a later one?\n'
                        default_res = False

                elif res.lower() == 'later':

                    count = tpl_count - 1
                    if pos != count:
                        pos = pos + 1
                        default_res = True
                    else:
                        changed_msg = 'Compuer: Sorry! This is the last train. Would you like an earlier one instead?[Type: Earlier]\n'
                        default_res = False

                elif res.lower() == 'no':
                    return 0

                elif res.lower() == 'help':
                    return 0
                else:
                    changed_msg = 'Computer: Please Enter either ' + '\'' + 'Earlier' + '\'' + ' , ' + '\'' + 'Later' + '\'' + ' or ' + '\'' + 'No' + '\'' + ' to quit.\n'
                    default_res = False

    except Exception as e:

           print('Error from scroll_data_set() :', e)


def timetable_ques():  # >> KEY QUESTIONS <<

    t_tbl = {'FROM':'Computer: What station would you like to leave from?\n',
             'TO':'Computer: Where are you travelling to?\n',
             'WEEKDAY_OR_WEEKEND':'Computer: Do you want to travel on a weekday or on a weekend?\n',
             'TIME': 'Computer: What time would you like to depart?\n'
             }
    return t_tbl


def track_w_ques():  # >> KEY QUESTIONS <<

    tw_ques = {'LINE':'Computer: On what line are you planning to travel on?\n',
               'T_DAY':'Computer: On what day will you be travelling??\n',
               'T_TIME':'Computer: At what time would you like to travel?\n'
               }
    return tw_ques


def find_line(search_text, saved_lines):

    try:
        s_txt = search_text.title()
        svd_ln = saved_lines

        for ln in svd_ln:  # search each station in the input text
            m_word = re.search(ln, s_txt)
            if m_word is not None:
                return m_word
    except Exception as e:
        print('find_line() -> Please check parameter [search_text]:', e)


def find_station(search_text, saved_stations):

    try:
        s_txt = search_text.title()
        svd_stations = saved_stations

        for stn in svd_stations:  # search each station in the input text
            m_word = re.search(stn, s_txt)
            if m_word is not None:
                return m_word
    except Exception as e:
        print('find_station() -> Please check parameter [search_text]:', e)


def next_dow(d, days):

    while d.weekday() not in days:
        d += datetime.timedelta(1)
    return d


def find_dow(text):  # finds the valid day of the week
    try:
        wk_days = []
        days = [0, 1, 2, 3, 4, 5, 6]
        for e in text.split():
            word = e.title()
            out_put = re.findall(r"day\b", word)
            if len(out_put) != 0:
                for d in days:
                    if calendar.day_name[d] == word:
                        wk_days.append(word)
        return wk_days
    except Exception as e:
            print(e)


def confirm_day(sentence):  # of the week and week[day/end]

    try:
        text = sentence.lower()
        match = re.search(r'(weekend)|(weekday)|(week day)|(week end)', text)
        not_confirmed = True
        if match is not None:
            while not_confirmed:
                ans_day = input('Computer: which day on the ' + match.group() + ' you would like to travel?\n')
                r = re.search(r"(mon|tues|wednes|thurs|fri|satur|sun)day", ans_day.lower())
                if r is not None:
                    d = r.group().title()
                    if len(find_dow(r.group())) != 0:
                        dt = next_dow(datetime.date.today(), (dow[find_dow(r.group())[0]], dow[d]))
                        print('-----------------------------------------')
                        print('Travelling on ' + ans_day.title() + ', ' + dt.strftime('%d %b %Y'))
                        print('-----------------------------------------')
                        return [1, match.group().replace(' ', '')] # removing gap between [week day]
                    else:
                        not_confirmed = True  # repeat loop until user enters correct format day of the week [___day]
                else:
                    print('Please follow the day format Mon[day]')
                    not_confirmed = True # as above
        return [0] # return false if match object neither weekend nor weekday or vise versa

    except Exception as e:
            print('from Function: confirm_day()', e)

def check_time(res):  # validate time format [HH:MM]

       try:
           tm = re.search(r'([1-9]|1[012]):[0-5][0-9]?', res)
           resp = input('Computer: Do you like to travel at ' + tm.string + '? [Type Yes/No]\n')
           if resp.lower() == 'yes':
              return True
       except AttributeError:
           print('Hint: Please Enter Time in 24hrs HH:MM Format')

# ----------------------------
#       Timetable Questions
# -----------------------------


def process_timetable():  # Returns user query

    q_bank = timetable_ques()  # load pre-defined built-in questions
    store_ans.update({'OPERATION': 'TIMETABLE'})  # mark dict as timetable object

    for each_q_key in q_bank:

        process_not_completed = True  # a process of mapping user responses with question_keys

        try:

            while process_not_completed:

                sentence = input(q_bank[each_q_key])  # get user response using same key'''

                #  -------------------------------------------------------------------------------
                #  Mapping starts here. Each loop question meets one of the 4 conditions down below
                #  -------------------------------------------------------------------------------

                if each_q_key == 'FROM':

                    station = find_station(sentence, stations)
                    if station is not None:
                        store_ans.update({each_q_key: station.group()})  # store name of the station
                        process_not_completed = False  # get the next question from the bank
                    else:
                         if sentence.lower() == 'quit':
                            exit()

                elif each_q_key == 'TO':

                    station = find_station(sentence, stations)

                    if station is not None:
                        if store_ans['FROM'] != station.group():
                            store_ans.update({each_q_key: station.group()})
                            process_not_completed = False
                        else:
                            print('Computer: Oops! Sorry <From and To> can not be the same station...')
                            process_not_completed = True
                    else:
                         if sentence.lower() == 'quit':
                            exit()

                elif each_q_key == 'WEEKDAY_OR_WEEKEND':

                    c_day = confirm_day(sentence)  # which day of the week?

                    if c_day[0] != 0:

                       if c_day[0] == 1 and c_day[1] == 'weekend':  # input validation
                          store_ans.update({each_q_key: 'WE'})
                       elif c_day[0] == 1 and c_day[1] == 'weekday':
                          store_ans.update({each_q_key: 'WD'})
                       process_not_completed = False
                    else:
                      process_not_completed = True
                      if sentence.lower() == 'quit':
                       exit()

                elif each_q_key == 'TIME':

                    if check_time(sentence):
                        store_ans.update({each_q_key: sentence.upper()})
                        process_not_completed = False
                    else:
                         if sentence.lower() == 'quit':
                            exit()

        except Exception as err:

                print('from Function: process_timetable():', err)
    return store_ans


def process_track_work():

    q_bank = track_w_ques()  # load pre-defined built-in questions
    store_tw_ans.update({'OPERATION': 'TRACK_WORK'})  # mark dict as track-work object

    for each_q_key in q_bank:

        process_not_completed = True

        try:

            while process_not_completed:

                sentence = input(q_bank[each_q_key])  # ask series of questions

                # -------------------------------------------------------------------------------
                #  Mapping starts here. Each loop question meets one of the 4 conditions down below
                #  -------------------------------------------------------------------------------

                if each_q_key == 'LINE':

                    line = find_line(sentence, lines)
                    if line is not None:
                        store_tw_ans.update({each_q_key: line.group()})  # store name of the line
                        process_not_completed = False  # get the next question from the bank
                    else:
                        print('Computer: Please enter one of the following lines: [Northern Line]..[Southern Line]..[Western Line]..[Bankstown Line]\n')
                        process_not_completed = True

                elif each_q_key == 'T_DAY':

                    if sentence is not None:
                        store_tw_ans.update({each_q_key: sentence})  # store day
                        process_not_completed = False  # get the next question from the bank

                elif each_q_key == 'T_TIME':

                    if check_time(sentence):
                        store_ans.update({each_q_key: sentence.upper()})
                        process_not_completed = False

        except Exception as err:
                print('from Function: process_track_work():', err)

    return store_tw_ans  # Returns user query


def switch_board():  # Returns user query to the main()

    # -------------------------------------------------------------------
    #             Main dashboard (a. Timetable b. Track-work)
    # -------------------------------------------------------------------

    user_info = {}
    run_program = True

    while run_program:  # only one output from the loop

        response = input(qs_type_1[str(random.randint(1, 5))]) # random msgs from [qs_type_1]

        if response is not None:
            if response.lower() == 'timetable':
                user_info = process_timetable()
                run_program = False

            elif response.lower() == 'trackwork':
                user_info = process_track_work()
                run_program = False

            elif response.lower() == 'help':
                #store_ans.update({'STATUS': 'HELP'})
                user_info.update({'OPERATION': 'HELP'})
                return user_info

            elif response.lower()== 'quit':
                user_info.update({'OPERATION': 'QUIT'})
                return user_info

    return user_info

if __name__ == '__main__':

    repeat_process = True  # until unless user says 'No'
    conn = activate_db() # Load cityRail database

    while repeat_process:

        u_info = switch_board()  # receives either [timetable] or [track-work] info from user
        print('\n')
        print('---------------------------------------------------- AI Info: ------------------------------------------------------------')

        if u_info['OPERATION'] == 'TIMETABLE':

            cursor_r = sql_query_timetable(conn, u_info)  # Get record set
            l_store = []
            for r in cursor_r:
                l_store.append(r)               # Copy record set to list
            if scroll_data_set(l_store) == 0:   # Navigate result set

                print('......................................... Thanks for using CityRail AI ...................................................')
                print('\n')
                store_ans.clear()               # Reset memory
                u_info.clear()                  # Reset memory

        elif u_info['OPERATION'] == 'TRACK_WORK':

            sql_query_track_work(conn, u_info)  # Run query
            store_tw_ans.clear()                # Reset memory
            u_info.clear()                      # Reset memory
            print('\n')

        elif u_info['OPERATION'] == 'HELP':
            print('  ..................................Please Wait. Someone Will Assist you Shortly..........................................')
            print('--------------------------------------------------- Good bye: ------------------------------------------------------------')
            exit()

        elif u_info['OPERATION'] == 'QUIT':
            conn.close()  # close the connection
            print('   ........................................Thanks for using CityRail AI...................................................')
            print('--------------------------------------------------- Good bye: ------------------------------------------------------------')
            exit()

        #  User input for next action
        response = input(qs_type_2[str(random.randint(1, 5))])  # random msgs from [qs_type_2]

        if response.lower() == 'no':
            conn.close() # close the connection
            print('--------------------------------------------------- Good bye: ------------------------------------------------------------')
            exit()

        elif response.lower() == 'yes':
            repeat_process = True
