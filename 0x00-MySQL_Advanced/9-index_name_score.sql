-- Step 1: Import names.sql into your database

-- Step 2: Create the index
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
