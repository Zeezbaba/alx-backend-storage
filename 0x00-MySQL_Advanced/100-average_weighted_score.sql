-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
-- Procedure ComputeAverageScoreForUser is taking 1 input:
--      user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
        DECLARE weighted_sum INT DEFAULT 0;
        DECLARE total_weight INT DEFAULT 0;

        SELECT SUM(corrections.score * projects.weight)
        INTO weighted_sum
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
END //
DELIMITER ;
