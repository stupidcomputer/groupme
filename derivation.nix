{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "groupme_sync";
  version = "1.0";

  propagatedBuildInputs = [ websockets requests ];

  src = ./.;
}