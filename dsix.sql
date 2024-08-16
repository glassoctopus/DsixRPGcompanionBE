DELETE FROM DsixRPGcompanionBE_skill;

DELETE FROM DsixRPGcompanionBE_characterskill;

SELECT *
FROM DsixRPGcompanionBE_characterskill

-- Reset the auto-increment counter
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_character';
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_skill';
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_characterskill';


SELECT name 
FROM sqlite_master 
WHERE type='table';


SELECT skill_id, character_id, COUNT(*) AS count
FROM DsixRPGcompanionBE_characterskill
GROUP BY skill_id, character_id
HAVING COUNT(*) > 1;

