--------------------- begin crypt_script.sql ---------------------

------------------- Creating gestorpsi_encrypt -------------------
CREATE OR REPLACE FUNCTION gestorpsi_get_key () RETURNS VARCHAR
AS $$
  try:
    return open('/home/gestorpsi/dev/gestorpsi/chave.key','r').readline().strip()
  except:
    raise Exception("Security Cryptography Error")
$$ LANGUAGE plpythonu;

------------------- Creating gestorpsi_encrypt -------------------
CREATE OR REPLACE FUNCTION gestorpsi_encrypt (to_be_encrypted VARCHAR) RETURNS VARCHAR
AS $$
  key_array = plpy.execute("SELECT gestorpsi_get_key() as key");
  key = [ (r["key"]) for r in key_array ][0]
  encrypted = plpy.execute("SELECT ENCODE(ENCRYPT('%s', '%s', 'bf'), 'hex') as secret" % (to_be_encrypted, key));
  return [ (r["secret"]) for r in encrypted ][0]
$$ LANGUAGE plpythonu;


------------------- Creating gestorpsi_decrypt -------------------
CREATE OR REPLACE FUNCTION gestorpsi_decrypt (to_be_decrypted VARCHAR) RETURNS VARCHAR
AS $$
  key_array = plpy.execute("SELECT gestorpsi_get_key() as key");
  key = [ (r["key"]) for r in key_array ][0]
  decrypted = plpy.execute("SELECT DECRYPT( DECODE('%s', 'hex'), '%s', 'bf' ) as secret" % (to_be_decrypted, key));
  return [ (r["secret"]) for r in decrypted ][0].decode('string_escape')
$$ LANGUAGE plpythonu;


------------------- Testing if functions was correctly installed -------------------
SELECT gestorpsi_encrypt('ABCDEF 1234567890 áéíóúç');
SELECT gestorpsi_decrypt('d15d09102bf10e14b1b14d4ae89cdb49788f6cbcefbb69bffe77683036c31623');


---- Now we'll have a sequence of:
---- DROP TABLE   - drop table created by syncdb django without cryptography
---- CREATE TABLE - create our own table prepared to store cryptographed data
---- CREATE VIEW  - create a view, that will be accessed by django like a ordinary table.
----                Here we'll use gestorpsi_decrypt function.
---- CREATE RULE  - create a rule to 'redirect' all action like INSERT/UPDATE/DELETE executed
----                in a view to our 'real' table. Here we'll use gestorpsi_encrypt function.

------------------------------------ Person App ------------------------------------
BEGIN;

DROP TABLE person_person CASCADE;

CREATE TABLE "person_person_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "name" varchar(256) NOT NULL,
    "nickname" varchar(256),
    "photo" varchar(100) NOT NULL,
    "birthDate" date,
    "birthPlace_id" integer REFERENCES "address_city" ("id") DEFERRABLE INITIALLY DEFERRED,
    "birthForeignCity" varchar(100),
    "birthForeignState" varchar(100),
    "birthForeignCountry" integer,
    "gender" varchar(1) NOT NULL,
    "maritalStatus_id" integer REFERENCES "person_maritalstatus" ("id") DEFERRABLE INITIALLY DEFERRED,
    "organization_id" varchar(36) REFERENCES "organization_organization" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE OR REPLACE VIEW person_person
  AS SELECT "id",
            gestorpsi_decrypt("name") as name,
            gestorpsi_decrypt("nickname") as nickname,
            "photo",
            "birthDate",
            "birthPlace_id",
            "birthForeignCity",
            "birthForeignState",
            "birthForeignCountry",
            "gender",
            "maritalStatus_id",
            "organization_id"
  FROM person_person_crypt;

CREATE OR REPLACE RULE rule_insert_person_person AS ON INSERT
    TO person_person
    DO INSTEAD
    INSERT INTO person_person_crypt VALUES
             (NEW."id",
              gestorpsi_encrypt(NEW."name"),
              gestorpsi_encrypt(NEW."nickname"),
              NEW."photo",
              NEW."birthDate",
              NEW."birthPlace_id",
              NEW."birthForeignCity",
              NEW."birthForeignState",
              NEW."birthForeignCountry",
              NEW."gender",
              NEW."maritalStatus_id",
              NEW."organization_id");

CREATE OR REPLACE RULE rule_update_person_person AS ON UPDATE
    TO person_person
    DO INSTEAD
    UPDATE person_person_crypt SET
        "name" = gestorpsi_encrypt(NEW."name"),
	"nickname" = gestorpsi_encrypt(NEW."nickname"),
	"photo" = NEW."photo",
	"birthDate" = NEW."birthDate",
	"birthPlace_id" = NEW."birthPlace_id",
	"birthForeignCity" = NEW."birthForeignCity",
        "birthForeignState" = NEW."birthForeignState",
	"birthForeignCountry" = NEW."birthForeignCountry",
	"gender" = NEW."gender", 
	"maritalStatus_id" = NEW."maritalStatus_id",
	"organization_id" = NEW."organization_id"
    WHERE "id" = OLD."id";


