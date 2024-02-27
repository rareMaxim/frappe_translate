// Copyright (c) 2024, Maxim S and contributors
// For license information, please see license.txt

function fill_installed_app(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_installed_app",
        callback: (r) => {
            console.log(r);
            if (r.message) {
                frm.set_df_property("target_app", "options", [""].concat(r.message));
            }
        }
    });
}

function fill_po_locales(frm) {
    if (!frm.doc.target_app) return;
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_locales",
        args: {
            "app": frm.doc.target_app,
        },
        callback: (r) => {
            console.log(r);
            if (r.message) {
                frm.set_df_property("select_show_po_locales", "options", [""].concat(r.message));
            }
        }
    });
}

function test_catalog(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_translate_catalog",
        args: {
            "app": frm.doc.target_app,
        },
        callback: (r) => {
            console.log(r);
            // if (r.message) {
            //     frm.set_df_property("app_translate", "options", [""].concat(r.message));
            // }
        }
    });
}

function generate_pot(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.generate_pot",
        args: {
            "target_app": frm.doc.target_app,
        },
        callback: (r) => {
            console.log(r);
            frappe.show_alert({
                message: __('Generate main.pot file: done'),
                indicator: 'green'
            }, 5);
            get_pot_path(frm);
        }
    });
}
function get_pot_path(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_pot_path",
        args: {
            "app": frm.doc.target_app,
        },
        callback: (r) => {
            console.log(r.message);
            var indicator = (r.message.exists) ? ' 🟢' : ' 🔴';
            frm.set_df_property("btn_generate_pot", "description", r.message.path.concat(indicator));

        }
    });
}
function get_po_path(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_po_path",
        args: {
            "app": frm.doc.target_app,
            "locale": frm.doc.language,
        },
        callback: (r) => {
            console.log(r.message);
            var indicator = (r.message.exists) ? ' 🟢' : ' 🔴';
            frm.set_df_property("btn_new_po", "description", r.message.path.concat(indicator));

        }
    });
}
function get_csv_path(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.get_csv_path",
        args: {
            "app": frm.doc.target_app,
            "locale": frm.doc.language,
        },
        callback: (r) => {
            console.log(r.message);
            var indicator = (r.message.exists) ? ' 🟢' : ' 🔴';
            frm.set_df_property("btn_csv_to_po", "description", r.message.path.concat(indicator));

        }
    });
}
function new_po(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.new_po",
        args: {
            "target_app": frm.doc.target_app,
            "locale": frm.doc.language,
        },
        callback: (r) => {
            get_po_path(frm);
            console.log(r);
            frappe.show_alert({
                message: __('Generate main.pot file: done'),
                indicator: 'green'
            }, 5);
        }
    });
}
function update_po(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.update_po",
        args: {
            "target_app": frm.doc.target_app,
            "locale": frm.doc.language,
        },
        callback: (r) => {
            console.log(r);
            frappe.show_alert({
                message: __('Generate main.pot file: done'),
                indicator: 'green'
            }, 5);
        }
    });
}

function csv_to_po(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.csv_to_po",
        args: {
            "app": frm.doc.target_app,
            "locale": frm.doc.language,
        },
        callback: (r) => {
            console.log(r);
            var msg = r.message.method + ": " + r.message.app + " " + r.message.locale;
            if (!r.message.is_ok) msg = msg + "</br>" + r.message.error;
            frappe.show_alert({
                message: msg,
                indicator: r.message.is_ok ? 'green' : 'red'
            }, 5);
        }
    });
}

function compile_translations(frm) {
    frappe.call({
        method: "frappe_translate.frappe_translate.doctype.translate_wizard.translate_wizard.compile_translations",
        args: {
            "target_app": frm.doc.target_app,
            "locale": frm.doc.language,
            "force": true,
        },
        callback: (r) => {
            console.log(r);
            frappe.show_alert({
                message: __('Generate main.pot file: done'),
                indicator: 'green'
            }, 5);
        }
    });
}

frappe.ui.form.on("Translate Wizard", {
    refresh(frm) {
        fill_installed_app(frm);
        fill_po_locales(frm);
        get_pot_path(frm);
        get_po_path(frm);
        get_csv_path(frm);
    },
    test(frm) {
        test_catalog(frm);
    },
    btn_generate_pot(frm) {
        generate_pot(frm);
    },
    target_app(frm) {
        fill_po_locales(frm);
    },
    btn_new_po(frm) {
        new_po(frm);
    },
    btn_compile_translations(frm) {
        compile_translations(frm);
    },
    btn_update_po(frm) {
        update_po(frm);
    },
    btn_csv_to_po(frm) { csv_to_po(frm) },
});