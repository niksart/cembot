{ buildPythonPackage
, fetchFromGitHub
, aiohttp
, urllib3
}:

buildPythonPackage rec {
  pname = "telepot";
  version = "unstable";

  src = fetchFromGitHub {
    owner = "nickoala";
    repo = "telepot";
    rev = "4bfe4eeb5e48b40e72976ee085a1b0a941ef3cf2";
    sha256 = "sha256-YfNQskzwn6MDsaFGqaNhd9RIplQKT14s5kV7/EV8A64=";
  };

  patches = [
    ./new-api.patch
  ];

  propagatedBuildInputs = [ aiohttp urllib3 ];
}