------------------------------------ Phone App ------------------------------------
DROP TABLE phone_phone CASCADE;

CREATE TABLE "phone_phone_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "area" varchar(16) NOT NULL,
    "phoneNumber" varchar(32) NOT NULL,
    "ext" varchar(16) NOT NULL,
    "phoneType_id" integer NOT NULL REFERENCES "phone_phonetype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);

CREATE OR REPLACE VIEW phone_phone
  AS SELECT "id",
            gestorpsi_decrypt("area") as "area", 
            gestorpsi_decrypt("phoneNumber") as "phoneNumber",
            gestorpsi_decrypt("ext") as "ext",
            "phoneType_id",
            "content_type_id",
            "object_id"
  FROM phone_phone_crypt;

CREATE OR REPLACE RULE rule_insert_phone_phone AS ON INSERT
    TO phone_phone
    DO INSTEAD
    INSERT INTO phone_phone_crypt VALUES
             (NEW."id",
              gestorpsi_encrypt(NEW."area"),
              gestorpsi_encrypt(NEW."phoneNumber"),
              gestorpsi_encrypt(NEW."ext"),
              NEW."phoneType_id",
              NEW."content_type_id",
              NEW."object_id");

CREATE OR REPLACE RULE rule_update_phone_phone AS ON UPDATE
    TO phone_phone
    DO INSTEAD
    UPDATE phone_phone_crypt SET
        "area" = gestorpsi_encrypt(NEW."area"),
	"phoneNumber" = gestorpsi_encrypt(NEW."phoneNumber"),
	"ext" = gestorpsi_encrypt(NEW."ext"),
	"phoneType_id" = NEW."phoneType_id",
	"content_type_id" = NEW."content_type_id",
	"object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_phone_phone AS ON DELETE
   TO phone_phone
   DO INSTEAD
   DELETE FROM phone_phone_crypt WHERE "id" = OLD."id";



------------------------------------ Address App ------------------------------------
DROP TABLE address_address CASCADE;

CREATE TABLE "address_address_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "addressPrefix" varchar(10) NOT NULL,
    "addressLine1" varchar(312) NOT NULL,
    "addressLine2" varchar(312) NOT NULL,
    "addressNumber" varchar(64) NOT NULL,
    "neighborhood" varchar(30) NOT NULL,
    "zipCode" varchar(64) NOT NULL,
    "addressType_id" integer NOT NULL REFERENCES "address_addresstype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "city_id" integer REFERENCES "address_city" ("id") DEFERRABLE INITIALLY DEFERRED,
    "foreignCountry_id" integer REFERENCES "address_country" ("id") DEFERRABLE INITIALLY DEFERRED,
    "foreignState" varchar(20) NOT NULL,
    "foreignCity" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);

CREATE OR REPLACE VIEW address_address
  AS SELECT "id",
            "addressPrefix",
            gestorpsi_decrypt("addressLine1") as "addressLine1", 
            gestorpsi_decrypt("addressLine2") as "addressLine2",
            gestorpsi_decrypt("addressNumber") as "addressNumber",
            "neighborhood",
            gestorpsi_decrypt("zipCode") as "zipCode",
            "addressType_id",
            "city_id",
            "foreignCountry_id",
            "foreignState",
            "foreignCity",
            "content_type_id",
            "object_id"
  FROM address_address_crypt;

CREATE OR REPLACE RULE rule_insert_address_address AS ON INSERT
    TO address_address
    DO INSTEAD
    INSERT INTO address_address_crypt VALUES
            (NEW."id",
             NEW."addressPrefix",
             gestorpsi_encrypt(NEW."addressLine1"),
             gestorpsi_encrypt(NEW."addressLine2"),
             gestorpsi_encrypt(NEW."addressNumber"),
             NEW."neighborhood",
             gestorpsi_encrypt(NEW."zipCode"),
             NEW."addressType_id",
             NEW."city_id",
             NEW."foreignCountry_id",
             NEW."foreignState",
             NEW."foreignCity",
             NEW."content_type_id",
             NEW."object_id");


