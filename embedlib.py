from discord import Embed


def long_embed(fields_texts, title="Default Title", description="Default description", fields_title="default title"):
	embed_list = [Embed(title=title, description=description)]
	fields_count = 0
	temp_text = ""
	for fields_part in fields_texts:
		if len(temp_text) + len(fields_part) >= 1024:
			embed_list[-1].add_field(name=fields_title + "{}".format(fields_count), value=temp_text, inline=True)
			temp_text = fields_part
			fields_count += 1
		else:
			temp_text += fields_part
	embed_list[-1].add_field(name=fields_title + "{}".format(fields_count), value=temp_text, inline=True)
	return embed_list
