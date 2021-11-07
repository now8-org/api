CREATE TABLE public.stops (
    stop_id character varying(255) NOT NULL,
    stop_code character varying(50),
    stop_name character varying(255) NOT NULL,
    stop_desc character varying(255),
    stop_lat numeric(12,9) NOT NULL,
    stop_lon numeric(12,9) NOT NULL,
    zone_id character varying(50),
    stop_url character varying(255),
    location_type integer,
    parent_station character varying(255),
    stop_timezone character varying(50),
    wheelchair_boarding integer,
    platform_code character varying(50),
    direction character varying(50),
    "position" character varying(50),
);

COPY public.stops (stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station, stop_timezone, wheelchair_boarding, platform_code, direction, "position", geom) FROM stdin;
par_8_06686	06686	AV.BURGOS-C.C.SANCHINARRO	Avda de Burgos 133	40.498046875	-3.662995577	A	http://www.crtm.es	0	\N	Europe/Madrid	2	\N	\N	\N
par_8_06687	06687	AV.BURGOS-DOMINICOS	Avda de Burgos 11300	40.501441956	-3.659948826	A	http://www.crtm.es	0	\N	Europe/Madrid	2	\N	\N	\N
par_8_06689	06689	CTRA.A1-CUESTA BLANCA	Ctra de Irún 13700	40.521770477	-3.651010752	B1	http://www.crtm.es	0	\N	Europe/Madrid	2	\N	\N	\N
\.
