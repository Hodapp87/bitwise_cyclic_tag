{ pkgs ? import <nixpkgs> {} }:

let stdenv = pkgs.stdenv;
in stdenv.mkDerivation rec {
  name = "python-stuff";
  buildInputs = with pkgs; [
     (python3.withPackages (ps: [ps.numpy ps.pillow]))
  ];
}
