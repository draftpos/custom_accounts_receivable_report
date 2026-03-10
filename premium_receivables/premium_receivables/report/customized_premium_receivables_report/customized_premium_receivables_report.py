import frappe
import math
from frappe import _
from frappe.utils import nowdate, getdate, date_diff, flt, cint

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns(filters)
    data = get_data(filters)
    chart = get_chart_data(data, filters)
    report_summary = get_report_summary(data)
    return columns, data, None, chart, report_summary

def get_columns(filters):
    r1 = cint(filters.get("range1") or 30)
    r2 = cint(filters.get("range2") or 60)
    r3 = cint(filters.get("range3") or 90)
    r4 = cint(filters.get("range4") or 120)
    return [
        {"label": _("Date of Payment Entry"), "fieldname": "posting_date", "fieldtype": "Date", "width": 140},
        {"label": _("Receipt Number"), "fieldname": "receipt_number", "fieldtype": "Data", "width": 140},
        {"label": _("Client Name"), "fieldname": "party", "fieldtype": "Data", "width": 200},
        {"label": _("Premium Due"), "fieldname": "invoiced", "fieldtype": "Currency", "options": "currency", "width": 140},
        {"label": _("Premium Paid"), "fieldname": "paid", "fieldtype": "Currency", "options": "currency", "width": 140},
        {"label": _("Arrears in Months"), "fieldname": "arrears_in_months", "fieldtype": "Int", "width": 140},
        {"label": _("Outstanding Premium"), "fieldname": "outstanding", "fieldtype": "Currency", "options": "currency", "width": 150},
        {"label": _("Age Analysis (Days)"), "fieldname": "age", "fieldtype": "Int", "width": 140},
        {"label": _("0-{0}").format(r1), "fieldname": "range1", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": _("{0}-{1}").format(r1+1, r2), "fieldname": "range2", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": _("{0}-{1}").format(r2+1, r3), "fieldname": "range3", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": _("{0}-{1}").format(r3+1, r4), "fieldname": "range4", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": _("Above {0}").format(r4), "fieldname": "range5", "fieldtype": "Currency", "options": "currency", "width": 120},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    today = getdate(filters.get("report_date") or nowdate())
    r1 = cint(filters.get("range1") or 30)
    r2 = cint(filters.get("range2") or 60)
    r3 = cint(filters.get("range3") or 90)
    r4 = cint(filters.get("range4") or 120)
    ageing_based_on = filters.get("ageing_based_on") or "Due Date"

    ple_entries = frappe.db.sql("""
        SELECT
            ple.posting_date,
            ple.party_type,
            ple.party,
            ple.account as party_account,
            ple.voucher_type,
            ple.voucher_no,
            ple.against_voucher_type,
            ple.against_voucher_no,
            ple.amount,
            ple.cost_center,
            ple.due_date,
            ple.account_currency as currency
        FROM `tabPayment Ledger Entry` ple
        WHERE ple.docstatus = 1
        AND ple.party_type = "Customer"
        {conditions}
        ORDER BY ple.posting_date DESC
    """.format(conditions=conditions), filters, as_dict=True)

    voucher_balance = {}
    for ple in ple_entries:
        key = (ple.against_voucher_type, ple.against_voucher_no, ple.party, ple.party_account)
        if key not in voucher_balance:
            voucher_balance[key] = frappe._dict({
                "posting_date": ple.posting_date,
                "party_type": ple.party_type,
                "party": ple.party,
                "party_account": ple.party_account,
                "against_voucher_type": ple.against_voucher_type,
                "against_voucher_no": ple.against_voucher_no,
                "cost_center": ple.cost_center,
                "due_date": ple.due_date,
                "currency": ple.currency,
                "invoiced": 0.0,
                "paid": 0.0,
                "credit_note": 0.0,
                "outstanding": 0.0,
            })

        row = voucher_balance[key]
        amount = flt(ple.amount)
        if amount > 0:
            if ple.voucher_type in ("Journal Entry", "Payment Entry") and ple.voucher_no != ple.against_voucher_no:
                row.paid += abs(amount)
            else:
                row.invoiced += amount
        else:
            row.paid += abs(amount)
        row.outstanding = row.invoiced - row.paid - row.credit_note

    data = []
    for key, row in voucher_balance.items():
        against_type = row.against_voucher_type
        against_no = row.against_voucher_no

        receipt_number = ""
        if against_type == "Sales Invoice":
            payment = frappe.db.sql("""
                SELECT pe.name as receipt_number, pe.posting_date as payment_date
                FROM `tabPayment Entry` pe
                INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
                WHERE pe.docstatus = 1
                AND per.reference_name = %(voucher_no)s
                ORDER BY pe.posting_date DESC LIMIT 1
            """, {"voucher_no": against_no}, as_dict=True)
            if payment:
                receipt_number = payment[0].receipt_number or ""
                row.posting_date = payment[0].payment_date or row.posting_date
        else:
            pe = frappe.db.get_value("Payment Entry", against_no,
                ["name", "posting_date"], as_dict=True)
            if pe:
                receipt_number = pe.name or ""
                row.posting_date = pe.posting_date or row.posting_date

        customer_name = frappe.db.get_value("Customer", row.party, "customer_name") or row.party

        if ageing_based_on == "Due Date":
            base_date = getdate(row.due_date) if row.due_date else getdate(row.posting_date)
        else:
            base_date = getdate(row.posting_date)

        age = date_diff(today, base_date)
        arrears_in_months = math.ceil(age / 30.0) if age > 0 else 0

        outstanding = flt(row.outstanding)
        range1_val, range2_val, range3_val, range4_val, range5_val = 0, 0, 0, 0, 0
        if age <= r1:
            range1_val = outstanding
        elif age <= r2:
            range2_val = outstanding
        elif age <= r3:
            range3_val = outstanding
        elif age <= r4:
            range4_val = outstanding
        else:
            range5_val = outstanding

        data.append({
            "posting_date": row.posting_date,
            "receipt_number": receipt_number,
            "party": customer_name,
            "invoiced": row.invoiced,
            "paid": row.paid,
            "arrears_in_months": arrears_in_months,
            "outstanding": row.outstanding,
            "age": age,
            "range1": range1_val,
            "range2": range2_val,
            "range3": range3_val,
            "range4": range4_val,
            "range5": range5_val,
            "currency": row.currency,
        })

    return data

def get_chart_data(data, filters):
    r1 = cint(filters.get("range1") or 30)
    r2 = cint(filters.get("range2") or 60)
    r3 = cint(filters.get("range3") or 90)
    r4 = cint(filters.get("range4") or 120)

    labels = [
        "0-{0}".format(r1),
        "{0}-{1}".format(r1+1, r2),
        "{0}-{1}".format(r2+1, r3),
        "{0}-{1}".format(r3+1, r4),
        "Above {0}".format(r4)
    ]

    rows = []
    for row in data:
        if flt(row.get("outstanding")) > 0:
            rows.append({
                "values": [
                    flt(row.get("range1")),
                    flt(row.get("range2")),
                    flt(row.get("range3")),
                    flt(row.get("range4")),
                    flt(row.get("range5")),
                ]
            })

    return {
        "data": {"labels": labels, "datasets": rows},
        "type": "percentage"
    }

def get_report_summary(data):
    total_invoiced = sum(flt(r.get("invoiced")) for r in data)
    total_paid = sum(flt(r.get("paid")) for r in data)
    total_outstanding = sum(flt(r.get("outstanding")) for r in data)
    currency = data[0].get("currency") if data else "ZWL"
    return [
        {"value": total_invoiced, "label": _("Total Premium Due"), "datatype": "Currency", "currency": currency},
        {"value": total_paid, "label": _("Total Premium Paid"), "datatype": "Currency", "currency": currency},
        {"value": total_outstanding, "label": _("Total Outstanding Premium"), "datatype": "Currency", "currency": currency},
    ]

def get_conditions(filters):
    conditions = ""
    if filters.get("company"):
        conditions += " AND ple.company = %(company)s"
    if filters.get("party"):
        conditions += " AND ple.party = %(party)s"
    if filters.get("from_date"):
        conditions += " AND ple.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND ple.posting_date <= %(to_date)s"
    if filters.get("cost_center"):
        conditions += " AND ple.cost_center = %(cost_center)s"
    if filters.get("currency"):
        conditions += " AND ple.account_currency = %(currency)s"
    if filters.get("party_account"):
        conditions += " AND ple.account = %(party_account)s"
    if filters.get("receipt_number"):
        conditions += """ AND ple.party IN (
            SELECT pe.party FROM `tabPayment Entry` pe
            WHERE pe.custom_receipt_number = %(receipt_number)s
            AND pe.docstatus = 1
        )"""
    return conditions
