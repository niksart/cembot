CREATE TABLE transactions (
    id            bigserial,
    payer         integer,
    amount        integer,
    time          integer,
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