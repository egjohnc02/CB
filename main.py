import discord
import re

from config import TOKEN, GUILD_ID

from ticket_manager import (
    tickets,
    create_ticket,
    ticket_exists,
    delete_ticket,
    reopen_ticket,
    add_note,
    find_ticket_id,
    undo_ticket_step,
)

from views import (
    TicketView,
    build_embed,
    update_card,
    build_list_embed,
)


# ============================================================
# DISCORD
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


# ============================================================
# TICKET DETECTION
# ============================================================

# Matches patterns like ENRICH-1469350, PROJ-1234, or ticket: 1469350, ticket #ENRICH-1469350
ticket_pattern = re.compile(
    r"\b(?:ticket\s*[:#-]?\s*)?([A-Za-z]{2,}-\d+)\b|\bticket\s*[:#-]?\s*([A-Za-z0-9_-]+)\b",
    re.IGNORECASE
)


# ============================================================
# AUTOCOMPLETE HELPER
# ============================================================

async def ticket_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[discord.app_commands.Choice[str]]:
    current_clean = current.strip().upper()
    choices = []

    for tid in tickets.keys():
        if not current_clean or current_clean in tid:
            choices.append(
                discord.app_commands.Choice(name=tid, value=tid)
            )

    return choices[:25]


# ============================================================
# /STATUS
# ============================================================

@tree.command(
    name="status",
    description="Check and continue working on a ticket"
)
@discord.app_commands.describe(ticket="Ticket ID (e.g. ENRICH-1469350)")
async def status(
    interaction: discord.Interaction,
    ticket: str
):
    ticket_id = find_ticket_id(ticket)

    if not ticket_exists(ticket_id):
        await interaction.response.send_message(
            f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        embed=build_embed(ticket_id),
        view=TicketView(ticket_id),
        ephemeral=True
    )

status.autocomplete("ticket")(ticket_autocomplete)


# ============================================================
# /LIST (DASHBOARD)
# ============================================================

@tree.command(
    name="list",
    description="Xem danh sách tổng quan các ticket và bước hiện tại"
)
@discord.app_commands.describe(
    filter="Lọc theo trạng thái ticket"
)
@discord.app_commands.choices(
    filter=[
        discord.app_commands.Choice(name="Tất cả (All)", value="all"),
        discord.app_commands.Choice(name="Đang xử lý (In Progress)", value="in_progress"),
        discord.app_commands.Choice(name="Tạm dừng (Paused / On Hold)", value="on_hold"),
        discord.app_commands.Choice(name="Đã hoàn thành (Done)", value="done"),
        discord.app_commands.Choice(name="Đã hủy (Cancelled)", value="cancelled"),
    ]
)
async def list_tickets(
    interaction: discord.Interaction,
    filter: discord.app_commands.Choice[str] = None
):
    filter_val = filter.value if filter else "all"
    embed = build_list_embed(filter_val)
    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )


# ============================================================
# /NOTE
# ============================================================

@tree.command(
    name="note",
    description="Add a note to a ticket"
)
@discord.app_commands.describe(
    ticket="Ticket ID (e.g. ENRICH-1469350)",
    text="Note content"
)
async def note(
    interaction: discord.Interaction,
    ticket: str,
    text: str
):
    ticket_id = find_ticket_id(ticket)

    if not ticket_exists(ticket_id):
        await interaction.response.send_message(
            f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    add_note(ticket_id, text)
    await update_card(ticket_id, bot)

    await interaction.response.send_message(
        f"📝 Added note to **Ticket #{ticket_id}**:\n> {text}",
        ephemeral=True
    )

note.autocomplete("ticket")(ticket_autocomplete)


# ============================================================
# /DELETE
# ============================================================

@tree.command(
    name="delete",
    description="Delete a ticket"
)
@discord.app_commands.describe(ticket="Ticket ID (e.g. ENRICH-1469350)")
async def delete(
    interaction: discord.Interaction,
    ticket: str
):
    ticket_id = find_ticket_id(ticket)

    if not delete_ticket(ticket_id):
        await interaction.response.send_message(
            f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"🗑️ Ticket #{ticket_id} deleted."
    )

# ============================================================
# /UNDO
# ============================================================

@tree.command(
    name="undo",
    description="Hoàn tác bước gần nhất của ticket"
)
@discord.app_commands.describe(ticket="Ticket ID (ví dụ: ENRICH-1469350)")
async def undo_cmd(
    interaction: discord.Interaction,
    ticket: str
):
    ticket_id = find_ticket_id(ticket)

    if not ticket_exists(ticket_id):
        await interaction.response.send_message(
            f"❌ Ticket #{ticket.upper()} không tồn tại.",
            ephemeral=True
        )
        return

    success, msg = undo_ticket_step(ticket_id)
    if not success:
        await interaction.response.send_message(
            f"⚠️ **Ticket #{ticket_id}**: {msg}",
            ephemeral=True
        )
        return

    await update_card(ticket_id, bot)
    await interaction.response.send_message(
        f"↩️ **Ticket #{ticket_id}**: {msg}",
        embed=build_embed(ticket_id),
        view=TicketView(ticket_id),
        ephemeral=True
    )

undo_cmd.autocomplete("ticket")(ticket_autocomplete)


# ============================================================
# MESSAGE HANDLER
# ============================================================

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Ignore slash commands or prefix commands typed into chat
    if message.content.startswith("/"):
        return

    match = ticket_pattern.search(message.content)
    if not match:
        return

    raw_ticket_id = (match.group(1) or match.group(2)).upper()
    ticket_id = find_ticket_id(raw_ticket_id)

    # ========================================================
    # EXISTING
    # ========================================================
    if ticket_exists(ticket_id):
        ticket = tickets[ticket_id]

        # ----------------------------------------------------
        # REOPEN AFTER 24 HOURS
        # ----------------------------------------------------
        if ticket["status"] == "done" and ticket["completed_at"]:
            from datetime import datetime
            elapsed = datetime.now() - ticket["completed_at"]

            if elapsed.total_seconds() >= 86400:
                reopen_ticket(ticket_id)
                await update_card(ticket_id, bot)

                await message.reply(
                    f"🔄 Ticket #{ticket_id} has been **RE-OPENED**."
                )
                return

        await message.reply(
            f"⚠️ Ticket #{ticket_id} already exists.\n"
            f"Use `/status` to check it."
        )
        return

    # ========================================================
    # NEW
    # ========================================================
    ticket_id = create_ticket(raw_ticket_id)
    ticket = tickets[ticket_id]
    ticket["channel_id"] = message.channel.id

    sent = await message.channel.send(
        embed=build_embed(ticket_id),
        view=TicketView(ticket_id)
    )

    ticket["message_id"] = sent.id
    print(f"[NEW] Ticket #{ticket_id}")


# ============================================================
# READY
# ============================================================

@bot.event
async def on_ready():
    print("================================")
    print(f"Bot online: {bot.user}")

    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        print("❌ Server not found. Check GUILD_ID.")
        return

    print(f"✅ Server: {guild.name}")

    try:
        tree.copy_global_to(guild=guild)
        synced = await tree.sync(guild=guild)
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync error: {e}")

    print("================================")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)