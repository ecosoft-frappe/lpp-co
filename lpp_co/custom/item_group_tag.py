import frappe


# Called from scheduler to reset group tags to latest as item groups
def prepare_group_tags(doc=None, method=None):
	# From all Item Group, create Item Group Tags
	frappe.db.sql("""
		insert into `tabItem Group Tag` (name)
		select distinct item_group_name from `tabItem Group`
		where item_group_name not in (select name from `tabItem Group Tag`)
    """)
	# Reset the use in levels to 0
	frappe.db.sql("""
        update `tabItem Group Tag`
        set level_0 = 0, level_1 = 0, level_2 = 0, level_3 = 0
    """)
	# Loop through all Item Group, level 0 to level 3
	update_levels(0, ("", None))
	# Delete what not used
	frappe.db.sql("""
        delete from `tabItem Group Tag` where
        level_0 = 0 and level_1 = 0 and level_2 = 0 and level_3 = 0
    """)
	frappe.db.commit()
 
 
def update_levels(level, parent):
	for item_group in frappe.get_all(
			"Item Group",
			filters={"parent_item_group": ["in", parent]},
			fields=["name", "item_group_name"]
		):
		frappe.db.set_value("Item Group Tag", item_group["item_group_name"], "level_%s" % level, 1)
		if level < 3:
			update_levels(level+1, item_group["name"])


# Called when item is updated, update item group tags
def update_item_group_tags_all(doc, method=None):
	items = frappe.get_all("Item", {}, pluck="name")
	for item_name in items:
		item = frappe.get_doc("Item", item_name)
		update_item_group_tags(item, method=None)
	

def update_item_group_tags(doc, method=None):
	# Reset
	frappe.db.sql("""
		update `tabItem`
  		set custom_item_group_1 = null,
    		custom_item_group_2 = null,
      		custom_item_group_3 = null
    	where name = %s
    """, doc.name)
	# Start with this item group, and climb parents
	parent = doc.item_group
	while parent:
		if not frappe.db.exists("Item Group", parent):
			parent = None
			continue
		item_group = frappe.get_doc("Item Group", parent)
		level = get_item_group_level(item_group.name)
		if level in (1, 2, 3):
			frappe.db.sql("""
				update `tabItem`
				set custom_item_group_%s = %s
				where name = %s
			""", (level, item_group.item_group_name, doc.name))
		parent = item_group.parent_item_group
	frappe.db.commit()
	doc.reload()


def get_item_group_level(item_group_id):
    item_group = frappe.get_doc("Item Group", item_group_id)
    lft = item_group.lft
    rgt = item_group.rgt
    item_groups = frappe.get_all("Item Group", fields=["name", "lft", "rgt"])
    level = 0
    for group in item_groups:
        if group.lft < lft and group.rgt > rgt:
            level += 1
    return level
