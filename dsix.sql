
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

DELETE FROM DsixRPGcompanionBE_usergroup;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_usergroup';

DELETE FROM DsixRPGcompanionBE_usergroup_characters;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_usergroup_characters';

DELETE FROM DsixRPGcompanionBE_usergroup_users;
DELETE FROM sqlite_sequence WHERE name='DsixRPGcompanionBE_usergroup_users';


SELECT *

-- a little code returns all tables
SELECT name 
FROM sqlite_master 
WHERE type='table';

DROP TABLE IF EXISTS DsixRPGcompanionBE_user


SELECT skill_id, character_id, COUNT(*) AS count
FROM DsixRPGcompanionBE_characterskill
GROUP BY skill_id, character_id
HAVING COUNT(*) > 1;

SELECT skill_name, COUNT(skill_name) as occurrences
FROM DsixRPGcompanionBE_skill
GROUP BY skill_name
HAVING occurrences > 1;