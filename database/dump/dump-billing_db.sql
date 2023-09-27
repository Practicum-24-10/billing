--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-1.pgdg110+1)
-- Dumped by pg_dump version 14.7 (Homebrew)

-- Started on 2023-09-27 21:34:42 MSK

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

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: app
--

CREATE SCHEMA IF NOT EXISTS public;


ALTER SCHEMA public OWNER TO app;

--
-- TOC entry 3040 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: app
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16385)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO app;

--
-- TOC entry 206 (class 1259 OID 16446)
-- Name: payment; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.payment (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    kassa_payment_id character varying NOT NULL,
    payment_status character varying NOT NULL,
    users_subscriptions_id uuid NOT NULL
);


ALTER TABLE public.payment OWNER TO app;

--
-- TOC entry 201 (class 1259 OID 16390)
-- Name: payment_method; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.payment_method (
    id uuid NOT NULL,
    kassa_payment_method_id character varying NOT NULL
);


ALTER TABLE public.payment_method OWNER TO app;

--
-- TOC entry 202 (class 1259 OID 16398)
-- Name: subscription; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.subscription (
    id uuid NOT NULL,
    duration integer NOT NULL,
    amount double precision NOT NULL,
    title character varying NOT NULL,
    active boolean NOT NULL,
    permission character varying NOT NULL,
    currency character varying NOT NULL
);


ALTER TABLE public.subscription OWNER TO app;

--
-- TOC entry 203 (class 1259 OID 16406)
-- Name: user; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public."user" (
    id uuid NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public."user" OWNER TO app;

--
-- TOC entry 204 (class 1259 OID 16411)
-- Name: users_payment_method; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.users_payment_method (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    payment_method_id uuid NOT NULL,
    "order" integer NOT NULL
);


ALTER TABLE public.users_payment_method OWNER TO app;

--
-- TOC entry 205 (class 1259 OID 16426)
-- Name: users_subscriptions; Type: TABLE; Schema: public; Owner: app
--

CREATE TABLE public.users_subscriptions (
    id uuid NOT NULL,
    "User" uuid NOT NULL,
    subscription_id uuid NOT NULL,
    next_subscription_id uuid NOT NULL,
    start_at timestamp without time zone NOT NULL,
    expires_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users_subscriptions OWNER TO app;

--
-- TOC entry 3028 (class 0 OID 16385)
-- Dependencies: 200
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.alembic_version (version_num) FROM stdin;
ae3e3c32bcaf
\.


--
-- TOC entry 3034 (class 0 OID 16446)
-- Dependencies: 206
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.payment (id, created_at, kassa_payment_id, payment_status, users_subscriptions_id) FROM stdin;
\.


--
-- TOC entry 3029 (class 0 OID 16390)
-- Dependencies: 201
-- Data for Name: payment_method; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.payment_method (id, kassa_payment_method_id) FROM stdin;
\.


--
-- TOC entry 3030 (class 0 OID 16398)
-- Dependencies: 202
-- Data for Name: subscription; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.subscription (id, duration, amount, title, active, permission, currency) FROM stdin;
94791a79-42a0-46cc-b231-9d8f61569b47	30	300	HD	t	hd	RUB
b0ec64e6-3c55-4f1f-8d1b-3c9048e53a0b	30	500	FullHD	t	fullhd	RUB
c4326b05-0e88-4c2a-a053-e8f1dd190b38	30	1000	4K	t	4k	RUB
\.


--
-- TOC entry 3031 (class 0 OID 16406)
-- Dependencies: 203
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public."user" (id, active) FROM stdin;
\.


--
-- TOC entry 3032 (class 0 OID 16411)
-- Dependencies: 204
-- Data for Name: users_payment_method; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.users_payment_method (id, user_id, payment_method_id, "order") FROM stdin;
\.


--
-- TOC entry 3033 (class 0 OID 16426)
-- Dependencies: 205
-- Data for Name: users_subscriptions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.users_subscriptions (id, "User", subscription_id, next_subscription_id, start_at, expires_at) FROM stdin;
\.


--
-- TOC entry 2879 (class 2606 OID 16389)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 2881 (class 2606 OID 16397)
-- Name: payment_method payment_method_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.payment_method
    ADD CONSTRAINT payment_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 16453)
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (id);


--
-- TOC entry 2883 (class 2606 OID 16405)
-- Name: subscription subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- TOC entry 2885 (class 2606 OID 16410)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2887 (class 2606 OID 16415)
-- Name: users_payment_method users_payment_method_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_payment_method
    ADD CONSTRAINT users_payment_method_pkey PRIMARY KEY (id);


--
-- TOC entry 2889 (class 2606 OID 16430)
-- Name: users_subscriptions users_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_subscriptions
    ADD CONSTRAINT users_subscriptions_pkey PRIMARY KEY (id);


--
-- TOC entry 2897 (class 2606 OID 16454)
-- Name: payment payment_users_subscriptions_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_users_subscriptions_id_fkey FOREIGN KEY (users_subscriptions_id) REFERENCES public.users_subscriptions(id);


--
-- TOC entry 2892 (class 2606 OID 16416)
-- Name: users_payment_method users_payment_method_payment_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_payment_method
    ADD CONSTRAINT users_payment_method_payment_method_id_fkey FOREIGN KEY (payment_method_id) REFERENCES public.payment_method(id);


--
-- TOC entry 2893 (class 2606 OID 16421)
-- Name: users_payment_method users_payment_method_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_payment_method
    ADD CONSTRAINT users_payment_method_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 2894 (class 2606 OID 16431)
-- Name: users_subscriptions users_subscriptions_User_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_subscriptions
    ADD CONSTRAINT "users_subscriptions_User_fkey" FOREIGN KEY ("User") REFERENCES public."user"(id);


--
-- TOC entry 2895 (class 2606 OID 16436)
-- Name: users_subscriptions users_subscriptions_next_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_subscriptions
    ADD CONSTRAINT users_subscriptions_next_subscription_id_fkey FOREIGN KEY (next_subscription_id) REFERENCES public.subscription(id);


--
-- TOC entry 2896 (class 2606 OID 16441)
-- Name: users_subscriptions users_subscriptions_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY public.users_subscriptions
    ADD CONSTRAINT users_subscriptions_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscription(id);


-- Completed on 2023-09-27 21:34:43 MSK

--
-- PostgreSQL database dump complete
--

