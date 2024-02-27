
frappe.listview_settings["Translate Message"] = {
    hide_name_column: true, // hide the last column which shows the `name`
    hide_name_filter: true, // hide the default filter field for the name column
    add_fields: ["title", "context"],
    onload(listview) {
        // triggers once before the list is loaded

    },
}