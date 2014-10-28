-- settings
-- ADMINS_REGISTRATION = ['webmaster@gestorpsi.com.br','tsm@gestorpsi.com.br','ozp@gestorpsi.com.br',]
-- URL_HOME, URL_APP, SIGNATURE, URL_DEMO

-- plan
alter table gcm_plan add column visible_client boolean NULL default "1";

-- invoice
Alter table gcm_invoice add payment_detail text NULL;
Alter table gcm_invoice add bank varchar(3) NULL;

Alter table gcm_invoice add payment_type_id integer NOT NULL;
-- ALTER TABLE `gcm_invoice` ADD CONSTRAINT `payment_type_id_refs_id_7e5b53be` FOREIGN KEY (`payment_type_id`) REFERENCES `gcm_paymenttype` (`id`);
CREATE INDEX `gcm_invoice_19543b21` ON `gcm_invoice` (`payment_type_id`);

Alter table gcm_invoice add start_date date NOT NULL;
Alter table gcm_invoice add end_date date NOT NULL;

Alter table gcm_invoice drop billet_url;
Alter table gcm_invoice drop due_date;

-- organization
Alter table organization_organization add suspension boolean NULL default False;
Alter table organization_organization add suspension_reason text NULL;

Alter table organization_organization add time_slot_schedule varchar(2) NOT NULL;

COMMIT;
