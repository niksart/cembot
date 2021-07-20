CREATE TABLE transactions (
    id            bigserial,
    payer         bigint,
    amount        bigint,
    time          bigint,
    description   text,
    group_id      bigint,
    PRIMARY KEY (id)
);

--beneficiari
CREATE TABLE payees (
    id               bigserial,
    transaction_id   bigint references transactions(id), -- FK Transactions.Id
    payee            bigint,--# User Id
    PRIMARY KEY (id)
);

CREATE TABLE authorizations (
    id               bigserial,
    authorizer       bigint, --User Id
    authorized       bigint,  --User Id
    PRIMARY KEY (id)
);

CREATE TABLE idmappings (
    username         varchar(20),
    id               bigint,
    PRIMARY KEY (id)
);

CREATE TABLE groupmappings (
    name             text,
    id               bigint,
    PRIMARY KEY (id)
);

CREATE TABLE belongings (
    group_id         bigint,
    user_id          bigint,
    PRIMARY KEY (group_id, user_id)
);

CREATE INDEX map_username ON idmappings (username);

CREATE INDEX check_group ON belongings (group_id, user_id);
