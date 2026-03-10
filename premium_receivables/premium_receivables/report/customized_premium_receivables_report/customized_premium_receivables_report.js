frappe.query_reports["Customized Premium Receivables Report"] = {
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
            fieldname: "territory",
            label: __("Territory"),
            fieldtype: "Link",
            options: "Territory"
        },
        {
            fieldname: "sales_person",
            label: __("Sales Person"),
            fieldtype: "Link",
            options: "Sales Person"
        },
        {
            fieldname: "cost_center",
            label: __("Cost Center"),
            fieldtype: "Link",
            options: "Cost Center"
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
        }
    ]
};
