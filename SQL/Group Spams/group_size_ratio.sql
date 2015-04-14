use ciao;
/*
CREATE TABLE tmp_products(
product_id integer
);

CREATE TABLE Group_size_ratio_sup3(
group_id integer,
product_id integer,
gsr_val decimal(8,6)
);
*/

# DROP PROCEDURE getReviewedProducts;

# TRUNCATE TABLE Group_size_ratio_sup3

DELIMITER $$
CREATE PROCEDURE getReviewedProducts()
BEGIN
	DECLARE row_num INT DEFAULT 1;
    DECLARE group_num INT DEFAULT 1;
    DECLARE max_group_num INT DEFAULT 0;
    DECLARE max_row_num INT DEFAULT 0;

    SET max_group_num = (select max(group_id) from groups_sup3);
    
	WHILE group_num <= max_group_num DO
		
        TRUNCATE TABLE tmp_products;
        
        SET @num = group_num;
        
        PREPARE stmt1 FROM 'select max(user_num) INTO @num1 from groups_sup3 where group_id = ?';
        EXECUTE stmt1 USING @num; 
		SET max_row_num = @num1;
		
        # select max_row_num;
        
        SET @num2 = row_num;
			
		PREPARE stmt FROM 'insert into tmp_products
								select product_id 
								from review 
								where user_id IN (select user_id 
												from groups_sup3 
												where group_id = ? and user_num = ?)';
		EXECUTE stmt USING @num, @num2;
		# select 'inserted 1st time';
        SET row_num = row_num + 1;
        
        WHILE row_num <= max_row_num DO
        
			SET @num2 = row_num;
			
            SET SQL_SAFE_UPDATES = 0;
            
			PREPARE stmt FROM 'delete from tmp_products
								where product_id NOT IN (
												select product_id 
												from review 
												where user_id = (select user_id 
																from groups_sup3 
																where group_id = ? and user_num = ?))';
            EXECUTE stmt USING @num, @num2;
            # select 'deleting';
            
			SET row_num = row_num + 1;
        END WHILE;
        
		PREPARE stmt2 FROM 'insert into group_size_ratio_sup3(group_id, product_id) select ?, product_id from tmp_products;';
            
        EXECUTE stmt2 USING @num;
        # select 'inserting in main table';
        
		SET group_num = group_num + 1;
    END WHILE;
END$$
DELIMITER ;
/*
select *
from review
where user_id in (select user_id 
				from groups_sup3);
                
select distinct product_id
from review r
inner join groups_sup3 g
on r.user_id = g.user_id
where g.group_id = 221;

select *
from groups_sup3 limit 50;

*/