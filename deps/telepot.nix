{ buildPythonPackage
, fetchPypi
, aiohttp
, urllib3
}:

buildPythonPackage rec {
  pname = "telepot";
  version = "12.7";

  src = fetchPypi {
    inherit pname version;
    sha256 = "1c587dmr71ppray0lzxgib1plnndmaiwal1kaiqx82rdwx4kw4ms";
  };

  propagatedBuildInputs = [ aiohttp urllib3 ];
}

