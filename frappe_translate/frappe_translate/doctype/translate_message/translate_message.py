# Copyright (c) 2024, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from babel.messages.catalog import Catalog, Message
from frappe.gettext.translate import get_catalog, write_catalog
from frappe.utils.data import cint


class TranslateMessage(Document):

    @staticmethod
    def get_catalog() -> Catalog:
        catalog_data = get_current_app_lang()
        if not catalog_data:
            return None
        catalog = get_catalog(catalog_data[0], catalog_data[1])
        i = 0
        for msg in catalog:
            setattr(msg, "name", str(i))
            i += 1
        return catalog

    def db_insert(self, *args, **kwargs):
        pass

    def load_from_db(self):
        catalog = TranslateMessage.get_catalog()
        id = int(self.name)
        d = serialize_message(list(catalog)[id])
        super(Document, self).__init__(d)

    def db_update(self):
        catalog: Catalog = TranslateMessage.get_catalog()
        msg = catalog.get(self.id, self.context)
        msg.string = self.string
        (target_app, locale) = get_current_app_lang()
        write_catalog(target_app, catalog, locale)

    def delete(self):
        catalog = TranslateMessage.get_catalog()
        msg = list(catalog)[int(self.name)]
        catalog.delete(msg.id, msg.context)
        (target_app, locale) = get_current_app_lang()
        write_catalog(target_app, catalog, locale)

    @staticmethod
    def get_list(args):
        start = cint(args.get("start"))
        page_length = cint(args.get("page_length")) or 20
        catalog = TranslateMessage.get_filtered_requests(args)[
            start : start + page_length
        ]

        if order_by_statment := args.get("order_by"):
            if "." in order_by_statment:
                order_by_statment = order_by_statment.split(".")[1]

            if " " in order_by_statment:
                sort_key, sort_order = order_by_statment.split(" ", 1)
            else:
                sort_key = order_by_statment
                sort_order = "desc"

            sort_key = sort_key.replace("`", "")
            return sorted(
                catalog,
                key=lambda r: r.get(sort_key) or "id",
                reverse=bool(sort_order == "desc"),
            )
        return sorted(catalog, key=lambda r: r.duration, reverse=1)

    @staticmethod
    def get_count(args):
        catalog = TranslateMessage.get_filtered_requests(args)
        return len(catalog) if catalog else 0

    @staticmethod
    def get_stats(args):
        pass

    @staticmethod
    def get_filtered_requests(args):
        from frappe.utils import evaluate_filters

        wizard = update_selected_wizard(args)
        filters = args.get("filters")
        catalog = TranslateMessage.get_catalog()
        if not catalog:
            return None
        messages = [
            serialize_message(message)
            for message in TranslateMessage.get_catalog()
            if message.id
        ]
        return [msg for msg in messages if evaluate_filters(msg, filters)]


def get_current_app_lang():
    wizard = frappe.cache.hget("translate_wizard", frappe.session.user)
    if not wizard:
        return None
    doc_wiz = frappe.get_doc("Translate Wizard", wizard)
    target_app = doc_wiz.get_value("target_app")
    locale = doc_wiz.get_value("language")
    return (target_app, locale)


def serialize_message(msg: Message) -> dict:
    """Convert a gettext.Message object to a dict."""
    return {
        "name": msg.name,
        "id": msg.id,
        "string": msg.string,
        "context": msg.context,
        "user_comments": "\n".join(msg.user_comments),
        "auto_comments": "\n".join(msg.auto_comments),
        "locations": "\n".join(f"{file}:{line}" for file, line in msg.locations),
        "flags": " ".join(msg.flags) if msg.flags else "",
        "lineno": msg.lineno,
        "previous_id": msg.previous_id,
        "modified": "2024-02-24 18:35:01.335664",
        "wizard": frappe.cache.hget("translate_wizard", frappe.session.user),
    }


def update_selected_wizard(args) -> str:
    for filter in args.filters:
        if filter[1] == "wizard" and filter[2] == "=":
            frappe.cache.hset("translate_wizard", frappe.session.user, filter[3])
            return frappe.cache.hget("translate_wizard", frappe.session.user)
