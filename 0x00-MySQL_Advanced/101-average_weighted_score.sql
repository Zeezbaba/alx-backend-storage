-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE user_id INT;
    DECLARE weighted_sum INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

    OPEN cur;

    get_users: LOOP
        FETCH cur INTO user_id;
        IF finished THEN
            LEAVE get_users;
        END IF;

        SET weighted_sum = 0;
        SET total_weight = 0;

        SELECT SUM(corrections.score * projects.weight) INTO weighted_sum
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        SELECT SUM(projects.weight) INTO total_weight
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        UPDATE users
        SET average_score = IF(total_weight = 0, 0, weighted_sum / total_weight)
        WHERE users.id = user_id;

    END LOOP get_users;

    CLOSE cur;
END //

DELIMITER ;
