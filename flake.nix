{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }@inputs: {
    devShell."x86_64-linux" = import ./shell.nix { pkgs = nixpkgs.legacyPackages."x86_64-linux"; };
  };
}