CREATE OR REPLACE RULE rule_update_address_address AS ON UPDATE
    TO address_address
    DO INSTEAD
    UPDATE address_address_crypt SET
         "addressPrefix" = NEW."addressPrefix",
         "addressLine1" = gestorpsi_encrypt(NEW."addressLine1"),
         "addressLine2" = gestorpsi_encrypt(NEW."addressLine2"),
         "addressNumber" = gestorpsi_encrypt(NEW."addressNumber"),
         "neighborhood" = NEW."neighborhood",
         "zipCode" = gestorpsi_encrypt(NEW."zipCode"),
         "addressType_id" = NEW."addressType_id",
         "city_id" = NEW."city_id",
         "foreignCountry_id" = NEW."foreignCountry_id",
         "foreignState" = NEW."foreignState",
         "foreignCity" = NEW."foreignCity",
         "content_type_id" = NEW."content_type_id",
         "object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_address_address AS ON DELETE
   TO address_address
   DO INSTEAD
   DELETE FROM address_address_crypt WHERE "id" = OLD."id";




------------------------------------ Document App ------------------------------------
DROP TABLE document_document CASCADE;

CREATE TABLE "document_document_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "typeDocument_id" integer NOT NULL REFERENCES "document_typedocument" ("id") DEFERRABLE INITIALLY DEFERRED,
    "document" varchar(96) NOT NULL,
    "issuer_id" integer REFERENCES "document_issuer" ("id") DEFERRABLE INITIALLY DEFERRED,
    "state_id" integer REFERENCES "address_state" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);

CREATE OR REPLACE VIEW document_document
  AS SELECT "id", "typeDocument_id", gestorpsi_decrypt("document") as "document", "issuer_id", "state_id", "content_type_id", "object_id"
  FROM document_document_crypt;

CREATE OR REPLACE RULE rule_insert_document_document AS ON INSERT
    TO document_document
    DO INSTEAD
    INSERT INTO document_document_crypt VALUES
            (NEW."id",
             NEW."typeDocument_id",
             gestorpsi_encrypt(NEW."document"),
             NEW."issuer_id",
             NEW."state_id",
             NEW."content_type_id",
             NEW."object_id");

CREATE OR REPLACE RULE rule_update_document_document AS ON UPDATE
    TO document_document
    DO INSTEAD
    UPDATE document_document_crypt SET
          "typeDocument_id" = NEW."typeDocument_id",
          "document" = gestorpsi_encrypt(NEW."document"),
          "issuer_id" = NEW."issuer_id",
          "state_id" = NEW."state_id",
          "content_type_id" = NEW."content_type_id",
          "object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_document_document AS ON DELETE
   TO document_document
   DO INSTEAD
   DELETE FROM document_document_crypt WHERE "id" = OLD."id";




------------------------------------ Client App ------------------------------------
DROP TABLE client_client CASCADE;

CREATE TABLE "client_client_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "person_id" varchar(36) NOT NULL UNIQUE REFERENCES "person_person_crypt" ("id") DEFERRABLE INITIALLY DEFERRED,
    "idRecord" varchar(250) NOT NULL,
    "legacyRecord" varchar(250) NOT NULL,
    "healthDocument" varchar(250) NOT NULL,
    "admission_date" date,
    "referral_choice_id" integer REFERENCES "admission_admissionreferral" ("id") DEFERRABLE INITIALLY DEFERRED,
    "indication_choice_id" integer REFERENCES "admission_indication" ("id") DEFERRABLE INITIALLY DEFERRED,
    "clientStatus" varchar(1) NOT NULL,
    "comments" text NOT NULL
);

CREATE OR REPLACE VIEW client_client
  AS SELECT "id",
            "person_id",
            gestorpsi_decrypt("idRecord") as "idRecord",
            gestorpsi_decrypt("legacyRecord") as "legacyRecord",
            gestorpsi_decrypt("healthDocument") as "healthDocument",
            "admission_date",
            "referral_choice_id",
            "indication_choice_id",
            "clientStatus",
            "comments"
  FROM client_client_crypt;

CREATE OR REPLACE RULE rule_insert_client_client AS ON INSERT
    TO client_client
    DO INSTEAD
    INSERT INTO client_client_crypt VALUES
            (NEW."id",
             NEW."person_id",
             gestorpsi_encrypt(NEW."idRecord"),
             gestorpsi_encrypt(NEW."legacyRecord"),
             gestorpsi_encrypt(NEW."healthDocument"),
             NEW."admission_date",
             NEW."referral_choice_id",
             NEW."indication_choice_id",
             NEW."clientStatus",
             NEW."comments");

CREATE OR REPLACE RULE rule_update_client_client AS ON UPDATE
    TO client_client
    DO INSTEAD
    UPDATE client_client_crypt SET
             "person_id" = NEW."person_id",
             "idRecord" = gestorpsi_encrypt(NEW."idRecord"),
             "legacyRecord" = gestorpsi_encrypt(NEW."legacyRecord"),
             "healthDocument" = gestorpsi_encrypt(NEW."healthDocument"),
             "admission_date" = NEW."admission_date",
             "referral_choice_id" = NEW."referral_choice_id",
             "indication_choice_id" = NEW."indication_choice_id",
             "clientStatus" = NEW."clientStatus",
             "comments" = NEW."comments"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_client_client AS ON DELETE
   TO client_client
   DO INSTEAD
   DELETE FROM client_client_crypt WHERE "id" = OLD."id";



