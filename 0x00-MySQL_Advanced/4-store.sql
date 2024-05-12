-- Step 1: Create the trigger
CREATE TRIGGER update_orders BEFORE INSERT ON orders
FOR EACH ROW UPDATE items
SET quantity = quantity - NEW.quantity
WHERE name = NEW.item_name;
