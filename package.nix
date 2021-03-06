{ stdenv
, python3
}:

let
  telepot = python3.pkgs.callPackage ./deps/telepot.nix { };

in python3.pkgs.buildPythonApplication rec {
  pname = "cembot";
  version = "0.1";
  format = "other";

  # Delete once (if...) we have a proper python package
  name = "${pname}-${version}";

  buildPhase = ''
    ${python3.interpreter} -O -m compileall .
  '';

  installPhase = ''
    mkdir -p "$out/share"
    cp -r commands DBManager __init__.py languages main.py utils "$out/share/"
    cp -r __pycache__ "$out/share/__pycache__"
    makeWrapper "${python3.interpreter}" "$out/bin/cem" \
          --set PYTHONPATH "$PYTHONPATH" \
          --run "cd \"$out/share\"" \
          --add-flags "$out/share/main.py"
  '';

  src = ./cembot;
  propagatedBuildInputs = [ telepot python3.pkgs.psycopg2 ];
}

