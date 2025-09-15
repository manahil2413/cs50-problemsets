-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- All three witnesses mentioned about bakery
-- Also littering took place at 16:36
-- THEFT TOOK place at 10:15am


--  Checked the transcript of witnesses to get the idea of case
SELECT transcript
FROM interviews
WHERE day = 28 AND month = 7

-- NEW:
-- THEFT TIME: 10:15am
-- LOCATION (street) = Humphrey Street Bakery
-- Littering Time: 16:36

-- People who exited the bakery between 10:15-10:25 : barry,Vaneesa,Iman,Sofia,Luca,Diana,Kelsey,Bruce
SELECT DISTINCT name
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE activity = 'exit' AND day = 28 AND month=7 AND hour=10 AND minute >=15 AND minute<=25
);
-- People did call on the same day and present at bakery:Vaneese,Barry,Sofia,Diana,Kelsey,Bruce(4 calls)
SELECT people.name
FROM people
JOIN phone_calls ON phone_call.caller = people.phone_number
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.activity= 'exit' AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute>= 15 AND bakery_security_logs.minute<=25 AND
bakery_security_logs.day = 28 AND bakery_security_logs.month=7 AND phone_calls.month=7 AND phone_calls.day = 28;

-- People who made transaction, exited the bakery within 10 minutes of theft and made a phone call
SELECT DISTINCT people.name
FROM people
JOIN bank_accounts ON  bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
JOIN phone_calls ON phone_calls.caller =people.phone_number
WHERE atm_transactions.month = 7 AND atm_transactions.day= 28 AND atm_transactions.atm_location = 'Leggett Street' AND  bakery_security_logs.activity= 'exit'
 AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute>= 15 AND bakery_security_logs.minute<=25 AND
bakery_security_logs.day = 28 AND bakery_security_logs.month=7 AND phone_calls.month = 7 AND phone_calls.day = 28;

-- PRIME SUSPECT: Bruce and Diana (meet all these movement of thief)

-- PEOPLE WHO EXITED THE BAKERY BETWEEN 10:15 to 10:25 AND also took the flight From fiftyville: Sofia,Luca,Diana,Kelsey,Bruce
SELECT name
FROM people
WHERE passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = (
        SELECT id
        FROM flights
        WHERE month = 7 AND day = 29 AND origin_airport_id = (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville'
        )
        ORDER BY hour, minute

    )
)
AND license_plate IN (
    SELECT license_plate
    FROM bakery
    WHERE activity = 'exit'
      AND month = 7
      AND day = 28
      AND hour = 10
      AND minute BETWEEN 15 AND 25
);

-- DESTINATION AIRPORT OF PRIME SUSPECT
SELECT city
FROM airports
WHERE id IN (
      SELECT destination_airport_id
      FROM flights
      WHERE id IN (
          SELECT flight_id
          FROM passengers
          WHERE passport_number IN
            (
           SELECT passport_number
           FROM people
           WHERE name IN ('Diana','Bruce')
    )
)

)
SELECT people.name,airports.city
FROM people
JOIN passengers ON passenger.passport_number = people.passenger_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON flights.destination_airport_id = airports.id
WHERE people.name IN ('Bruce','Diana')

--  RESULT: name | destination city
--          Diana  Boston
--          Diana  Fiftyville
--          Bruce  New York
--          Bruce  Dallas
-- Diana is not the thief as she returned to Fiftyville

SELECT name
FROM people
WHERE phone_number IN (
   SELECT phone_number
   FROM phone_calls
   WHERE receiver = (
      SELECT phone_number
      FROM people
      WHERE name ='Bruce')
    OR
     caller = (
      SELECT phone_number
      FROM people
      WHERE name ='Bruce'
   )
AND day = 28 AND month =7
) AND name != 'Bruce';


