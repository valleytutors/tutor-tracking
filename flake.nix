{
  description = "python environment for tutor-tracking code";
  inputs.mach-nix.url = "github:DavHau/mach-nix";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, mach-nix, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShell = mach-nix.lib.${system}.mkPythonShell {
        requirements = ''
          notion
          gspread
          google-auth-oauthlib
        '';
      };
    });
}
