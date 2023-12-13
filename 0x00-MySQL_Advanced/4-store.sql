-- sql script that creates a trigger that decreases the
-- quantity of an item after adding a new order
-- Quantity in the table can be negative
DROP TRIGGER IF EXISTS aft_ins_order;
DELIMITER //
CREATE TRIGGER aft_ins_order
AFTER INSERT ON orders
FOR EACH ROW
    BEGIN
        UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
    END //
DELIMITER ;
