import discord


class MessageEmbed:

    # title : 시간 / author_name : 릴경알림 / relay_list : 릴경리스트
    def make_embed_message_for_relay_notify(self, title, author_name, relay_entity):
        embed_msg = discord.Embed(title=title)
        embed_msg.set_author(name=author_name)

        ch = relay_entity.get_channel()
        fm = relay_entity.get_first_minute()
        sm = relay_entity.get_second_minute()
        embed_msg.add_field(name=ch + "ch", value=fm + "분, " + sm)

        embed_msg.set_footer(text="!사용법 참조")
        return embed_msg


