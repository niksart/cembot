{ config, pkgs, ... }:

let
  cembotPackage = pkgs.callPackage ./package.nix {};
  language = "IT";
  currency = "€";
  dbname = "cembot";
  user = "cembot";

in {
  users.users."${user}" = {
    description = "cembot service user";
    isSystemUser = true;
    group = user;
  };
  users.groups."${user}" = {};
  services.postgresql = {
    enable = true;
    ensureDatabases = [ dbname ];
    ensureUsers = [{
      name = user;
      ensurePermissions = {
        "DATABASE \"${dbname}\"" = "ALL PRIVILEGES";
        "ALL TABLES IN SCHEMA public" = "ALL PRIVILEGES";
      };
    }];
    initialScript = pkgs.writeText "postgres-cembot-initial-script" ''
      \connect ${dbname}
      ${builtins.readFile ./schema.sql};
    '';
  };
  systemd.services.cembot = {
    description = "cembot main service";
    path  = [ cembotPackage ];
    environment = {
      CEM_TELEGRAM_TOKEN = import ./telegram-token.nix;
    };
    script =
      ''
        cem \
          ${dbname} \
          ${user} \
          "" \
          "" \
          ${language} \
          ${currency}
      '';
    serviceConfig = {
      User = user;
    };
  };
}
