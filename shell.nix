{ pkgs ? import <nixpkgs> {} }:

let
  my-python-packages = ps: with ps; [
    requests
    websockets
  ];
in
  pkgs.mkShell {
    packages = [
      (pkgs.python3.withPackages my-python-packages)
    ];
  }