{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages = {
          myapp = mkPoetryApplication { projectDir = self; };
          default = self.packages.${system}.myapp;
        };

        devShells.default = pkgs.mkShell {
		  buildInputs = [
		    pkgs.gcc
			pkgs.pkg-config
			pkgs.cairo.dev
			pkgs.xorg.libxcb.dev
			pkgs.xorg.libX11.dev
			pkgs.xorg.xorgproto
			pkgs.glib.dev
			pkgs.gobject-introspection.dev
			pkgs.libffi.dev
			pkgs.cmake
			pkgs.zlib
			pkgs.libglvnd
			pkgs.libstdcxx5
			pkgs.libuuid
			pkgs.openssl
			pkgs.libffi
			pkgs.stdenv.cc.cc.lib
		  ];
          packages = [
		    poetry2nix.packages.${system}.poetry
			pkgs.libstdcxx5
			pkgs.python311Packages.google-cloud-texttospeech
			pkgs.ffmpeg
			pkgs.alsaLib
			pkgs.util-linux
			pkgs.libuuid
			pkgs.openssl
			pkgs.libffi
			pkgs.stdenv.cc.cc.lib
		  ];
		  env = {

			LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
			pkgs.libuuid
			pkgs.openssl
			pkgs.libffi
			pkgs.stdenv.cc.cc.lib
			];
			};
        };
      });
}
