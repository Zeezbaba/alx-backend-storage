-- a SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student
-- An average score can be a decimal
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
        DECLARE score_sum INT DEFAULT 0;
        DECLARE project_count INT DEFAULT 0;

        SELECT SUM(score) INTO score_sum
        FROM corrections
        WHERE corrections.user_id = user_id;

        SELECT COUNT(*) INTO project_count
        FROM corrections
        WHERE corrections.user_id = user_id;

        UPDATE users
        SET users.average_score = IF(project_count = 0, 0, score_sum / project_count)
        WHERE users.id = user_id;
END //
DELIMITER ;
