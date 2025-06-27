{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.ffmpeg
    pkgs.pnpm
    pkgs.python312Full
    pkgs.python312Packages.pip
    pkgs.uv
  ];
}
