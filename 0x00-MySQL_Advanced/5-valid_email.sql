-- Step 1: Create the trigger
DELIMITER //

CREATE TRIGGER before_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has been changed
    IF OLD.email <> NEW.email THEN
        -- Reset the valid_email attribute
        SET NEW.valid_email = 0;
    END IF;
END;
//

DELIMITER ;