------------------------------------ Internet App: email ------------------------------------
DROP TABLE internet_email CASCADE;

CREATE TABLE "internet_email_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "email" varchar(256) NOT NULL,
    "email_type_id" integer NOT NULL REFERENCES "internet_emailtype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);

CREATE OR REPLACE VIEW internet_email
  AS SELECT "id",
            gestorpsi_decrypt("email") as "email",
            "email_type_id",
            "content_type_id",
            "object_id"
  FROM internet_email_crypt;

CREATE OR REPLACE RULE rule_insert_internet_email AS ON INSERT
    TO internet_email
    DO INSTEAD
    INSERT INTO internet_email_crypt VALUES
            (NEW."id",
             gestorpsi_encrypt(NEW."email"),
             NEW."email_type_id",
             NEW."content_type_id",
             NEW."object_id");

CREATE OR REPLACE RULE rule_update_internet_email AS ON UPDATE
    TO internet_email
    DO INSTEAD
    UPDATE internet_email_crypt SET
             "email" = gestorpsi_encrypt(NEW."email"),
             "email_type_id" = NEW."email_type_id",
             "content_type_id" = NEW."content_type_id",
             "object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_internet_email AS ON DELETE
   TO internet_email
   DO INSTEAD
   DELETE FROM internet_email_crypt WHERE "id" = OLD."id";


------------------------------------ Internet App: site ------------------------------------
DROP TABLE internet_site CASCADE;

CREATE TABLE "internet_site_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "description" varchar(256) NOT NULL,
    "site" varchar(232) NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);


CREATE OR REPLACE VIEW internet_site
  AS SELECT "id",
            gestorpsi_decrypt("description") as "description",
            gestorpsi_decrypt("site") as "site",
            "content_type_id",
            "object_id"
  FROM internet_site_crypt;

CREATE OR REPLACE RULE rule_insert_internet_site AS ON INSERT
    TO internet_site
    DO INSTEAD
    INSERT INTO internet_site_crypt VALUES
            (NEW."id",
             gestorpsi_encrypt(NEW."description"),
             gestorpsi_encrypt(NEW."site"),
             NEW."content_type_id",
             NEW."object_id");

CREATE OR REPLACE RULE rule_update_internet_site AS ON UPDATE
    TO internet_site
    DO INSTEAD
    UPDATE internet_site_crypt SET
             "description" = gestorpsi_encrypt(NEW."description"),
             "site" = gestorpsi_encrypt(NEW."site"),
             "content_type_id" = NEW."content_type_id",
             "object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_internet_site AS ON DELETE
   TO internet_site
   DO INSTEAD
   DELETE FROM internet_site_crypt WHERE "id" = OLD."id";



------------------------------------ Internet App: instantmessenger ------------------------------------

DROP TABLE internet_instantmessenger CASCADE;

CREATE TABLE "internet_instantmessenger_crypt" (
    "id" varchar(36) NOT NULL PRIMARY KEY,
    "identity" varchar(256) NOT NULL,
    "network_id" integer NOT NULL REFERENCES "internet_imnetwork" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" varchar(36) NOT NULL
);

CREATE OR REPLACE VIEW internet_instantmessenger
  AS SELECT "id",
            gestorpsi_decrypt("identity") as "identity",
            "network_id",
            "content_type_id",
            "object_id"
  FROM internet_instantmessenger_crypt;

CREATE OR REPLACE RULE rule_insert_internet_instantmessenger AS ON INSERT
    TO internet_instantmessenger
    DO INSTEAD
    INSERT INTO internet_instantmessenger_crypt VALUES
            (NEW."id",
             gestorpsi_encrypt(NEW."identity"),
             NEW."network_id",
             NEW."content_type_id",
             NEW."object_id");

CREATE OR REPLACE RULE rule_update_internet_instantmessenger AS ON UPDATE
    TO internet_instantmessenger
    DO INSTEAD
    UPDATE internet_instantmessenger_crypt SET
             "identity" = gestorpsi_encrypt(NEW."identity"),
             "network_id" = NEW."network_id",
             "content_type_id" = NEW."content_type_id",
             "object_id" = NEW."object_id"
    WHERE "id" = OLD."id";

CREATE OR REPLACE RULE rule_delete_internet_instantmessenger AS ON DELETE
   TO internet_instantmessenger
   DO INSTEAD
   DELETE FROM internet_instantmessenger_crypt WHERE "id" = OLD."id";

COMMIT;
--------------------- end crypt_script.sql ---------------------
