--
-- PostgreSQL database dump
--

-- Dumped from database version 10.18 (Ubuntu 10.18-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.18 (Ubuntu 10.18-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: logs_user
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO logs_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: logs_user
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO logs_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: logs_user
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: logs_user
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: logs_user
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-09-26 10:48:44.567502+03
2	contenttypes	0002_remove_content_type_name	2019-09-26 10:48:44.592427+03
3	auth	0001_initial	2019-09-26 10:48:44.687117+03
4	auth	0002_alter_permission_name_max_length	2019-09-26 10:48:44.70662+03
5	auth	0003_alter_user_email_max_length	2019-09-26 10:48:44.722213+03
6	auth	0004_alter_user_username_opts	2019-09-26 10:48:44.746267+03
7	auth	0005_alter_user_last_login_null	2019-09-26 10:48:44.763924+03
8	auth	0006_require_contenttypes_0002	2019-09-26 10:48:44.76797+03
9	auth	0007_alter_validators_add_error_messages	2019-09-26 10:48:44.78293+03
10	auth	0008_alter_user_username_max_length	2019-09-26 10:48:44.815953+03
11	accounts	0001_initial	2019-09-26 10:48:44.908675+03
12	admin	0001_initial	2019-09-26 10:48:44.981859+03
13	admin	0002_logentry_remove_auto_add	2019-09-26 10:48:45.020872+03
14	custom_auth	0001_initial	2019-09-26 10:48:45.099545+03
15	property	0001_initial	2019-09-26 10:48:45.272891+03
16	property	0002__	2019-09-26 10:48:45.339157+03
17	property	0003__	2019-09-26 10:48:45.397395+03
18	logs	0001_initial	2019-09-26 10:48:45.424624+03
21	sessions	0001_initial	2019-09-26 10:48:45.511368+03
22	accounts	0002__	2019-09-26 19:42:37.994735+03
23	accounts	0003__	2019-10-02 17:32:44.563985+03
27	accounts	0004__	2021-04-30 20:29:24.258458+03
28	notifications	0001_initial	2021-04-30 20:29:24.38298+03
29	notifications	0002__	2021-04-30 20:29:24.575909+03
30	notifications	0003__	2021-04-30 20:29:24.670723+03
26	logs	0004__	2019-11-16 18:23:51.66344+02
19	logs	0002__	2019-09-26 10:48:45.45318+03
20	logs	0003__	2019-09-26 10:48:45.475876+03
25	property	0005__	2019-10-06 21:00:46.714675+03
24	property	0004__	2019-10-06 21:00:46.645952+03
31	logs	0005__	2021-10-14 18:11:36.561531+03
32	logs	0006__	2021-11-07 12:22:43.944395+02
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: logs_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 32, true);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: logs_user
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--
