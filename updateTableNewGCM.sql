-- plan
alter table gcm_plan add column visible_client boolean NULL default "1";

-- invoice

Alter table gcm_invoice add observation text NULL;
