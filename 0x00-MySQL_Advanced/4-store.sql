-- Step 1: Create the trigger
DELIMITER //

CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_quantity INT;

    -- Get the current quantity of the item
    SELECT quantity INTO item_quantity
    FROM items
    WHERE item_id = NEW.item_id;

    -- Update the quantity of the item after the order
    UPDATE items
    SET quantity = item_quantity - NEW.quantity
    WHERE item_id = NEW.item_id;
END;
//

DELIMITER ;
