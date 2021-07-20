{ config, pkgs, ... }:

let
  cembotPackage = pkgs.callPackage ./package.nix {};
  language = "IT";
  dbname = "cem";
  dbuser = "cem";
  dbpassword = import ./db-password.nix;
  dbhost = "localhost";

in {
  services.postgresql = {
    enable = true;
    # Disable to migrate:
    initialScript = pkgs.writeText "postgres-initial-script" (''
      CREATE ROLE cem SUPERUSER LOGIN PASSWORD '${dbpassword}';
      CREATE DATABASE cem;
      \connect cem
    ''
    + builtins.readFile ./schema.sql);
  };
  systemd.services.cembot = {
    description = "cembot main service";
    path  = [ cembotPackage ];
    environment = {
      CEM_IT = import ./telegram-token.nix;
    };
    script =
      ''
        cem \
          ${dbname} \
          ${dbuser} \
          ${dbpassword} \
          ${dbhost} \
          ${language}
      '';
  };
}

