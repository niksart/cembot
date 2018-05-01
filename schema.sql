CREATE TABLE transactions (
    id            bigserial,
    payer         integer,
    amount        integer,
    time          integer,
    description   text,
    group_id      bigint,
    PRIMARY KEY (id)
);

--beneficiari
CREATE TABLE payees (
    id               bigserial,
    transaction_id   bigint references transactions(id), -- FK Transactions.Id
    payee            integer,--# User Id
    PRIMARY KEY (id)
);

CREATE TABLE authorizations (
    id               bigserial,
    authorizer       integer, --User Id
    authorized       integer,  --User Id
    PRIMARY KEY (id)
);

CREATE TABLE idmappings (
    username         varchar(20),
    id               integer,
    PRIMARY KEY (username, id)
)

CREATE TABLE belongings (
    group_id         integer,
    user_id          integer,
    PRIMARY KEY (group_id, user_id)
)

CREATE INDEX map_username ON idmappings USING HASH (username);

CREATE INDEX check_group ON belongings USING HASH (group_id, user_id);