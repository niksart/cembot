{ config, pkgs, lib, ... }:

let
  cembotPackage = pkgs.callPackage ./package.nix {};
  cfg = config.services.cembot;
  dbname = "cembot";
  user = "cembot";

in {
  options.services.cembot = {
    enable = lib.mkEnableOption (lib.mdDoc "cembot telegram bot");
    language = lib.mkOption {
      type = lib.types.enum [ "EN" "IT" ];
      default = "IT";
    };
    currency = lib.mkOption {
      type = lib.types.str;
      default = "€";
      example = "$";
      description = lib.mkDoc ''
        Currency name to use for display and parsing
      '';
    };
    telegramTokenFile = lib.mkOption {
      type = lib.types.path;
      example = "/run/credentials/cembot.service/telegram-token";
      description = lib.mkDoc ''
        Path to a file containing `CEM_TELEGRAM_TOKEN=<token>`
      '';
    };
  };
  config = lib.mkIf cfg.enable {
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
        ensureDBOwnership = true;
      }];
      initialScript = pkgs.writeText "postgres-cembot-initial-script" ''
        \connect ${dbname}
        ${builtins.readFile ./schema.sql};
      '';
    };
    systemd.services.cembot = {
      description = "cembot main service";
      path  = [ cembotPackage ];
      script =
        ''
          cem \
            ${lib.strings.escapeShellArg dbname} \
            ${lib.strings.escapeShellArg user} \
            "" \
            "" \
            ${lib.strings.escapeShellArg cfg.language} \
            ${lib.strings.escapeShellArg cfg.currency}
        '';
      serviceConfig = {
        User = user;
        EnvironmentFile = cfg.telegramTokenFile;
      };
    };
  };
}
