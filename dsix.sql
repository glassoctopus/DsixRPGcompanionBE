
-- kill all entries in the table
-- Reset the auto-increment counter
DELETE FROM DsixRPGcompanionBE_archetype;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_archetype';

DELETE FROM DsixRPGcompanionBE_character;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_character';

DELETE FROM DsixRPGcompanionBE_skill;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_skill';

DELETE FROM DsixRPGcompanionBE_characterskill;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_characterskill';

DELETE FROM DsixRPGcompanionBE_skillspecialization;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_skillspecialization';

SELECT *

-- a little code returns all tables
SELECT name 
FROM sqlite_master 
WHERE type='table';


SELECT skill_id, character_id, COUNT(*) AS count
FROM DsixRPGcompanionBE_characterskill
GROUP BY skill_id, character_id
HAVING COUNT(*) > 1;

SELECT skill_name, COUNT(skill_name) as occurrences
FROM DsixRPGcompanionBE_skill
GROUP BY skill_name
HAVING occurrences > 1;