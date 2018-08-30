with import <nixpkgs> {};

let
telepot = pythonPackages.buildPythonPackage rec {
  pname = "telepot";
  version = "12.7";

  src = pythonPackages.fetchPypi {
    inherit pname version;
    sha256 = "1c587dmr71ppray0lzxgib1plnndmaiwal1kaiqx82rdwx4kw4ms";
  };

  propagatedBuildInputs = with pythonPackages; [ urllib3 ];
};
   # once we have a proper python package replace this with: pythonPackages.buildPythonApplication {
in stdenv.mkDerivation rec {
  pname = "cembot";
  version = "0.1";

  # Delete once we have a proper python package
  name = "${pname}-${version}";
  installPhase = ''
    install -Dm755 cem.py $out/share/cem.py
    install -Dm755 DBManager.py $out/share/DBManager.py
    echo "cd $out/share; ${python.withPackages (ps: [ telepot ps.psycopg2 ])}/bin/python $out/share/cem.py '$@'" > cem-wrapper
    install -Dm755 cem-wrapper $out/bin/cem
  '';

  src = ./.;
  propagatedBuildInputs = [ telepot pythonPackages.psycopg2 ];
}
