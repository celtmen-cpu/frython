# Documentation for alize, a French version of Python.
#
# To publish a release and fill the placeholders below:
#   1. Push the project to https://github.com/celtmen-cpu/alize
#   2. Tag the release: git tag v5.0.0 && git push origin v5.0.0
#   3. Create the GitHub release (archive auto-generated)
#   4. Download it and run: shasum -a 256 v5.0.0.tar.gz
#   5. Replace URL_PLACEHOLDER and SHA256_PLACEHOLDER below
class Alize < Formula
  include Language::Python::Virtualenv

  desc "French version of Python (French keywords and built-ins)"
  homepage "https://github.com/celtmen-cpu/alize"
  # TODO(release): replace with the real stable archive once published, e.g.:
  #   https://github.com/celtmen-cpu/alize/archive/refs/tags/v5.0.0.tar.gz
  url "URL_PLACEHOLDER"
  sha256 "SHA256_PLACEHOLDER"
  version "5.0.0"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    (testpath / "bonjour.az").write <<~EOS
      afficher("bonjour")
    EOS
    assert_equal "bonjour", shell_output("#{bin}/alize bonjour.az").strip
  end
end
