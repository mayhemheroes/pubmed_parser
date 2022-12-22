#! /usr/bin/python3
import tempfile
from contextlib import contextmanager
import atheris
import sys
import lxml.etree
import logging
import io
import tempfile
logging.disable(logging.CRITICAL)

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.BytesIO()
    sys.stderr = io.BytesIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

with atheris.instrument_imports():
   import pubmed_parser as pp


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    # bytes_per_harness = len(data) // 2
    # xml_bytes = fdp.ConsumeBytes(bytes_per_harness)
    # ref_bytes = fdp.ConsumeBytes(bytes_per_harness)

    try:
        with nostdout(), tempfile.NamedTemporaryFile() as f:
            f.write(data)
            f.flush()
            pp.parse_pubmed_xml(f.name)
        with nostdout(), tempfile.NamedTemporaryFile() as f:
            f.write(data)
            f.flush()
            pp.parse_pubmed_references(f.name)

    except lxml.etree.XMLSyntaxError:
        pass
    except TypeError as e:
        if "bytes-like" not in str(e):
            raise

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
