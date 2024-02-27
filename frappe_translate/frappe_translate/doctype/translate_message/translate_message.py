# Copyright (c) 2024, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from babel.messages.catalog import Catalog, Message
from frappe.gettext.translate import get_catalog, write_catalog
from frappe.utils.data import cint


class TranslateMessage(Document):
	
	@staticmethod
	def get_catalog()->Catalog:
		(target_app, locale) = get_current_app_lang()
		catalog = list(get_catalog (target_app, locale)) 
		i = 0
		for msg in catalog:
			setattr(msg, "name", str(i))
			i += 1
		return catalog

	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		d = self.get_valid_dict(convert_dates_to_str=True)
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
		catalog = TranslateMessage.get_filtered_requests(args)[start : start + page_length]
  
		if order_by_statment := args.get("order_by"):
			if "." in order_by_statment:
				order_by_statment = order_by_statment.split(".")[1]

			if " " in order_by_statment:
				sort_key, sort_order = order_by_statment.split(" ", 1)
			else:
				sort_key = order_by_statment
				sort_order = "desc"

			sort_key = sort_key.replace("`", "")
			print(f"sort_key = {sort_key}, sort_order = {sort_order}")
			return sorted(catalog, key=lambda r: r.get(sort_key) or "id", reverse=bool(sort_order == "desc"))
		return sorted(catalog, key=lambda r: r.duration, reverse=1)

	@staticmethod
	def get_count(args):
		update_selected_wizard(args)
		return len(TranslateMessage.get_filtered_requests(args))

	@staticmethod
	def get_stats(args):
		update_selected_wizard(args)
		return

	@staticmethod
	def get_filtered_requests(args):
		from frappe.utils import evaluate_filters
		filters = args.get("filters")
		messages = [serialize_message(message) for message in TranslateMessage.get_catalog() if message.id]
		return [msg for msg in messages if evaluate_filters(msg, filters)]

def get_current_app_lang():
	wizard = frappe.cache.hget("translate_wizard", frappe.session.user)
	doc_wiz = frappe.get_doc("Translate Wizard", wizard)
	target_app =  doc_wiz.get_value("target_app")
	locale = doc_wiz.get_value("language")
	return (target_app, locale)

def serialize_message(msg: Message):
	return ({
		# "name": f'{msg.context} {msg.id}',
  		"name": msg.name,
		"id": msg.id,
		"string": msg.string,
		"context": msg.context,
		"user_comments": '\n'.join(str(x) for x in msg.user_comments),
		"auto_comments": '\n'.join(str(x) for x in msg.auto_comments), 
		"locations": ''.join(f'{x[0]}:{x[1]}' for x in msg.locations),
		"flags": msg.flags,
		"lineno": msg.lineno,
		"previous_id": msg.previous_id,
		"modified": '2024-02-24 18:35:01.335664',
		"wizard": frappe.cache.hget("translate_wizard", frappe.session.user),
	})
 
def update_selected_wizard(args)->str:
#  {'doctype': 'Translate Message', 'fields': ['`tabTranslate Message`.`name`', '`tabTranslate Message`.`owner`', '`tabTranslate Message`.`creation`', 
# '`tabTranslate Message`.`modified`', '`tabTranslate Message`.`modified_by`', '`tabTranslate Message`.`_user_tags`', '`tabTranslate Message`.`_comments`', 
# '`tabTranslate Message`.`_assign`', '`tabTranslate Message`.`_liked_by`', '`tabTranslate Message`.`docstatus`', '`tabTranslate Message`.`idx`', 
# '`tabTranslate Message`.`context`', '`tabTranslate Message`.`title`', '`tabTranslate Message`.`string`'], 
# 'filters': [['Translate Message', 'wizard', '=', 'Frappe Ukraine']], 'order_by': '`tabTranslate Message`.`title` asc', 'start': '0', 'page_length': '20', 
# 'group_by': '`tabTranslate Message`.`name`', 'with_comment_count': '1', 'save_user_settings': True, 'strict': None}
	for filter in args.filters:
		if filter[1] == "wizard" and filter[2] == "=":
			# e.g. ['WooCommerce Order', 'name', '=', '11']
			# params['include'] = [filter[3]]
			frappe.cache.hset("translate_wizard", frappe.session.user, filter[3])


def apply_catalog_filter(catalog, filter):
    pass

def frappe_sort(obj_list:list, sort:str):
	# `tabTranslate Message`.`title` asc
	from operator import attrgetter
	# ['', 'tabTranslate Message', '.', 'title', ' asc']
	parts = sort.split('`')
	return sorted(obj_list, key=attrgetter(parts[3]), reverse = parts[4].find('desc') >= 0)

def _eval_filters(filter, values: list[str]) -> list[str]:
	from frappe.utils import compare
	if filter:
		operator, operand = filter
		return [val for val in values if compare(val, operator, operand)]
	return values