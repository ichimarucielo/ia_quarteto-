import unittest

import pandas as pd

from src.check import build_check
from src.normalization import normalize_fs10n, normalize_prefeitura
from src.reconciliation import find_unmatched
from src.report import BILLING_COLUMNS, build_report


def prefeitura(rows):
    return pd.DataFrame(rows, columns=["Numero NF", "Tomador", "Valor Serviço", "Nf Ativa"])


def billing(rows):
    dataframe = pd.DataFrame(rows, columns=["Nº Nota Fiscal", "Razão Social", "Valor Bruto"])
    for column in BILLING_COLUMNS:
        if column not in dataframe:
            dataframe[column] = ""
    return dataframe[BILLING_COLUMNS]


class ReconciliationTests(unittest.TestCase):
    def test_groups_each_source_before_comparison(self):
        left = prefeitura([
            ["10", "A", 30, "SIM"], ["10", "A", 20, "SIM"],
            ["20", "B", 7, "SIM"], ["20", "B", 8, "SIM"],
        ])
        right = billing([
            ["10.0", "A", 15], ["10.0", "A", 35],
            ["30", "C", 4], ["30", "C", 6],
        ])
        actual = find_unmatched(left, right)
        self.assertEqual(actual["Tipo Exceção"].tolist(), [
            "PREFEITURA_SEM_BILLING", "BILLING_SEM_PREFEITURA",
        ])
        self.assertEqual(actual["Diferença"].tolist(), [15, -10])
        self.assertEqual(actual["Diferença"].sum(), 5)
        self.assertNotIn("_nf", left.columns)
        self.assertNotIn("_nf", right.columns)

    def test_common_nf_with_different_value_or_cancelled_status_is_not_unmatched(self):
        left = prefeitura([["001", "A", 100, "CANCELADA"]])
        right = billing([["001.0", "A", 90]])
        report = build_report(left, right)
        self.assertTrue(report["Nao_Conciliadas"].empty)
        self.assertEqual(report["SAP x Prefeitura"].iloc[2]["Valor"], 10)
        self.assertEqual(len(report["Notas Emitidas"]), 1)

    def test_invalid_keys_do_not_become_exceptions(self):
        left = prefeitura([[key, "A", 10, "SIM"] for key in (None, "", "nan", "none", "0")])
        right = billing([[key, "B", 20] for key in (None, "", "nan", "none", "0")])
        self.assertTrue(find_unmatched(left, right).empty)

    def test_one_sided_and_empty_sources_have_stable_columns(self):
        empty_left, empty_right = prefeitura([]), billing([])
        self.assertEqual(len(find_unmatched(empty_left, empty_right).columns), 11)
        actual = find_unmatched(empty_left, billing([["9", "A", 20]]))
        self.assertEqual(actual["Diferença"].tolist(), [-20])


class CheckTests(unittest.TestCase):
    def test_rv_exact_match_active_only_and_no_deduplication(self):
        left = prefeitura([["10", "A", 20, "SIM"], ["20", "B", 10, "CANCELADA"]])
        right = pd.DataFrame([
            ["10", "RV", -10], ["10", "RV", -10],
            ["20", "RV", -10], ["RPS / 10", "RV", -99],
            ["10", "EF", 20], ["10", "DG", 5],
        ], columns=["Referência", "Tipo de documento", "Montante em moeda interna"])
        actual = build_check(left, right)
        self.assertEqual(len(actual["Notas Emitidas Razao"]), 2)
        self.assertEqual(len(actual["Prefeitura Canceladas"]), 1)
        self.assertEqual(len(actual["Cancelamentos"]), 2)
        self.assertTrue(actual["Excecoes"].empty)
        self.assertEqual(actual["SAP x Prefeitura"].iloc[1]["Valor"], 20)

    def test_sap_balance_is_absolute_of_sum(self):
        left = prefeitura([["10", "A", 8, "SIM"]])
        right = pd.DataFrame([
            ["10", "RV", -10], ["10", "RV", 2],
        ], columns=["Referência", "Tipo de documento", "Montante em moeda interna"])
        actual = build_check(left, right)
        self.assertEqual(actual["SAP x Prefeitura"].iloc[1]["Valor"], 8)


class NormalizationTests(unittest.TestCase):
    def test_money_identifiers_and_original_data_are_preserved(self):
        original = pd.DataFrame({
            " Numero NF ": ["00123.0"], "Numerp RPS": ["0000236763"],
            "CNPJ": ["123"], "Valor Serviço": ["1.234,56"],
            "Total NF": ["1.234,56"], "Valor Fatura": ["invalido"],
        })
        actual = normalize_prefeitura(original)
        self.assertEqual(actual.iloc[0]["Numero NF"], "00123")
        self.assertEqual(actual.iloc[0]["Numerp RPS"], "0000236763")
        self.assertEqual(actual.iloc[0]["CNPJ"], "00000000000123")
        self.assertEqual(actual.iloc[0]["Valor Serviço"], 1234.56)
        self.assertEqual(actual.iloc[0]["Valor Fatura"], 0)
        self.assertIn(" Numero NF ", original.columns)

    def test_fs10n_retains_rows_and_drops_empty_header(self):
        original = pd.DataFrame({" Montante em moeda interna ": ["10", "invalido"], float("nan"): [1, 2]})
        actual = normalize_fs10n(original)
        self.assertEqual(actual.columns.tolist(), ["Montante em moeda interna"])
        self.assertEqual(actual["Montante em moeda interna"].tolist(), [10, 0])


if __name__ == "__main__":
    unittest.main()
