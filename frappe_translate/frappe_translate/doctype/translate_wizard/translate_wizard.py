# Copyright (c) 2024, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from babel.messages.catalog import Catalog


class TranslateWizard(Document):
	pass


@frappe.whitelist()
def get_installed_app():
    '''
    get installed apps
    '''
    return frappe.get_all_apps(True)

@frappe.whitelist()
def get_locales(app: str) -> list[str]:
    from frappe.gettext.translate import get_locales
    locales = get_locales(app = app)
    return locales

@frappe.whitelist()
def generate_pot(target_app: str | None = None):
    from frappe.gettext.translate import generate_pot
    generate_pot(target_app=target_app)
    return {
        "generate_pot": True,
        "target_app": target_app,
        }

@frappe.whitelist()
def get_pot_path(app: str) -> str:
    from frappe.gettext.translate import get_pot_path
    path = get_pot_path(app)
    
    return {
        "path": str(path),
        "exists": path.exists(),
        }
    
@frappe.whitelist()
def csv_to_po(app: str | None = None, locale: str | None = None):
    from frappe.gettext.translate import migrate
    response = {}
    response.update({"method":"csv_to_po",
                     "app": app,
                     "locale": locale})
    try:
        migrate(app=app, locale = locale)
    except Exception as e:
        response.update({"error": e, "is_ok": False})
    else: 
        response.update({"is_ok": True})
    return response

@frappe.whitelist()
def get_translate_catalog(app: str, locale: str | None = None) -> Catalog:
    from frappe.gettext.translate import get_catalog
    catalog: Catalog = get_catalog(app = app, locale = locale) #
    return catalog

@frappe.whitelist()
def get_locales(app: str) -> list[str]:
    from frappe.gettext.translate import get_locales
    locales = get_locales(app = app)
    return locales

@frappe.whitelist()
def new_po(locale, target_app: str | None = None):
    from frappe.gettext.translate import new_po
    new_po(locale = locale, target_app = target_app)

@frappe.whitelist()
def update_po(target_app: str | None = None, locale: str | None = None):
    from frappe.gettext.translate import update_po
    update_po(target_app = target_app, locale = locale)
        
@frappe.whitelist()
def compile_translations(target_app: str | None  = None, locale: str | None = None, force=False):
    from frappe.gettext.translate import compile_translations
    compile_translations(target_app = target_app, locale = locale, force = force)    
    
@frappe.whitelist()
def set_user_project(user, wizard: str):
    frappe.cache.hset("translate_wizard", frappe.session.user, wizard)