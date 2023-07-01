{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [ fish ] 
    ++ (with pkgs.nodePackages; [ pnpm ]); 

  shellHook = ''
  fish
  '';
}
