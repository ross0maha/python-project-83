CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name varchar(255),
    created_at date
);


CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id bigint REFERENCES urls(id),
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at date
);
