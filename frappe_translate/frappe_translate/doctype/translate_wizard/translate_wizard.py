# Copyright (c) 2024, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from babel.messages.catalog import Catalog
from frappe.gettext.translate import get_catalog


class TranslateWizard(Document):
    def get_catalog(self) -> Catalog:
        from frappe.gettext.translate import get_catalog

        app = self.get_value("target_app")
        locale = self.get_value("language")
        catalog: Catalog = get_catalog(app=app, locale=locale)  #
        return catalog

    @property
    def creation_date(self):
        return self.get_catalog().creation_date

    @property
    def revision_date(self):
        return self.get_catalog().revision_date

    @property
    def charset(self):
        return self.get_catalog().charset

    @property
    def copyright_holder(self):
        return self.get_catalog().copyright_holder

    @property
    def domain(self):
        return self.get_catalog().domain

    @property
    def header_comment(self):
        return self.get_catalog().header_comment

    @property
    def language_team(self):
        return self.get_catalog().language_team

    @property
    def last_translator(self):
        return self.get_catalog().last_translator

    @property
    def last_translator(self):
        return self.get_catalog().last_translator

    @property
    def version(self):
        return self.get_catalog().version

    @property
    def project(self):
        return self.get_catalog().project

    def test(self):
        return self.get_catalog().version

    pass


@frappe.whitelist()
def get_installed_app():
    """
    get installed apps
    """
    return frappe.get_all_apps(True)


@frappe.whitelist()
def get_locales(app: str) -> list[str]:
    from frappe.gettext.translate import get_locales

    locales = get_locales(app=app)
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
def get_pot_path(app: str):
    from frappe.gettext.translate import get_pot_path

    path = get_pot_path(app)

    return {
        "path": str(path),
        "exists": path.exists(),
    }


@frappe.whitelist()
def get_po_path(app: str, locale: str | None = None):
    from frappe.gettext.translate import get_po_path

    path = get_po_path(app, locale)
    return {
        "path": str(path),
        "exists": path.exists(),
    }


@frappe.whitelist()
def get_csv_path(app: str, locale: str | None = None):
    from pathlib import Path

    path = (
        Path(frappe.get_app_path(app))
        / "translations"
        / f"{locale.replace('_', '-')}.csv"
    )
    return {
        "path": str(path),
        "exists": path.exists(),
    }


@frappe.whitelist()
def convert_csv_to_po(
    application: str | None = None, language: str | None = None
) -> dict:
    """Convert a CSV to PO for a specific language"""
    from frappe.gettext.translate import migrate

    response = {
        "method": "convert_csv_to_po",
        "application": application,
        "language": language,
    }
    try:
        migrate(app=application, locale=language)
    except Exception as e:
        response.update(error=str(e), is_successful=False)
    else:
        response.update(is_successful=True)
    return response


@frappe.whitelist()
def get_translate_catalog(app: str, locale: str | None = None) -> Catalog:
    from frappe.gettext.translate import get_catalog

    catalog: Catalog = get_catalog(app=app, locale=locale)  #
    return catalog


@frappe.whitelist()
def get_locales(app: str) -> list[str]:
    from frappe.gettext.translate import get_locales

    locales = get_locales(app=app)
    return locales


@frappe.whitelist()
def new_po(locale, target_app: str | None = None):
    from frappe.gettext.translate import new_po

    new_po(locale=locale, target_app=target_app)


@frappe.whitelist()
def update_po(target_app: str | None = None, locale: str | None = None):
    from frappe.gettext.translate import update_po

    update_po(target_app=target_app, locale=locale)


@frappe.whitelist()
def compile_translations(
    target_app: str | None = None, locale: str | None = None, force=False
):
    from frappe.gettext.translate import compile_translations

    compile_translations(target_app=target_app, locale=locale, force=force)
    frappe.clear_cache()


@frappe.whitelist()
def set_user_project(wizard: str):
    frappe.cache.hset("translate_wizard", frappe.session.user, wizard)


@frappe.whitelist()
def calculate_translation_statistics(app: str, locale: str | None = None) -> dict:
    """
    Calculate and return statistics about the number of translated messages
    in the given app and locale.

    Returns:
            dict: A dictionary with the following keys:
                    total: The total number of messages in the catalog.
                    translated: The number of translated messages.
                    percent: The percentage of translated messages (as a float).
                    percent_str: The percentage of translated messages as a string
                            (with two decimal places).
                    text: A string with a readable version of the translation progress.
    """
    catalog = get_catalog(app=app, locale=locale)
    translated_count = sum(1 for msg in catalog if msg.string)
    total = len(catalog)
    percent = translated_count / total
    percent_str = "{:.2%}".format(percent)
    return {
        "total": total,
        "translated": translated_count,
        "percent": percent,
        "percent_str": percent_str,
        "text": "Translated {} of {} ({})".format(translated_count, total, percent_str),
    }
