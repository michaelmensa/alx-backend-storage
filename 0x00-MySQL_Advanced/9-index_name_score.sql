-- sql script that creates an idx idx_name_first_score on table names 
-- the first letter of name and the score.
CREATE INDEX idx_name_first_score ON names(name(1), score);
