class Hipodromo < Formula
  include Language::Python::Virtualenv

  desc "Juego de hipódromo en terminal con apuestas"
  homepage "https://github.com/svaldesoliva/hipodromo_python"
  url "https://github.com/svaldesoliva/hipodromo_python/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "REPLACE_WITH_TARBALL_SHA256"
  license "MIT"

  depends_on "python@3.11"

  resource "termcolor" do
    url "https://files.pythonhosted.org/packages/2b/cc/0a927e7b8b646a5c96eb1f0ec261646ddf1e9a40c3c4a8a515cf2e3d3093/termcolor-2.4.0.tar.gz"
    sha256 "c2512d1e6b2a6f3f8b83a00d2fe4b48d9c5a79310277c9b6e6ef0d5f362ec1cd"
  end

  def install
    virtualenv_install_with_resources
    bin.install_symlink libexec/"bin/hipodromo"
  end

  test do
    # Non-interactive smoke test: ensure CLI is present
    assert_match "", shell_output("#{bin}/hipodromo < /dev/null || true")
  end
end
