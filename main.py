import discord
from discord.ext import tasks
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
    cleanup_expired_tickets,
    save_ticket,
)

from views import (
    TicketView,
    build_embed,
    update_card,
    build_list_embed,
    ListDashboardView,
    build_on_hold_reminder_embed,
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


async def safe_respond(interaction: discord.Interaction, content=None, embed=None, view=None, ephemeral=True):
    try:
        if interaction.response.is_done():
            kwargs = {"ephemeral": ephemeral}
            if content:
                kwargs["content"] = content
            if embed:
                kwargs["embed"] = embed
            if view:
                kwargs["view"] = view
            await interaction.followup.send(**kwargs)
        else:
            kwargs = {"ephemeral": ephemeral}
            if content:
                kwargs["content"] = content
            if embed:
                kwargs["embed"] = embed
            if view:
                kwargs["view"] = view
            await interaction.response.send_message(**kwargs)
    except discord.HTTPException as e:
        if getattr(e, "code", None) == 40060:
            pass  # Already acknowledged by another instance
        else:
            print(f"[WARN] safe_respond HTTPException: {e}")


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
        await safe_respond(
            interaction,
            content=f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    await safe_respond(
        interaction,
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
    description="Xem danh sách tổng quan các ticket theo ngày và trạng thái"
)
@discord.app_commands.describe(
    date="Chọn mốc thời gian hiển thị",
    filter="Lọc theo trạng thái ticket"
)
@discord.app_commands.choices(
    date=[
        discord.app_commands.Choice(name="Hôm nay (Today - Mặc định)", value="today"),
        discord.app_commands.Choice(name="Hôm qua (Yesterday)", value="yesterday"),
        discord.app_commands.Choice(name="7 ngày gần đây (Last 7 Days)", value="week"),
        discord.app_commands.Choice(name="Tất cả thời gian (All Time)", value="all"),
    ],
    filter=[
        discord.app_commands.Choice(name="Tất cả trạng thái (All)", value="all"),
        discord.app_commands.Choice(name="Đang xử lý (In Progress)", value="in_progress"),
        discord.app_commands.Choice(name="Tạm dừng (Paused / On Hold)", value="on_hold"),
        discord.app_commands.Choice(name="Đã hoàn thành (Done)", value="done"),
        discord.app_commands.Choice(name="Đã hủy (Cancelled)", value="cancelled"),
    ]
)
async def list_tickets(
    interaction: discord.Interaction,
    date: discord.app_commands.Choice[str] = None,
    filter: discord.app_commands.Choice[str] = None
):
    date_val = date.value if date else "today"
    filter_val = filter.value if filter else "all"

    embed = build_list_embed(filter_val, date_val)
    view = ListDashboardView(filter_val, date_val)

    await safe_respond(
        interaction,
        embed=embed,
        view=view,
        ephemeral=True
    )


# ============================================================
# /ONHOLD & /REMIND (NHẮC NHỞ ĐẦU CA LÀM VIỆC)
# ============================================================

@tree.command(
    name="onhold",
    description="Nhắc nhở kiểm tra các ticket đang tạm dừng (On Hold) khi bắt đầu làm việc"
)
async def onhold_cmd(interaction: discord.Interaction):
    embed = build_on_hold_reminder_embed()
    await safe_respond(
        interaction,
        embed=embed,
        ephemeral=True
    )


@tree.command(
    name="remind",
    description="Nhắc nhở các ticket On Hold cần kiểm tra phản hồi trong ngày"
)
async def remind_cmd(interaction: discord.Interaction):
    embed = build_on_hold_reminder_embed()
    await safe_respond(
        interaction,
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
        await safe_respond(
            interaction,
            content=f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    add_note(ticket_id, text)
    await update_card(ticket_id, bot)

    await safe_respond(
        interaction,
        content=f"📝 Added note to **Ticket #{ticket_id}**:\n> {text}",
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
        await safe_respond(
            interaction,
            content=f"❌ Ticket #{ticket.upper()} not found.",
            ephemeral=True
        )
        return

    await safe_respond(
        interaction,
        content=f"🗑️ Ticket #{ticket_id} deleted.",
        ephemeral=False
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
        await safe_respond(
            interaction,
            content=f"❌ Ticket #{ticket.upper()} không tồn tại.",
            ephemeral=True
        )
        return

    success, msg = undo_ticket_step(ticket_id)
    if not success:
        await safe_respond(
            interaction,
            content=f"⚠️ **Ticket #{ticket_id}**: {msg}",
            ephemeral=True
        )
        return

    await update_card(ticket_id, bot)
    await safe_respond(
        interaction,
        content=f"↩️ **Ticket #{ticket_id}**: {msg}",
        embed=build_embed(ticket_id),
        view=TicketView(ticket_id),
        ephemeral=True
    )

undo_cmd.autocomplete("ticket")(ticket_autocomplete)


# ============================================================
# /REOPEN
# ============================================================

@tree.command(
    name="reopen",
    description="Mở lại (Re-open) một ticket đã hoàn thành hoặc đã hủy"
)
@discord.app_commands.describe(ticket="Ticket ID (ví dụ: ENRICH-1469350)")
async def reopen_cmd(
    interaction: discord.Interaction,
    ticket: str
):
    ticket_id = find_ticket_id(ticket)

    if not ticket_exists(ticket_id):
        await safe_respond(
            interaction,
            content=f"❌ Ticket #{ticket.upper()} không tồn tại.",
            ephemeral=True
        )
        return

    ticket_data = tickets[ticket_id]
    if ticket_data.get("status") not in ("done", "cancelled"):
        await safe_respond(
            interaction,
            content=f"⚠️ Ticket #{ticket_id} hiện đang ở trạng thái `{ticket_data.get('status')}` (chỉ có thể Re-open khi đã Done hoặc Cancelled).",
            ephemeral=True
        )
        return

    reopen_ticket(ticket_id)
    await update_card(ticket_id, bot)

    await safe_respond(
        interaction,
        content=f"🔄 Ticket #{ticket_id} đã được **RE-OPEN** thành công!",
        embed=build_embed(ticket_id),
        view=TicketView(ticket_id),
        ephemeral=True
    )

reopen_cmd.autocomplete("ticket")(ticket_autocomplete)


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
        # REOPEN TICKET (DONE hoặc CANCEL từ ngày hôm trước)
        # ----------------------------------------------------
        if ticket.get("status") in ("done", "cancelled"):
            from datetime import datetime
            now_date = datetime.now().date()
            is_previous_day = False

            if ticket.get("completed_at"):
                is_previous_day = ticket["completed_at"].date() < now_date
            elif ticket.get("created_at"):
                is_previous_day = ticket["created_at"].date() < now_date

            if is_previous_day:
                reopen_ticket(ticket_id)
                ticket["channel_id"] = message.channel.id

                sent = await message.channel.send(
                    embed=build_embed(ticket_id),
                    view=TicketView(ticket_id)
                )
                ticket["message_id"] = sent.id
                save_ticket(ticket_id)

                await message.reply(
                    f"🔄 Ticket #{ticket_id} (đã xong/hủy từ hôm trước) đã được **RE-OPEN** và mở lại tại đây!"
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
# BACKGROUND TASKS (CLEANUP SAU 30 NGÀY)
# ============================================================

@tasks.loop(hours=24)
async def daily_cleanup_task():
    try:
        deleted = cleanup_expired_tickets(days=30)
        if deleted > 0:
            print(f"🧹 [DAILY TASK] Đã xóa {deleted} ticket hoàn thành/hủy hơn 30 ngày.")
    except Exception as e:
        print(f"[ERROR] daily_cleanup_task: {e}")


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

    if not daily_cleanup_task.is_running():
        daily_cleanup_task.start()
        print("✅ Daily 30-day ticket cleanup task started.")

    print("================================")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)