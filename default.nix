{ pkgs ? import <nixpkgs> {} }:
let
#  python = import ./requirements.nix { inherit pkgs; };
  gspread_fixed = pkgs.python38Packages.gspread.overrideAttrs (old: {
    buildInputs = [ pkgs.python38Packages.google-auth-oauthlib ];
  });
in 
pkgs.mkShell {
  buildInputs = with pkgs.python38Packages; [ 
    google-auth-oauthlib
    oauth2client
    gspread_fixed
  ];
}

