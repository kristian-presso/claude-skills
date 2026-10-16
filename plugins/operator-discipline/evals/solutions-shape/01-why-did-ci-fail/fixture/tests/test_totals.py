from invoicer.totals import gross_total


def test_gross_total_adds_vat():
    assert gross_total(1000) == 1200
