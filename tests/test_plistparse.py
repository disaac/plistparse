import pytest
from click.testing import CliRunner
from pytest import tmp

from plistparse.plistparse import run

__author__ = "Daniel"
__copyright__ = "Daniel"
__license__ = "MIT"


def test_run_globals():

    tmp.mod.plistXML = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.test.gupdatedb</string>
    <key>LowPriorityIO</key>
    <true/>
    <key>Nice</key>
    <integer>13</integer>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/gupdatedb</string>
        <string>--localpaths=/Users /var/tmp /opt</string>
        <string>--prunepaths=/Users/user/Library/CloudStorage</string>
        <string>--output=/Users/user/findutils-conf/locatedb</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/var/tmp/logs/gupdatedb.log</string>
    <key>StandardOutPath</key>
    <string>/var/tmp/logs/gupdatedb.log</string>
    <key>StartInterval</key>
    <integer>86400</integer>
</dict>
</plist>
    """  # noqa
    tmp.mod.plistJSON = """\
{
    "Label": "com.test.gupdatedb",
    "LowPriorityIO": true,
    "Nice": 13,
    "ProgramArguments": [
        "/opt/homebrew/bin/gupdatedb",
        "--localpaths=/Users /var/tmp /opt",
        "--prunepaths=/Users/user/Library/CloudStorage",
        "--output=/Users/user/findutils-conf/locatedb"
    ],
    "RunAtLoad": true,
    "StandardErrorPath": "/var/tmp/logs/gupdatedb.log",
    "StandardOutPath": "/var/tmp/logs/gupdatedb.log",
    "StartInterval": 86400
}
    """


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_run(tmp_path):
    runner = CliRunner()
    fname = "test.plist"
    with runner.isolated_filesystem(tmp_path):
        with open(fname, "w") as f:
            f.write(tmp.mod.plistXML)
        result = runner.invoke(run, args=["-f", fname], catch_exceptions=False)
    assert result.exit_code == 0
    # assert result.output == tmp.mod.plistJSON
