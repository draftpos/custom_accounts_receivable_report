frappe.query_reports["Premium Receivables Report"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            fieldname: "report_date",
            label: __("Report Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "finance_book",
            label: __("Finance Book"),
            fieldtype: "Link",
            options: "Finance Book"
        },
        {
            fieldname: "cost_center",
            label: __("Cost Center"),
            fieldtype: "Link",
            options: "Cost Center"
        },
        {
            fieldname: "party_type",
            label: __("Party Type"),
            fieldtype: "Select",
            options: "\nCustomer\nSupplier",
            default: "Customer"
        },
        {
            fieldname: "party",
            label: __("Client"),
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "party_account",
            label: __("Receivable Account"),
            fieldtype: "Link",
            options: "Account"
        },
        {
            fieldname: "ageing_based_on",
            label: __("Ageing Based On"),
            fieldtype: "Select",
            options: "Due Date\nPosting Date",
            default: "Due Date"
        },
        {
            fieldname: "range1",
            label: __("Ageing Range 1"),
            fieldtype: "Int",
            default: 30
        },
        {
            fieldname: "range2",
            label: __("Ageing Range 2"),
            fieldtype: "Int",
            default: 60
        },
        {
            fieldname: "range3",
            label: __("Ageing Range 3"),
            fieldtype: "Int",
            default: 90
        },
        {
            fieldname: "range4",
            label: __("Ageing Range 4"),
            fieldtype: "Int",
            default: 120
        },
        {
            fieldname: "customer_group",
            label: __("Client Group"),
            fieldtype: "Link",
            options: "Customer Group"
        },
        {
            fieldname: "payment_terms_template",
            label: __("Payment Terms Template"),
            fieldtype: "Link",
            options: "Payment Terms Template"
        },
        {
            fieldname: "sales_partner",
            label: __("Sales Partner"),
            fieldtype: "Link",
            options: "Sales Partner"
        },
        {
            fieldname: "sales_person",
            label: __("Sales Person"),
            fieldtype: "Link",
            options: "Sales Person"
        },
        {
            fieldname: "territory",
            label: __("Territory"),
            fieldtype: "Link",
            options: "Territory"
        },
        {
            fieldname: "currency",
            label: __("Currency"),
            fieldtype: "Link",
            options: "Currency"
        },
        {
            fieldname: "receipt_number",
            label: __("Receipt Number"),
            fieldtype: "Data"
        },
        {
            fieldname: "group_by_customer",
            label: __("Group By Customer"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "based_on_payment_terms",
            label: __("Based On Payment Terms"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "show_future_payments",
            label: __("Show Future Payments"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "show_delivery_notes",
            label: __("Show Linked Delivery Notes"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "show_sales_person",
            label: __("Show Sales Person"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "show_remarks",
            label: __("Show Remarks"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "revaluation_journals",
            label: __("Revaluation Journals"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "group_by_voucher",
            label: __("Group by Voucher"),
            fieldtype: "Check",
            default: 0
        },
        {
            fieldname: "in_party_currency",
            label: __("In Party Currency"),
            fieldtype: "Check",
            default: 0
        }
    ]
};
