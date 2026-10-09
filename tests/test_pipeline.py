"""Regressão das entradas reais contra a referência anterior à reorganização."""

import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pandas as pd

import main
from src.ingestion import read_prefeitura

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(frame):
    values = frame.to_json(orient="split", date_format="iso", double_precision=15,
                           force_ascii=False)
    return {
        "rows": len(frame), "columns": list(frame.columns),
        "dtypes": [str(dtype) for dtype in frame.dtypes],
        "sha256": hashlib.sha256(values.encode("utf-8")).hexdigest(),
    }


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = json.loads((ROOT / "tests/fixtures/baseline.json").read_text(encoding="utf-8"))
        cls.inputs = [ROOT / path for path in cls.reference["inputs"]]
        for relative, expected in cls.reference["inputs"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            if actual != expected:
                raise AssertionError(f"Entrada alterada: {relative}. A referência exige as entradas originais.")
        with patch("main.read_prefeitura", wraps=read_prefeitura) as reader:
            cls.workbooks = main.build_workbooks(*cls.inputs)
            cls.read_count = reader.call_count

    def arguments(self, *extra):
        return [item for name, path in zip(("prefeitura", "fs10n", "zsd008"), self.inputs)
                for item in (f"--{name}", str(path))] + list(extra)

    def test_prefeitura_is_read_once(self):
        self.assertEqual(self.read_count, 1)

    def test_all_twelve_sheets_match_reference(self):
        self.assertEqual(list(self.workbooks), list(self.reference["workbooks"]))
        for filename, sheets in self.workbooks.items():
            expected = self.reference["workbooks"][filename]
            self.assertEqual(list(sheets), list(expected))
            for name, frame in sheets.items():
                with self.subTest(file=filename, sheet=name):
                    self.assertEqual(fingerprint(frame), expected[name]["dataframe"])

    def test_cli_exports_all_sheets_with_identical_cell_values(self):
        # Diretório exclusivo dentro do workspace; históricos nunca são sobrescritos.
        with tempfile.TemporaryDirectory(prefix="test-quarteto-", dir=ROOT) as directory:
            with patch("main.configure_logging"), patch("main.build_workbooks", return_value=self.workbooks):
                outputs = main.main(self.arguments("--output-dir", directory))
            self.assertEqual(len(outputs), 2)
            for output in outputs:
                actual = pd.read_excel(output, sheet_name=None)
                expected = self.reference["workbooks"][output.name]
                self.assertEqual(list(actual), list(expected))
                for name, frame in actual.items():
                    with self.subTest(file=output.name, sheet=name):
                        self.assertEqual(fingerprint(frame), expected[name]["exported"])

    def test_analysis_does_not_export_or_create_output_directory(self):
        with tempfile.TemporaryDirectory(prefix="test-quarteto-", dir=ROOT) as directory:
            destination = Path(directory) / "nao-criar"
            with patch("main.configure_logging"), patch("main.build_workbooks", return_value=self.workbooks), patch("main.export_workbook") as export, redirect_stdout(io.StringIO()) as output:
                result = main.main(self.arguments("--analisar", "--output-dir", str(destination)))
            self.assertEqual(result, [])
            export.assert_not_called()
            self.assertFalse(destination.exists())
            self.assertIn("PREFEITURA_SEM_BILLING", output.getvalue())

    def test_missing_input_is_rejected_before_processing(self):
        arguments = self.arguments()
        arguments[1] = str(ROOT / "arquivo-inexistente.csv")
        with patch("main.build_workbooks") as build, redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main.main(arguments)
        self.assertEqual(error.exception.code, 2)
        build.assert_not_called()

    def test_reader_preserves_identifier_zeroes(self):
        with tempfile.TemporaryDirectory(prefix="test-quarteto-", dir=ROOT) as directory:
            path = Path(directory) / "prefeitura.csv"
            path.write_text("Numero NF;Numerp RPS;Tomador\n00123;0000236763;João\n", encoding="latin1")
            actual = read_prefeitura(path)
        self.assertEqual(actual.iloc[0]["Numero NF"], "00123")
        self.assertEqual(actual.iloc[0]["Numerp RPS"], "0000236763")
        self.assertEqual(actual.iloc[0]["Tomador"], "João")


if __name__ == "__main__":
    unittest.main()
