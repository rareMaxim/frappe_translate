# Copyright (c) 2024, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from babel.messages.catalog import Catalog, Message
from frappe.gettext.translate import get_catalog, write_catalog

class TranslateMessage(Document):
	
	@staticmethod
	def get_catalog()->Catalog:
		(target_app, locale) = get_current_app_lang()
		return get_catalog (target_app, locale)  
  
	@staticmethod
	def get_catalog()->Catalog:
		(target_app, locale) = get_current_app_lang()
		return get_catalog (target_app, locale)	

	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		d = self.get_valid_dict(convert_dates_to_str=True)
		catalog = TranslateMessage.get_catalog()
		id = int(self.name)
		d = message2json(id, list(catalog)[id])
		super(Document, self).__init__(d)

	def db_update(self):
		catalog: Catalog = TranslateMessage.get_catalog()
		msg = catalog.get(self.title, self.context)
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
		# wizard = frappe.get_doc("Translate Wizard",  )
		# catalog: Catalog = get_catalog (wizard.get('target_app'), wizard.get('language'))
		catalog = list(TranslateMessage.get_catalog())
		result = []
		if not 'start' in dict(args):
			return
		i =  int(args.start)+1
		while len(result) < int(args.page_length):
			if i >= len(catalog):
				break
			msg = catalog[i]
			if not msg.id:
				continue
			result.append(message2json(i, msg))  
			i += 1          
		return result

	@staticmethod
	def get_count(args):
		return len( TranslateMessage.get_catalog())

	@staticmethod
	def get_stats(args):
		pass

def get_current_app_lang():
	wizard = frappe.cache.hget("translate_wizard", frappe.session.user)
	doc_wiz = frappe.get_doc("Translate Wizard", wizard)
	target_app =  doc_wiz.get_value("target_app")
	locale = doc_wiz.get_value("language")
	return (target_app, locale)

def message2json(id:int, msg: Message):
	return ({
		"name": id,
		"title": msg.id,
		"string": msg.string,
		"context": msg.context,
		"user_comments": ''.join(str(x) for x in msg.user_comments),
		"auto_comments": ''.join(str(x) for x in msg.auto_comments),
		"locations": ''.join(str(x) for x in msg.locations),
		"flags":msg.flags,
		"lineno":msg.lineno,
		"previous_id":msg.previous_id,
		"modified": '2024-02-24 18:35:01.335664',
	})