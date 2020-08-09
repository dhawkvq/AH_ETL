DROP TABLE reservation;
DROP TABLE property;
DROP TABLE account;
DROP TABLE location;

CREATE TABLE public.location (
  id serial NOT NULL,
  uuid uuid NULL DEFAULT uuid_generate_v4(),
  "timestamp" timestamp NULL DEFAULT now(),
  iso_3166_2 varchar NULL,
  postal_code varchar NULL,
  locality varchar NULL,
  street varchar NULL,
  num int4 NULL,
  line_02 varchar NULL,
  latitude float8 NULL,
  longitude float8 NULL,
  CONSTRAINT location_pkey PRIMARY KEY (id),
  CONSTRAINT location_uuid_uni UNIQUE (uuid)
);


 CREATE TABLE public.account (
  id serial NOT NULL,
  uuid uuid NULL DEFAULT uuid_generate_v4(),
  "firebase_id" VARCHAR NOT NULL,
  "timestamp" timestamp NULL DEFAULT now(),
  active bool NOT NULL DEFAULT true,
  handle varchar NULL,
  name_first varchar NULL,
  name_last varchar NULL,
  "type" varchar NULL,
  email varchar NULL,
  email_validated_timestamp timestamp NULL,
  phone int4 NULL,
  phone_validated_timestamp timestamp NULL,
  "location" int4 NULL,
  CONSTRAINT account_pkey PRIMARY KEY (id),
  CONSTRAINT account_uuid_uni UNIQUE (uuid),
  CONSTRAINT fk_account_location FOREIGN KEY (location) REFERENCES location(id)
);

CREATE TABLE public.property (
  id serial NOT NULL,
  uuid uuid NULL DEFAULT uuid_generate_v4(),
  "timestamp" timestamp NULL DEFAULT now(),
  active bool NOT NULL DEFAULT true,
  firebase_id VARCHAR NOT NULL,
  managing_account int4 NOT NULL,
  "location" int4 NOT NULL,
  rate int4 NOT NULL,
  acres numeric NOT NULL,
  max_capacity int4 NULL,
  validated_timestamp timestamp NULL,
  validated_memo text NULL,
  CONSTRAINT property_pkey PRIMARY KEY (id),
  CONSTRAINT property_uuid_uni UNIQUE (uuid),
  CONSTRAINT fk_property_location FOREIGN KEY (location) REFERENCES location(id),
  CONSTRAINT fk_property_managing_account FOREIGN KEY (managing_account) REFERENCES account(id)
);

CREATE TABLE public.reservation (
  id serial NOT NULL,
  uuid uuid NULL DEFAULT uuid_generate_v4(),
  "timestamp" timestamp NULL DEFAULT now(),
  state varchar NOT NULL,
  account int4 NOT NULL,
  property int4 NOT NULL,
  rate int4 NOT NULL,
  timestamp_start timestamp NOT NULL,
  timestamp_end timestamp NOT NULL,
  CONSTRAINT reservation_pkey PRIMARY KEY (id),
  CONSTRAINT reservation_uuid_uni UNIQUE (uuid),
  CONSTRAINT fk_reservation_account FOREIGN KEY (account) REFERENCES account(id),
  CONSTRAINT fk_reservation_property FOREIGN KEY (property) REFERENCES property(id)
);